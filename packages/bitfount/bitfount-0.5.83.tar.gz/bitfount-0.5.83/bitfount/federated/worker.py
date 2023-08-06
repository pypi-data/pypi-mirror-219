"""Workers for handling task running on pods."""
from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
from sqlite3 import Connection
from typing import Any, List, Optional, Sequence, cast

import pandas as pd
import sqlvalidator

from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
    MultiTableSource,
)
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datasources.views import SQLDataView
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import DataStructureError
from bitfount.data.schema import BitfountSchema
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.authorisation_checkers import _AuthorisationChecker
from bitfount.federated.exceptions import PodDBError, PodSchemaMismatchError
from bitfount.federated.helper import TaskContext
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.monitoring.monitor import task_config_update
from bitfount.federated.pod_db_utils import (
    _map_task_to_hash_add_to_db,
    _save_results_to_db,
)
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseProtocolFactory,
    _BaseProtocol,
)
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import (
    SerializedAlgorithm,
    SerializedProtocol,
    _DataLessAlgorithm,
)
from bitfount.federated.utils import _PROTOCOLS
from bitfount.hooks import BaseProtocolHook
from bitfount.hub.api import BitfountHub
from bitfount.schemas.utils import bf_load
from bitfount.types import _JSONDict

logger = _get_federated_logger(__name__)


class SaveResultsToDatabase(BaseProtocolHook):
    """Hook to save protocol results to database."""

    def on_run_end(
        self, protocol: _BaseProtocol, context: TaskContext, *args: Any, **kwargs: Any
    ) -> None:
        """Runs after protocol run to save results to database."""
        if context == TaskContext.WORKER:
            worker: _Worker = kwargs["worker"]
            db_con: Connection = kwargs["db_con"]
            table: Optional[str] = kwargs["table"]
            results: Any = kwargs["results"]
            # pod_db is always false for DatabaseSource,
            # which is the only datasource that accepts sqlquery
            # instead of table name, so we can cast
            # if pod_db is true, task_hash is a str,
            # so it's safe to cast
            if isinstance(results, list):
                # This is set in another `if self._pod_db` block above so can
                # assert on it to make mypy happy
                assert table is not None  # nosec assert_used

                _save_results_to_db(
                    results=results,
                    pod_identifier=worker.parent_pod_identifier,
                    task_hash=cast(str, worker._task_hash),
                    table=worker.get_pod_db_table_name(table),
                    query=worker._get_pod_datasource_query(),
                    datasource=worker.datasource,
                    show_datapoints_in_results_db=worker._show_datapoints_in_results_db,
                    run_on_new_data_only=worker.run_on_new_data_only,
                    project_db_con=db_con,
                )
            else:
                logger.warning(
                    "Results cannot be saved to pod database. "
                    "Results can be only saved to database if "
                    "they are returned from the algorithm as a list, "
                    f"whereas the chosen protocol returns {type(results)}."
                )
            db_con.close()


class _Worker:
    """Client worker which runs a protocol locally.

    Args:
        datasource: BaseSource object.
        schema: BitfountSchema object corresponding to the datasource. This is just
            used to validate the protocol.
        mailbox: Relevant mailbox.
        bitfounthub: BitfountHub object.
        authorisation: AuthorisationChecker object.
        parent_pod_identifier: Identifier of the pod the Worker is running in.
        serialized_protocol: SerializedProtocol dictionary that the Pod has received
            from the Modeller.
        pod_vitals: PodVitals object.
        pod_dp: DPPodConfig object.
        pod_db: Whether the pod has a databse associated with it. Defaults to False.
        show_datapoints_in_results_db: Whether the datasource records are shown
            in the results database. Defaults to True.
        project_id: The project id. Defaults to None.
        run_on_new_data_only: Whether to run on the whole dataset or only on
            new data. Defaults to False.
        data_identifier: The logical pod/datasource identifier for the task the
            worker has been created for. May differ from the pod identifier for
            pods with multiple datasources. Defaults to the parent_pod_identifier
            if not otherwise provided.
        batched_execution: Whether to run the protocol in batched mode. Defaults to
            False.
        multi_pod_task: Whether the task is a multi-pod task. Defaults to False.
    """

    def __init__(
        self,
        datasource: BaseSource,
        schema: BitfountSchema,
        mailbox: _WorkerMailbox,
        bitfounthub: BitfountHub,
        authorisation: _AuthorisationChecker,
        parent_pod_identifier: str,
        serialized_protocol: SerializedProtocol,
        pod_vitals: Optional[_PodVitals] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_db: bool = False,
        show_datapoints_in_results_db: bool = True,
        project_id: Optional[str] = None,
        run_on_new_data_only: bool = False,
        data_identifier: Optional[str] = None,
        batched_execution: bool = False,
        multi_pod_task: bool = False,
        **_kwargs: Any,
    ):
        self.datasource = datasource
        self.schema = schema
        self.mailbox = mailbox
        self.hub = bitfounthub
        self.authorisation = authorisation
        self.parent_pod_identifier = parent_pod_identifier
        self.serialized_protocol = serialized_protocol
        self.pod_vitals = pod_vitals
        self._pod_dp = pod_dp
        self.project_id = project_id
        self.multi_pod_task = multi_pod_task
        # We only consider making use of the pod_db if we are working in a project
        # (project_id is not None) and the datasource isn't a DatabaseSource
        self._pod_db = (
            pod_db
            if project_id is not None
            and not isinstance(self.datasource, DatabaseSource)
            else False
        )
        self._show_datapoints_in_results_db = (
            show_datapoints_in_results_db if self._pod_db else False
        )
        self.run_on_new_data_only = run_on_new_data_only if self._pod_db else False
        # Compute task hash on ordered json dictionary
        self._task_hash = (
            hashlib.sha256(
                json.dumps(serialized_protocol, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if self._pod_db
            else None
        )

        # The logical pod/datasource identifier that is actually being used by
        # this worker. For multidatasource pods, this will be different than the
        # pod identifier of the physical pod that the worker is running on
        # (parent_pod_identifier).
        # Will still be of the form: <pod_namespace>/<datasource_name>
        self._data_identifier = (
            data_identifier if data_identifier else self.parent_pod_identifier
        )

        self.batched_execution = batched_execution

        # Set up the results saving hook. This is idempotent so it's safe to
        # call it multiple times for different tasks
        if self._pod_db:
            SaveResultsToDatabase().register()

    def _update_task_config(self) -> None:
        """Send task config update to monitor service.

        Also checks that the schema in the task config matches the schema of the
        pod (if there is only a single pod in the task) and raises a
        PodSchemaMismatchError if it doesn't.
        """
        # remove schema from task_config to limit request body size
        task_config = copy.deepcopy(self.serialized_protocol)
        algorithm = task_config["algorithm"]
        algorithms = algorithm if isinstance(algorithm, list) else [algorithm]
        for algorithm in algorithms:
            if "model" in algorithm.keys():
                model = algorithm["model"]
                if "schema" in model:
                    if (
                        not self.multi_pod_task
                        and BitfountSchema.load(model["schema"]) != self.schema
                    ):
                        raise PodSchemaMismatchError(
                            f"Schema mismatch between pod and task in model "
                            f"{model['class_name']}. "
                        )
                    del model["schema"]

        task_config_update(dict(task_config))

    async def run(self) -> None:
        """Calls relevant training procedure and sends back weights/results."""
        # Send task to Monitor service. This is done regardless of whether or not
        # the task is accepted. This method is being run in a task monitor context
        # manager so no need to set the task monitor prior to sending.
        self._update_task_config()

        # Check authorisation with access manager
        authorisation_errors = await self.authorisation.check_authorisation()

        if authorisation_errors.messages:
            # Reject task, as there were errors
            await self.mailbox.reject_task(
                authorisation_errors.messages,
            )
            return

        # Accept task and inform modeller
        logger.info("Task accepted, informing modeller.")
        await self.mailbox.accept_task()
        # Wait for Modeller to give the green light to start the task
        await self.mailbox.get_task_start_update()

        # Update hub instance if BitfountModelReference
        algorithm = self.serialized_protocol["algorithm"]
        if not isinstance(self.serialized_protocol["algorithm"], list):
            algorithm = [cast(SerializedAlgorithm, algorithm)]

        algorithm = cast(List[SerializedAlgorithm], algorithm)
        for algo in algorithm:
            if model := algo.get("model"):
                if model["class_name"] == "BitfountModelReference":
                    logger.debug("Patching model reference hub.")
                    model["hub"] = self.hub

        # Deserialize protocol only after task has been accepted just to be safe
        protocol = cast(
            BaseProtocolFactory,
            bf_load(cast(_JSONDict, self.serialized_protocol), _PROTOCOLS),
        )
        # For FederatedAveraging, we return a dictionary of
        # validation metrics, which is incompatible with the database.
        if isinstance(protocol, FederatedAveraging):
            self._pod_db = False
        # Load data according to model datastructure if one exists.
        # For multi-algorithm protocols, we assume that all algorithm models have the
        # same datastructure.
        datastructure: Optional[DataStructure] = None
        algorithm_ = protocol.algorithm
        if not isinstance(algorithm_, Sequence):
            algorithm_ = [algorithm_]

        algorithm_ = cast(List[BaseCompatibleAlgoFactory], algorithm_)
        if self._pod_db:
            project_db_con = sqlite3.connect(f"{self.project_id}.sqlite")
            cur = project_db_con.cursor()
            cur.execute(
                f"""CREATE TABLE IF NOT EXISTS "{self._task_hash}" (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""  # noqa: B950
            )
        table: Optional[str] = None
        for algo_ in algorithm_:
            # TODO: [BIT-2709] This should not be run once per algorithm, but once
            # per protocol
            if isinstance(algo_, _BaseModelAlgorithmFactory):
                datastructure = algo_.model.datastructure
                if self.project_id:
                    algo_.project_id = self.project_id
            if isinstance(algo_, _DataLessAlgorithm):
                self._pod_db = False
            else:
                if self._pod_db:
                    table = self._load_data_for_worker(
                        datastructure=datastructure, project_db_con=project_db_con
                    )
                    # task_hash is set if pod_db is true, so it's safe to cast
                    _map_task_to_hash_add_to_db(
                        self.serialized_protocol,
                        cast(str, self._task_hash),
                        project_db_con,
                    )
                else:
                    # We execute the query directly on the db connection,
                    # or load the data at runtime for a csv.
                    # TODO: [NO_TICKET: Reason] No ticket created yet. Add the private sql query algorithm here as well. # noqa: B950
                    self._load_data_for_worker(datastructure=datastructure)

        # Calling the `worker` method on the protocol also calls the `worker` method on
        # underlying objects such as the algorithm and aggregator. The algorithm
        # `worker` method will also download the model from the Hub if it is a
        # `BitfountModelReference`
        worker_protocol = protocol.worker(mailbox=self.mailbox, hub=self.hub)

        # If the algorithm is a model algorithm, then we need to pass the pod identifier
        # to the model so that it can extract the relevant information from the
        # datastructure the Modeller has sent. This must be done after the worker
        # protocol has been created, so that any model references have been converted
        # to models.
        for worker_algo in worker_protocol.algorithms:
            if isinstance(worker_algo, _BaseModelAlgorithm):
                worker_algo.model.set_datastructure_identifier(self._data_identifier)

        try:
            await worker_protocol.run(
                datasource=self.datasource,
                pod_dp=self._pod_dp,
                pod_vitals=self.pod_vitals,
                pod_identifier=self.mailbox.pod_identifier,
                batched_execution=self.batched_execution,
                context=TaskContext.WORKER,
                hook_kwargs={
                    "worker": self,
                    "db_con": project_db_con if self._pod_db else None,
                    "table": table if self._pod_db else None,
                },
            )
        except Exception:
            logger.error("Exception encountered during task execution. Aborting task.")
            await self.mailbox.send_task_abort_message()
            raise
        else:
            await self.mailbox.get_task_complete_update()
        finally:
            if isinstance(self.datasource, FileSystemIterableSource):
                self.datasource.selected_file_names_override = []
            logger.info("Task complete.")
            self.mailbox.delete_all_handlers(_BitfountMessageType.LOG_MESSAGE)

    def _load_data_for_worker(
        self,
        datastructure: Optional[DataStructure] = None,
        project_db_con: Optional[Connection] = None,
    ) -> Optional[str]:
        """Load the data for the worker and returns table_name."""
        sql_query: Optional[str] = None
        table: Optional[str] = None
        kwargs = {}

        if datastructure:
            if datastructure.table:
                # If the table definition is a dict then it defines
                # pod_ids -> pod table names.
                # We need to extract the table name that corresponds to _this_
                # pod/datasource.
                if isinstance(datastructure.table, dict):
                    if not (table := datastructure.table.get(self._data_identifier)):
                        raise DataStructureError(
                            f"Table definition not found for"
                            f" {self._data_identifier}."
                            f" Table definitions provided in this DataStructure:"
                            f" {str(datastructure.table)}"
                        )
                    kwargs["table_name"] = table
                # If the table definition is a single string then we are only
                # referencing a single pod (this one) and so it refers to the
                # table name directly.
                # Need to establish that this table name is correct and exists for
                # the datasource.
                elif isinstance(datastructure.table, str):
                    table = datastructure.table

                    if not self.datasource.multi_table:
                        # If the datasource is single table, the target table name
                        # must match the "pod name"/"datasource name" to be valid
                        single_table_name = self._data_identifier.split("/")[1]
                        if table != single_table_name:
                            raise DataStructureError(
                                f"Table definition not found for"
                                f" {single_table_name} (from {self._data_identifier})."
                                f" Table definitions provided in this DataStructure:"
                                f" {str(datastructure.table)}"
                            )
                    else:
                        # In the case of multitable datasources, it could be _any_
                        # of the tables, so need to check against that.
                        data_table_names = cast(
                            MultiTableSource, self.datasource
                        ).table_names
                        if table not in data_table_names:
                            raise DataStructureError(
                                f"Table definition was supplied for {table} but"
                                f" this does not match any of the tables specified"
                                f" in the datasource: {data_table_names}"
                            )
                    kwargs["table_name"] = table

            # Separate handling if we are using a query rather than referencing a table
            elif datastructure.query:
                if isinstance(datastructure.query, dict):
                    if not (
                        sql_query := datastructure.query.get(self._data_identifier)
                    ):
                        raise DataStructureError(
                            f"Query definition not found for"
                            f" {self._data_identifier}."
                            f" Query definitions provided in this DataStructure:"
                            f" {str(datastructure.query)}"
                        )
                elif isinstance(datastructure.query, str):
                    sql_query = datastructure.query
                if sql_query and sqlvalidator.parse(sql_query).is_valid():
                    if not isinstance(self.datasource, DatabaseSource):
                        raise ValueError(
                            "Incompatible DataStructure, data source pair. "
                            "DataStructure is expecting the data source to "
                            "be a DatabaseSource."
                        )
                    kwargs["sql_query"] = sql_query

        # This call loads the data for a multi-table BaseSource as specified by the
        # Modeller/DataStructure.
        self.datasource.load_data(**kwargs)
        if self._pod_db and self.run_on_new_data_only:
            # pod database is incompatible with DatabaseSource,
            # which is the only datasource that supports
            # datastructure queries, so it's safe to assert
            # for the table name
            assert table is not None  # nosec assert_used

            target_table = self.get_pod_db_table_name(table)
            query = self._get_pod_datasource_query()

            self.load_new_records_only_for_task(
                cast(Connection, project_db_con), pod_db_table=target_table, query=query
            )
        return table

    def get_pod_db_table_name(self, base_table_name: str) -> Optional[str]:
        """Calculates the actual table name in the pod DB from a target table name.

        The actual table name will differ depending on if the datasource is
        multitable or not.
        """
        # If we are running a multitable datasource then the table names in
        # the pod_db will be prepended with the datasource name. If it is only
        # a single table datasource then the table name will simply match the
        # datasource name.
        # See Pod._update_pod_db() for more information.
        if isinstance(self.datasource, SQLDataView):
            return None
        else:
            datasource_name = self._data_identifier.split("/")[1]
            if self.datasource.multi_table:
                actual_table_name = f"{datasource_name}_{base_table_name}"
            else:
                if base_table_name != datasource_name and not isinstance(
                    self.datasource, SQLDataView
                ):
                    raise ValueError(
                        f"For single table datasources, the pod DB table name should"
                        f" equal the datasource name;"
                        f" got table={base_table_name}, datasource={datasource_name}"
                    )
                actual_table_name = base_table_name
            return actual_table_name

    def _get_pod_datasource_query(self) -> Optional[str]:
        """Get the query for SQLDataView datasource."""
        if not isinstance(self.datasource, SQLDataView):
            return None
        else:
            return self.datasource._get_updated_query_with_metadata()

    def load_new_records_only_for_task(
        self,
        project_db_con: Connection,
        pod_db_table: Optional[str] = None,
        query: Optional[str] = None,
    ) -> None:
        """Loads only records that the task has not seen before."""
        # Ignoring the security warning because the sql query is trusted and
        # the task_hash is calculated at __init__.
        logger.debug("Loading new records only for task.")
        task_data = pd.read_sql(
            f'SELECT "datapoint_hash" FROM "{self._task_hash}"',  # nosec hardcoded_sql_expressions # noqa: B950
            project_db_con,
        )

        # check hash in from static datasource table -
        pod_db_con = sqlite3.connect(
            f"{self.parent_pod_identifier.split('/')[1]}.sqlite"
        )
        if pod_db_table is not None:
            # Ignoring the security warning because the sql query is trusted and
            # the table is checked that it matches the datasource tables.
            data = pd.read_sql(
                f'SELECT * FROM "{pod_db_table}"',  # nosec hardcoded_sql_expressions
                pod_db_con,
            )
        elif query is not None:
            data = pd.read_sql_query(query, pod_db_con)
        else:
            pod_db_con.close()
            raise PodDBError("Either table name or query needs to be passed.")
        pod_db_con.close()
        # set datasource_data for specific task to only run on new records.
        new_records = data[~data["datapoint_hash"].isin(task_data["datapoint_hash"])]
        if len(new_records) == 0:
            logger.info("No new records to run the tasks on.")
            # TODO: [BIT-2739]

        if "rowID" in new_records.columns:
            new_records.drop(columns=["rowID"], inplace=True)

        if (
            isinstance(self.datasource, FileSystemIterableSource)
            and self.datasource.iterable
        ):
            self.datasource.selected_file_names_override = list(
                new_records["_original_filename"]
            )
        else:
            self.datasource._ignore_cols.append("datapoint_hash")
            self.datasource._data = new_records
