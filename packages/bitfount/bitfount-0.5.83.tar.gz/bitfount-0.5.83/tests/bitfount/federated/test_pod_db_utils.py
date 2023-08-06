"""Tests pod_db_utils.py."""
import hashlib
import json
import os
from pathlib import Path
import platform
import sqlite3
from typing import Generator, cast
from unittest.mock import Mock

import numpy as np
import pandas as pd
from pandas.errors import DatabaseError
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.dicom_source import DICOMSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.federated.exceptions import PodDBError
from bitfount.federated.pod_db_utils import (
    _SQL_TYPES,
    _add_file_iterable_datasource_to_db,
    _add_single_record_to_db,
    _map_task_to_hash_add_to_db,
    _save_results_to_db,
    _sql_type_name,
    _update_single_record_in_db,
)
from bitfount.types import _JSONDict
from tests.utils import PytestRequest
from tests.utils.helper import create_datasource, unit_test

POD_NAME = "testpod"
POD_IDENTIFIER = f"user/{POD_NAME}"


@unit_test
@pytest.mark.skipif(
    condition=platform.system() == "Windows",
    reason=(
        "Only works intermittently on Windows. "
        "Connection to database not always closed properly,"
        "leading to PermissionError."
    ),
)
class TestPodDBUtils:
    """Tests functions from pod_db_utils.py."""

    @fixture
    def serialized_protocol_with_model(self) -> _JSONDict:
        """Serialized protocol dict with model (and aggregator)."""
        return {
            "algorithm": {
                "class_name": "alg",
                "model": {
                    "class_name": "model",
                    "schema": "mock_schema",
                    "datastructure": {"table": POD_NAME},
                },
            },
            "aggregator": {"class_name": "aggregator"},
            "class_name": "FederatedAveraging",
        }

    @fixture
    def con(self) -> Generator[sqlite3.Connection, None, None]:
        """Yields a connection to a test SQLite database.

        Closes the connection and deletes the database after the test.
        """
        db_name = f"{POD_NAME}.sqlite"
        if os.path.exists(db_name):
            os.remove(db_name)
        con = sqlite3.connect(db_name)
        yield con
        con.close()
        os.remove(db_name)

    def dicom_files_2d(self, tmp_path: Path, filename: str = "dicom_file") -> None:
        """Generates five 2d dicom files for testing."""
        for i in range(5):
            filepath = tmp_path / f"{filename}_{i}.dcm"
            pixel_arr = np.random.randint(0, 255, (100, 100))
            file_meta = FileMetaDataset()
            ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
            ds.PatientName = f"Patient {i}"
            ds.PatientID = f"ID {i}"
            ds.StudyDate = "20200101"
            ds.StudyTime = f"{i}"
            ds.StudyDescription = "Test"
            ds.PixelData = pixel_arr.tobytes()
            ds.NumberOfFrames = "1"
            ds.BitsAllocated = 8
            ds.SamplesPerPixel = 1
            ds.Rows = 100
            ds.Columns = 100
            ds.PhotometricInterpretation = "RGB"
            ds.PixelRepresentation = 0
            ds.BitsStored = 8
            ds.file_meta = FileMetaDataset()
            ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian  # type: ignore[attr-defined] # Reason: pydicom has that attr and we only use it for testing. # noqa: B950
            ds.is_little_endian = False
            ds.is_implicit_VR = False
            ds.save_as(filepath)

    @fixture
    def datasource(self, request: PytestRequest, tmp_path: Path) -> BaseSource:
        """Returns an optionally iterable datasource.

        Args:
            request: Should be one of "dicom", "dicom_iterable" or "basic".

        Returns:
            The DataSource object.
        """
        datasource: BaseSource
        if "dicom" in request.param:
            self.dicom_files_2d(tmp_path)
            iterable = bool("iterable" in request.param)
            datasource = DICOMSource(
                path=tmp_path,
                output_path=tmp_path,
                iterable=iterable,
                # 3 of the 5 values are part of the test set
                data_splitter=PercentageSplitter(40, 60),
            )
            datasource.load_data()
            # Remove apostrophe from column name because the database can't handle it
            datasource.data.rename(
                columns={"Patient's Name": "Patient Name"}, inplace=True
            )
            datasource.data["Patient Name"] = datasource.data["Patient Name"].apply(
                lambda x: str(x)
            )
            datasource.data["Pixel Data 0"] = datasource.data["Pixel Data 0"].apply(
                lambda x: str(x)
            )
            if not iterable:
                datasource._test_idxs = np.array([0, 1, 2])

        else:
            datasource = create_datasource(classification=True)
            datasource._ignore_cols = ["Date"]
            datasource._test_idxs = np.array([234, 21, 19])
            datasource.load_data()

        return datasource

    @pytest.mark.parametrize(
        "datasource", ["dicom", "dicom_iterable", "basic"], indirect=True
    )
    def test_sql_type_name(self, datasource: BaseSource) -> None:
        """Tests _sql_type_name returns a SQLite appropriate dtype."""
        for col in datasource.data.columns:
            dtype = _sql_type_name(datasource.data[col])
            assert dtype in _SQL_TYPES.values()

    def test_worker_map_task_to_hash_multiple_algo(
        self, con: sqlite3.Connection, serialized_protocol_with_model: _JSONDict
    ) -> None:
        """Tests that mapping task to hash works as expected."""
        task_hash = hashlib.sha256(
            json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
        ).hexdigest()
        _map_task_to_hash_add_to_db(serialized_protocol_with_model, task_hash, con)  # type: ignore[arg-type] # reason: testing purposes only # noqa: B950
        task_defs = pd.read_sql("SELECT * FROM 'task_definitions' ", con)
        assert sorted(set(task_defs.columns)) == [
            "algorithm",
            "index",
            "protocol",
            "taskhash",
        ]
        assert task_hash in task_defs["taskhash"].values

    @pytest.mark.parametrize(
        "datasource", ["dicom", "dicom_iterable", "basic"], indirect=True
    )
    @pytest.mark.parametrize("run_on_new_data_only", [True, False])
    @pytest.mark.parametrize("show_datapoints_in_results_db", [True, False])
    def test_save_results_to_db(
        self,
        con: sqlite3.Connection,
        datasource: BaseSource,
        run_on_new_data_only: bool,
        serialized_protocol_with_model: _JSONDict,
        show_datapoints_in_results_db: bool,
    ) -> None:
        """Tests that only results are saved to db."""
        task_hash = hashlib.sha256(
            json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
        ).hexdigest()
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}"
            ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""
        )
        new_data = datasource._data.copy()
        hashed_list = []
        for _, row in new_data.iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
        for col in new_data.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(new_data[col])}"  # noqa: B950
            )
        con.commit()
        new_data["datapoint_hash"] = hashed_list
        new_data.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        serialized_protocol_with_model["algorithm"] = [
            serialized_protocol_with_model["algorithm"]
        ]

        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{task_hash}"
            (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""
        )

        _save_results_to_db(
            results=[np.array([1]), np.array([2]), np.array([3])],
            pod_identifier=POD_IDENTIFIER,
            datasource=datasource,
            show_datapoints_in_results_db=show_datapoints_in_results_db,
            run_on_new_data_only=run_on_new_data_only,
            task_hash=task_hash,
            project_db_con=con,
            table=POD_NAME,
        )
        task_data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
        if show_datapoints_in_results_db:
            # The DICOMSource has a different number of columns to the DataFrameSource
            if isinstance(datasource, DICOMSource):
                # 3 rows corresponding to the test_idxs,
                # 15 datasource_cols + 3 columns (rowID, datapoint_hash, result)
                assert task_data.shape == (3, 19)
            else:
                # 3 rows corresponding to the test_idxs,
                # 17 datasource_cols + 3 columns (rowID, datapoint_hash, result)
                assert task_data.shape == (3, 20)
        else:
            # 3 rows corresponding to the test_idxs,
            # 3 columns (rowID, datapoint_hash, result)
            assert task_data.shape == (3, 3)

    @pytest.mark.parametrize(
        "datasource", ["dicom", "dicom_iterable", "basic"], indirect=True
    )
    @pytest.mark.parametrize("run_on_new_data_only", [True, False])
    @pytest.mark.parametrize("show_datapoints_in_results_db", [True, False])
    def test_save_results_to_db_does_not_save_duplicated_results(
        self,
        con: sqlite3.Connection,
        datasource: BaseSource,
        run_on_new_data_only: bool,
        serialized_protocol_with_model: _JSONDict,
        show_datapoints_in_results_db: bool,
    ) -> None:
        """Tests that only results that are not already in the db are saved to db."""
        task_hash = hashlib.sha256(
            json.dumps(serialized_protocol_with_model, sort_keys=True).encode("utf-8")
        ).hexdigest()
        cur = con.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{POD_NAME}"
            ('rowID' INTEGER PRIMARY KEY, 'datapoint_hash' TEXT)"""
        )
        new_data = datasource._data.copy()
        hashed_list = []
        for _, row in new_data.iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
        for col in new_data.columns:
            cur.execute(
                f"ALTER TABLE '{POD_NAME}' ADD COLUMN '{col}' {_sql_type_name(new_data[col])}"  # noqa: B950
            )
        new_data["datapoint_hash"] = hashed_list
        new_data.to_sql(POD_NAME, con=con, if_exists="append", index=False)
        con.commit()
        serialized_protocol_with_model["algorithm"] = [
            serialized_protocol_with_model["algorithm"]
        ]

        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{task_hash}"
            (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""
        )

        # We run the task twice and the results should not be duplicated
        # so we make the same assertions both times
        for _ in range(2):
            _save_results_to_db(
                results=[np.array([1]), np.array([2]), np.array([3])],
                pod_identifier=POD_IDENTIFIER,
                datasource=datasource,
                show_datapoints_in_results_db=show_datapoints_in_results_db,
                run_on_new_data_only=run_on_new_data_only,
                task_hash=task_hash,
                project_db_con=con,
                table=POD_NAME,
            )
            task_data = pd.read_sql(f"SELECT * FROM '{task_hash}' ", con)
            if show_datapoints_in_results_db:
                # The DICOMSource has a different number of columns to the
                # DataFrameSource
                if isinstance(datasource, DICOMSource):
                    # 3 rows corresponding to the test_idxs,
                    # 15 datasource_cols + 3 columns (rowID, datapoint_hash, result)
                    assert task_data.shape == (3, 19)
                else:
                    # 3 rows corresponding to the test_idxs,
                    # 17 datasource_cols + 3 columns (rowID, datapoint_hash, result)
                    assert task_data.shape == (3, 20)
            else:
                # 3 rows corresponding to the test_idxs,
                # 3 columns (rowID, datapoint_hash, result)
                assert task_data.shape == (3, 3)

    def test__save_results_to_db_error_no_table_no_query(self) -> None:
        """Tests that error is raised when no table or query is passed."""
        with pytest.raises(PodDBError):
            _save_results_to_db(
                results=[np.array([1]), np.array([2]), np.array([3])],
                pod_identifier=POD_IDENTIFIER,
                datasource=Mock(),
                show_datapoints_in_results_db=False,
                run_on_new_data_only=False,
                task_hash=" ",
                project_db_con=Mock(),
            )

    @pytest.mark.parametrize("datasource", ["dicom", "dicom_iterable"], indirect=True)
    def test__add_fileiterable_data_to_pod_db(
        self,
        con: sqlite3.Connection,
        datasource: BaseSource,
        mocker: MockerFixture,
    ) -> None:
        """Test adding file-iterable datasource to pod_db."""
        # we only test for dicom source so it's safe to cast
        datasource = cast(DICOMSource, datasource)
        table_name = "testtable"
        _add_file_iterable_datasource_to_db(
            pod_name=POD_NAME, datasource=datasource, table_name=table_name
        )
        pod_con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cur.fetchall()]
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        assert table_name in tables
        assert data.shape == (5, 18)
        mock_get_data = mocker.patch.object(datasource, "_get_data")
        mock_get_data.return_value = datasource.data.iloc[[0]]
        # Do second run as well:
        _add_file_iterable_datasource_to_db(
            pod_name=POD_NAME, datasource=datasource, table_name=table_name
        )
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        # Check that the number of records is unchanged.
        assert data.shape == (5, 18)

    @pytest.mark.parametrize("datasource", ["dicom", "dicom_iterable"], indirect=True)
    def test__add_fileiterable_data_to_pod_db_new_record(
        self,
        con: sqlite3.Connection,
        datasource: BaseSource,
        mocker: MockerFixture,
    ) -> None:
        """Test adding file-iterable datasource to pod_db."""
        # we only test for dicom source so it's safe to cast
        datasource = cast(DICOMSource, datasource)
        table_name = "testtable"
        _add_file_iterable_datasource_to_db(
            pod_name=POD_NAME, datasource=datasource, table_name=table_name
        )
        pod_con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cur.fetchall()]
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        assert table_name in tables
        assert data.shape == (5, 18)
        # Remove a row from db
        cur.execute(f"DELETE FROM '{table_name}' WHERE rowID=1;")
        con.commit()
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        assert data.shape == (4, 18)
        assert any(data["rowID"] != 1)
        mock_get_data = mocker.patch.object(datasource, "_get_data")
        mock_get_data.return_value = datasource.data.iloc[[0]]
        # Do second run as well:
        _add_file_iterable_datasource_to_db(
            pod_name=POD_NAME, datasource=datasource, table_name=table_name
        )
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        # Check that the number of records is unchanged.
        assert data.shape == (5, 18)

    @pytest.mark.parametrize("datasource", ["dicom", "dicom_iterable"], indirect=True)
    def test__add_fileiterable_data_to_pod_db_duplicate_record(
        self,
        con: sqlite3.Connection,
        datasource: BaseSource,
        mocker: MockerFixture,
    ) -> None:
        """Test adding file-iterable datasource to pod_db."""
        # we only test for dicom source so it's safe to cast
        datasource = cast(DICOMSource, datasource)
        table_name = "testtable"
        _add_file_iterable_datasource_to_db(
            pod_name=POD_NAME, datasource=datasource, table_name=table_name
        )
        pod_con = sqlite3.connect(f"{POD_NAME}.sqlite")
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cur.fetchall()]
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        assert table_name in tables
        assert data.shape == (5, 18)
        # Duplicate rows in the db.
        data["rowID"] = [6, 7, 8, 9, 10]
        data = data.set_index("rowID")
        data.to_sql(table_name, pod_con, if_exists="append")
        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        assert data.shape == (10, 18)
        mock_add_data = mocker.patch(
            "bitfount.federated.pod_db_utils._add_data_to_pod_db"
        )

        data = pd.read_sql(f"SELECT * FROM '{table_name}'", pod_con)
        assert data.shape == (10, 18)
        mocker.patch.object(datasource, "_get_data", return_value=datasource.data)
        # Do second run as well:
        _add_file_iterable_datasource_to_db(
            pod_name=POD_NAME, datasource=datasource, table_name=table_name
        )
        mock_add_data.assert_called_once()

    def test__add_update_single_record_to_pod_db(
        self, con: sqlite3.Connection, tmp_path: Path
    ) -> None:
        """Test _add_single_record_to_db and _update_single_record_in_db."""
        self.dicom_files_2d(tmp_path)
        datasource = DICOMSource(
            path=tmp_path,
            output_path=tmp_path,
            # 3 of the 5 values are part of the test set
            data_splitter=PercentageSplitter(40, 60),
        )
        filepath = tmp_path / "dicom_file_1.dcm"

        # Check db is empty before adding record
        with pytest.raises(DatabaseError):
            pd.read_sql("SELECT * FROM 'test'", con)

        df = datasource._get_data(file_names=[str(filepath)])
        df["_original_filename"] = "bla"
        df["rowID"] = 1  # row id normally gets added in _add_data_to_pod_db
        assert "Patient's Name" in df.columns
        _add_single_record_to_db(df, "test", con)
        data = pd.read_sql("SELECT * FROM 'test'", con)
        assert df.shape == data.shape
        assert "Patient`s Name" in data.columns
        assert df["_original_filename"].iloc[0] == data["_original_filename"].iloc[0]
        df["_original_filename"] = "bla2"
        _update_single_record_in_db(
            updated_record=df,
            original_record=data.iloc[0],
            table_name="test",
            con=con,
            cur=con.cursor(),
        )
        data = pd.read_sql("SELECT * FROM 'test'", con)
        assert data["_original_filename"].iloc[0] == "bla2"
