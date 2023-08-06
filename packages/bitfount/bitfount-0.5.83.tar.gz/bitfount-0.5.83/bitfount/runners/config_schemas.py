"""Dataclasses to hold the configuration details for the runners."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
import os
from pathlib import Path
import re
import typing
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    Union,
)

import desert
from marshmallow import ValidationError, fields, validate
from marshmallow.validate import OneOf
from marshmallow_union import Union as M_Union

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _get_environment,
)
from bitfount.data.types import (
    DataPathModifiers,
    SchemaOverrideMapping,
    _ForceStypeValue,
    _SemanticTypeValue,
)
from bitfount.federated.authorisation_checkers import (
    DEFAULT_IDENTITY_VERIFICATION_METHOD,
    IDENTITY_VERIFICATION_METHODS,
)
from bitfount.federated.privacy.differential import DPModellerConfig, DPPodConfig
from bitfount.federated.transport.config import (
    _DEV_MESSAGE_SERVICE_PORT,
    _DEV_MESSAGE_SERVICE_TLS,
    _DEV_MESSAGE_SERVICE_URL,
    _STAGING_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.types import AlgorithmType, ProtocolType
from bitfount.hub.authentication_handlers import _DEFAULT_USERNAME
from bitfount.hub.types import (
    _DEV_AM_URL,
    _DEV_HUB_URL,
    _DEV_IDP_URL,
    _PRODUCTION_IDP_URL,
    _STAGING_AM_URL,
    _STAGING_HUB_URL,
    _STAGING_IDP_URL,
    PRODUCTION_AM_URL,
    PRODUCTION_HUB_URL,
)
from bitfount.models.base_models import (
    EarlyStopping,
    LoggerConfig,
    Optimizer,
    Scheduler,
)
from bitfount.types import _JSONDict

logger = logging.getLogger(__name__)

# POD_NAME_REGEX = re.compile(r"[a-z\d]+(-[a-z\d]+)*")
# USERNAME_REGEX = re.compile(r"[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}")
# TODO: [BIT-1493] revert to regex above to disallow underscores
POD_NAME_REGEX = re.compile(r"[a-z\d]+((-|_)[a-z\d]+)*")
USERNAME_REGEX = re.compile(r"[a-z\d](?:[a-z\d]|(-|_)(?=[a-z\d])){0,38}")


def _deserialize_path(
    path: Optional[str], context: Dict[str, typing.Any]
) -> Optional[Path]:
    """Converts a str into a Path.

    If the input is None, the output is None.

    If the path to the config file is supplied in the `context` dict (in the
    "config_path" key) then any relative paths will be resolved relative to the
    directory containing the config file.
    """
    if path is None:
        return None

    ppath = Path(path)

    # If relative path, use relative to config file if present
    if not ppath.is_absolute() and "config_path" in context:
        config_dir = Path(context["config_path"]).parent
        orig_ppath = ppath
        ppath = config_dir.joinpath(ppath).resolve()
        logger.debug(
            f"Making relative paths relative to {config_dir}: {orig_ppath} -> {ppath}"
        )

    return ppath.expanduser()


def _deserialize_model_ref(ref: str) -> Union[Path, str]:
    """Deserializes a model reference.

    If the reference is a path to a file (and that file exists), return a Path
    instance. Otherwise, returns the str reference unchanged.
    """
    path = Path(ref).expanduser()
    if path.is_file():  # also returns False if path doesn't exist
        return path
    else:
        return ref


# COMMON SCHEMAS
@dataclass
class AccessManagerConfig:
    """Configuration for the access manager."""

    url: str = desert.field(fields.URL(), default=PRODUCTION_AM_URL)


@dataclass
class HubConfig:
    """Configuration for the hub."""

    url: str = desert.field(fields.URL(), default=PRODUCTION_HUB_URL)


@dataclass
class APIKeys:
    """API keys for BitfountSession."""

    access_key_id: str = desert.field(fields.String())
    access_key: str = desert.field(fields.String())


@dataclass
class JWT:
    """Externally managed JWT for BitfountSession."""

    jwt: str = desert.field(fields.String())
    expires: datetime = desert.field(fields.DateTime())
    get_token: Callable[[], Tuple[str, datetime]] = desert.field(fields.Function())


# POD SCHEMAS
@dataclass
class DataSplitConfig:
    """Configuration for the data splitter."""

    data_splitter: str = desert.field(
        fields.String(validate=OneOf(["percentage", "predefined"])),
        default="percentage",
    )
    args: _JSONDict = desert.field(fields.Dict(keys=fields.Str), default_factory=dict)


@dataclass
class PodDataConfig:
    """Configuration for the Schema, BaseSource and Pod.

    Args:
        force_stypes: The semantic types to force for the data. This is passed to the
            `BitfountSchema`. This should be a mapping from pod name to a mapping from
            the type to a list of column names (e.g. {"pod_name": {categorical:
            ["col1", "col2"]}}, or a mapping from each table name in a multitable
            datasource to a mapping from the type to a list of column names (e.g.
            {"table1": {categorical: ["col1", "col2"]}, "table2":  {continuous:
            ["col3", "col4"]}}.
        ignore_cols: The columns to ignore. This is passed to the data source.
        modifiers: The modifiers to apply to the data. This is passed to the
            `BaseSource`.
        datasource_args: Key-value pairs of arguments to pass to the data source
            constructor.
        data_split: The data split configuration. This is passed to the data source.
        auto_tidy: Whether to automatically tidy the data. This is used by the
            `Pod` and will result in removal of NaNs and normalisation of numeric
            values. Defaults to False.
    """

    force_stypes: Optional[
        Mapping[
            str, MutableMapping[Union[_ForceStypeValue, _SemanticTypeValue], List[str]]
        ]
    ] = desert.field(
        fields.Dict(
            keys=fields.String(),
            values=fields.Dict(
                keys=fields.String(validate=OneOf(typing.get_args(_ForceStypeValue))),
                values=fields.List(fields.String()),
            ),
        ),
        default=None,
    )

    ignore_cols: Optional[Mapping[str, List[str]]] = desert.field(
        fields.Dict(keys=fields.String(), values=fields.List(fields.String())),
        default=None,
    )

    modifiers: Optional[Dict[str, DataPathModifiers]] = desert.field(
        fields.Dict(
            keys=fields.Str,
            values=fields.Dict(
                keys=fields.String(
                    validate=OneOf(DataPathModifiers.__annotations__.keys())
                )
            ),
            default=None,
        ),
        default=None,
    )
    datasource_args: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )
    data_split: DataSplitConfig = desert.field(
        fields.Nested(desert.schema_class(DataSplitConfig)),
        default_factory=DataSplitConfig,
    )
    auto_tidy: bool = False


@dataclass
class PodDetailsConfig:
    """Configuration for the pod details.

    Args:
        display_name: The display name of the pod.
        description: The description of the pod.
    """

    display_name: str
    description: str


@dataclass
class DatasourceConfig:
    """Datasouce configuration for a multi-datasource Pod."""

    datasource: str
    data_config: PodDataConfig
    name: Optional[str] = desert.field(
        fields.String(validate=validate.Regexp(POD_NAME_REGEX)), default=None
    )
    datasource_details_config: Optional[PodDetailsConfig] = desert.field(
        fields.Nested(desert.schema_class(PodDetailsConfig)),
        default=None,
    )
    schema: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )


@dataclass
class PodConfig:
    """Full configuration for the pod.

    Raises:
        ValueError: If a username is not provided alongside API keys.
    """

    name: str = desert.field(fields.String(validate=validate.Regexp(POD_NAME_REGEX)))
    secrets: Optional[Union[APIKeys, JWT]] = desert.field(
        M_Union(
            [
                fields.Nested(desert.schema_class(APIKeys)),
                fields.Nested(desert.schema_class(JWT)),
            ]
        ),
        default=None,
    )
    pod_details_config: Optional[PodDetailsConfig] = None
    datasource: Optional[str] = desert.field(fields.String(), default=None)
    data_config: Optional[PodDataConfig] = desert.field(
        fields.Nested(desert.schema_class(PodDataConfig)),
        default=None,
    )
    schema: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )
    datasources: Optional[List[DatasourceConfig]] = desert.field(
        fields.List(fields.Nested(desert.schema_class(DatasourceConfig))),
        default=None,
    )
    access_manager: AccessManagerConfig = desert.field(
        fields.Nested(desert.schema_class(AccessManagerConfig)),
        default_factory=AccessManagerConfig,
    )
    hub: HubConfig = desert.field(
        fields.Nested(desert.schema_class(HubConfig)), default_factory=HubConfig
    )
    message_service: MessageServiceConfig = desert.field(
        fields.Nested(desert.schema_class(MessageServiceConfig)),
        default_factory=MessageServiceConfig,
    )
    differential_privacy: Optional[DPPodConfig] = None
    approved_pods: Optional[List[str]] = None
    username: str = desert.field(
        fields.String(validate=validate.Regexp(USERNAME_REGEX)),
        default=_DEFAULT_USERNAME,
    )
    update_schema: bool = False
    pod_db: bool = False
    show_datapoints_with_results_in_db: bool = True

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            logger.warning(f"{environment=} detected; changing URLs in config")
            self.hub.url = _STAGING_HUB_URL
            self.access_manager.url = _STAGING_AM_URL
            self.message_service.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            logger.warning(
                f"{environment=} detected; changing URLs and ports in config"
            )
            self.hub.url = _DEV_HUB_URL
            self.access_manager.url = _DEV_AM_URL
            self.message_service.url = _DEV_MESSAGE_SERVICE_URL
            self.message_service.port = _DEV_MESSAGE_SERVICE_PORT
            self.message_service.tls = _DEV_MESSAGE_SERVICE_TLS

        # datasource xor datasources must be defined
        if (self.datasource is None) == (self.datasources is None):
            raise ValueError(
                "You must either supply a datasource or a set of datasources"
            )

        # Use API Keys for authentication if provided
        if isinstance(self.secrets, APIKeys):
            if self.username == _DEFAULT_USERNAME:
                raise ValueError("Must specify a username when using API Keys.")

            logger.info("Setting API Keys as environment variables.")

            if os.environ.get("BITFOUNT_API_KEY_ID") or os.environ.get(
                "BITFOUNT_API_KEY"
            ):
                logger.warning(
                    "Existing environment variable API keys detected. Overriding with "
                    "those provided in the pod config."
                )
            os.environ["BITFOUNT_API_KEY_ID"] = self.secrets.access_key_id
            os.environ["BITFOUNT_API_KEY"] = self.secrets.access_key

    @property
    def pod_id(self) -> str:
        """The pod ID of the pod specified."""
        return f"{self.username}/{self.name}"


@dataclass
class PathConfig:
    """Configuration for the path."""

    path: Path = desert.field(fields.Function(deserialize=_deserialize_path))


@dataclass
class DataStructureSelectConfig:
    """Configuration for the datastructure select argument."""

    include: List[str] = desert.field(
        fields.List(fields.String()), default_factory=list
    )
    exclude: List[str] = desert.field(
        fields.List(fields.String()), default_factory=list
    )


@dataclass
class DataStructureAssignConfig:
    """Configuration for the datastructure assign argument."""

    target: Optional[Union[str, List[str]]] = desert.field(
        M_Union([fields.String(), fields.List(fields.String())]), default=None
    )
    image_cols: Optional[List[str]] = None
    loss_weights_col: Optional[str] = None
    multihead_col: Optional[str] = None
    ignore_classes_col: Optional[str] = None


@dataclass
class DataStructureTransformConfig:
    """Configuration for the datastructure transform argument."""

    dataset: Optional[List[Dict[str, _JSONDict]]] = None
    batch: Optional[List[Dict[str, _JSONDict]]] = None
    auto_convert_grayscale_images: bool = True


@dataclass
class DataStructureTableConfig:
    """Configuration for the datastructure table arguments."""

    table: Optional[Union[str, Dict[str, str]]] = desert.field(
        M_Union(
            [
                fields.String(),
                fields.Dict(keys=fields.String(), values=fields.String(), default=None),
            ],
            default=None,
        ),
        default=None,
    )
    query: Optional[Union[str, Dict[str, str]]] = desert.field(
        M_Union(
            [
                fields.String(),
                fields.Dict(keys=fields.String(), values=fields.String(), default=None),
            ],
            default=None,
        ),
        default=None,
    )
    schema_types_override: Optional[
        Union[SchemaOverrideMapping, Mapping[str, SchemaOverrideMapping]]
    ] = desert.field(
        fields.Dict(
            keys=fields.String(),
            values=fields.List(
                M_Union([fields.String(default=None), fields.Dict(default=None)])
            ),
            default=None,
        ),
        default=None,
    )


@dataclass
class DataStructureConfig:
    """Configuration for the modeller schema and dataset options."""

    table_config: DataStructureTableConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureTableConfig)),
    )
    assign: DataStructureAssignConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureAssignConfig)),
        default_factory=DataStructureAssignConfig,
    )
    select: DataStructureSelectConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureSelectConfig)),
        default_factory=DataStructureSelectConfig,
    )
    transform: DataStructureTransformConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureTransformConfig)),
        default_factory=DataStructureTransformConfig,
    )


# MODELLER SCHEMAS
@dataclass
class ModellerUserConfig:
    """Configuration for the modeller.

    Args:
        username: The username of the modeller. This can be picked up automatically
            from the session but can be overridden here.
        identity_verification_method: The method to use for identity verification.
            Accepts one of the values in `IDENTITY_VERIFICATION_METHODS`, i.e. one of
            `key-based`, `saml`, `oidc-auth-code` or `oidc-device-code`.
        private_key_file: The path to the private key file for key-based identity
            verification.
    """

    username: str = desert.field(
        fields.String(validate=validate.Regexp(USERNAME_REGEX)),
        default=_DEFAULT_USERNAME,
    )

    identity_verification_method: str = desert.field(
        fields.String(validate=OneOf(IDENTITY_VERIFICATION_METHODS)),
        default=DEFAULT_IDENTITY_VERIFICATION_METHOD,
    )
    private_key_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )

    def __post_init__(self) -> None:
        environment = _get_environment()
        self._identity_provider_url: str

        if environment == _STAGING_ENVIRONMENT:
            self._identity_provider_url = _STAGING_IDP_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self._identity_provider_url = _DEV_IDP_URL
        else:
            self._identity_provider_url = _PRODUCTION_IDP_URL


@dataclass
class ModellerConfig:
    """Full configuration for the modeller."""

    pods: PodsConfig
    task: TaskConfig
    secrets: Optional[Union[APIKeys, JWT]] = desert.field(
        M_Union(
            [
                fields.Nested(desert.schema_class(APIKeys)),
                fields.Nested(desert.schema_class(JWT)),
            ]
        ),
        default=None,
    )

    modeller: ModellerUserConfig = desert.field(
        fields.Nested(desert.schema_class(ModellerUserConfig)),
        default_factory=ModellerUserConfig,
    )
    hub: HubConfig = desert.field(
        fields.Nested(desert.schema_class(HubConfig)), default_factory=HubConfig
    )
    message_service: MessageServiceConfig = desert.field(
        fields.Nested(desert.schema_class(MessageServiceConfig)),
        default_factory=MessageServiceConfig,
    )
    project_id: Optional[str] = None
    run_on_new_data_only: bool = False
    batched_execution: bool = False

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            self.hub.url = _STAGING_HUB_URL
            self.message_service.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self.hub.url = _DEV_HUB_URL
            self.message_service.url = _DEV_MESSAGE_SERVICE_URL
            self.message_service.port = _DEV_MESSAGE_SERVICE_PORT
            self.message_service.tls = _DEV_MESSAGE_SERVICE_TLS


@dataclass
class ModelStructureConfig:
    """Configuration for the ModelStructure."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )


@dataclass
class BitfountModelReferenceConfig:
    """Configuration for BitfountModelReference."""

    model_ref: Union[Path, str] = desert.field(
        fields.Function(deserialize=_deserialize_model_ref)
    )
    model_version: Optional[int] = None
    username: Optional[str] = None


@dataclass
class ModelConfig:
    """Configuration for the model."""

    # For existing models
    name: Optional[str] = None
    structure: Optional[ModelStructureConfig] = None

    # For custom models
    bitfount_model: Optional[BitfountModelReferenceConfig] = None

    # Other
    hyperparameters: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )
    logger_config: Optional[LoggerConfig] = None
    dp_config: Optional[DPModellerConfig] = None

    def __post_init__(self) -> None:
        # Validate either name or bitfount_model reference provided
        self._name_or_bitfount_model()
        try:
            self.hyperparameters["optimizer"] = Optimizer(
                **self.hyperparameters["optimizer"]
            )
        except KeyError:
            pass
        try:
            self.hyperparameters["early_stopping"] = EarlyStopping(
                **self.hyperparameters["early_stopping"]
            )
        except KeyError:
            pass
        try:
            self.hyperparameters["scheduler"] = Scheduler(
                **self.hyperparameters["scheduler"]
            )
        except KeyError:
            pass

    def _name_or_bitfount_model(self) -> None:
        """Ensures that both `name` and `bitfount_model` can't be set.

        Raises:
            ValidationError: if both `name` and `bitfount_model` are set
        """
        if self.name and self.bitfount_model:
            raise ValidationError("Cannot specify both name and bitfount_model.")
        if not self.name and not self.bitfount_model:
            raise ValidationError("Must specify either name or bitfount_model.")


@dataclass
class PodsConfig:
    """Configuration for the pods to use for the modeller."""

    identifiers: List[str]


@dataclass
class ProtocolConfig:
    """Configuration for the Protocol."""

    name: str
    arguments: Optional[Any] = None

    @classmethod
    def _get_subclasses(cls) -> Tuple[Type[ProtocolConfig], ...]:
        return tuple(cls.__subclasses__())


@dataclass
class AggregatorConfig:
    """Configuration for the Aggregator."""

    secure: bool
    weights: Optional[Dict[str, Union[int, float]]] = None

    def __post_init__(self) -> None:
        if self.secure and self.weights:
            # TODO: [BIT-1486] Remove this constraint
            raise NotImplementedError(
                "SecureAggregation does not support update weighting"
            )


@dataclass
class AlgorithmConfig:
    """Configuration for the Algorithm."""

    name: str
    arguments: Optional[Any] = None

    @classmethod
    def _get_subclasses(cls) -> Tuple[Type[AlgorithmConfig], ...]:
        """Get all the end node subclasses of a class."""
        queue = [cls]
        end_nodes = []
        while queue:
            current_cls = queue.pop()
            if current_cls.__subclasses__():
                queue.extend(current_cls.__subclasses__())
            else:  # end node
                end_nodes.append(current_cls)
        return tuple(end_nodes)


@dataclass
class ModelAlgorithmConfig(AlgorithmConfig):
    """Configuration for the Model algorithms."""

    model: Optional[ModelConfig] = None
    pretrained_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )


# ALGORITHMS
@dataclass
class FederatedModelTrainingArgumentsConfig:
    """Configuration for the FederatedModelTraining algorithm arguments."""

    modeller_checkpointing: bool = True
    checkpoint_filename: Optional[str] = None


@dataclass
class FederatedModelTrainingAlgorithmConfig(ModelAlgorithmConfig):
    """Configuration for the FederatedModelTraining algorithm."""

    name: str = desert.field(
        fields.String(
            validate=validate.Equal(AlgorithmType.FederatedModelTraining.value)
        )
    )
    arguments: Optional[FederatedModelTrainingArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(FederatedModelTrainingArgumentsConfig)),
        default=FederatedModelTrainingArgumentsConfig(),
    )


@dataclass
class ModelTrainingAndEvaluationArgumentsConfig:
    """Configuration for the ModelTrainingAndEvaluation algorithm arguments."""

    # Currently there are no arguments


@dataclass
class ModelTrainingAndEvaluationAlgorithmConfig(ModelAlgorithmConfig):
    """Configuration for the ModelTrainingAndEvaluation algorithm."""

    name: str = desert.field(
        fields.String(
            validate=validate.Equal(AlgorithmType.ModelTrainingAndEvaluation.value)
        )
    )
    arguments: Optional[ModelTrainingAndEvaluationArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(ModelTrainingAndEvaluationArgumentsConfig))
    )


@dataclass
class ModelEvaluationArgumentsConfig:
    """Configuration for the ModelEvaluation algorithm arguments."""

    # Currently there are no arguments


@dataclass
class ModelEvaluationAlgorithmConfig(ModelAlgorithmConfig):
    """Configuration for the ModelEvaluation algorithm."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(AlgorithmType.ModelEvaluation.value))
    )
    arguments: Optional[ModelEvaluationArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(ModelEvaluationArgumentsConfig))
    )


@dataclass
class ModelInferenceArgumentsConfig:
    """Configuration for the ModelInference algorithm arguments."""

    class_outputs: Optional[List[str]] = None


@dataclass
class ModelInferenceAlgorithmConfig(ModelAlgorithmConfig):
    """Configuration for the ModelInference algorithm."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(AlgorithmType.ModelInference.value))
    )
    arguments: ModelInferenceArgumentsConfig = desert.field(
        fields.Nested(desert.schema_class(ModelInferenceArgumentsConfig)),
        default=ModelInferenceArgumentsConfig(),
    )


@dataclass
class ColumnAverageArgumentsConfig:
    """Configuration for the ColumnAverage algorithm arguments."""

    field: str
    table_name: str


@dataclass
class ColumnAverageAlgorithmConfig(AlgorithmConfig):
    """Configuration for the ColumnAverage algorithm."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(AlgorithmType.ColumnAverage.value))
    )

    arguments: ColumnAverageArgumentsConfig = desert.field(
        fields.Nested(desert.schema_class(ColumnAverageArgumentsConfig))
    )


@dataclass
class SqlQueryArgumentsConfig:
    """Configuration for the SqlQuery algorithm arguments."""

    query: str
    table: Optional[str] = None


@dataclass
class SqlQueryAlgorithmConfig(AlgorithmConfig):
    """Configuration for the SqlQuery algorithm."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(AlgorithmType.SqlQuery.value))
    )
    arguments: SqlQueryArgumentsConfig = desert.field(
        fields.Nested(desert.schema_class(SqlQueryArgumentsConfig))
    )


@dataclass
class PrivateSqlQueryArgumentsConfig:
    """Configuration for the PrivateSqlQuery algorithm arguments."""

    query: str
    epsilon: float
    delta: float
    column_ranges: Dict[str, Dict[str, int]]
    table: Optional[str] = None
    db_schema: Optional[str] = None


@dataclass
class PrivateSqlQueryAlgorithmConfig(AlgorithmConfig):
    """Configuration for the PrivateSqlQuery algorithm."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(AlgorithmType.PrivateSqlQuery.value))
    )
    arguments: PrivateSqlQueryArgumentsConfig = desert.field(
        fields.Nested(desert.schema_class(PrivateSqlQueryArgumentsConfig))
    )


@dataclass
class ComputeIntersectionRSAArgumentsConfig:
    """Configuration for the ComputeIntersectionRSA algorithm arguments."""

    # Currently there are no arguments


@dataclass
class ComputeIntersectionRSAAlgorithmConfig(AlgorithmConfig):
    """Configuration for the ComputeIntersectionRSA algorithm."""

    name: str = desert.field(
        fields.String(
            validate=validate.Equal(AlgorithmType.ComputeIntersectionRSA.value)
        )
    )

    arguments: Optional[ComputeIntersectionRSAArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(ComputeIntersectionRSAArgumentsConfig))
    )


@dataclass
class GenericAlgorithmConfig(AlgorithmConfig):
    """Configuration for unspecified algorithm plugins."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )


# Protocols
@dataclass
class PrivateSetIntersectionArgumentsConfig:
    """Configuration for the PSI Protocol arguments."""

    # TODO: [BIT-2912] investigate why the datasource is optional.
    datasource: Optional[DatasourceConfig] = None
    datasource_columns: Optional[List[str]] = None
    datasource_table: Optional[str] = None
    pod_columns: Optional[List[str]] = None
    pod_table: Optional[str] = None
    # TODO: [BIT-2905] remove aggregator from PSI config
    aggregator: Optional[AggregatorConfig] = None


@dataclass
class PrivateSetIntersectionProtocolConfig(ProtocolConfig):
    """Configuration for the PSI Protocol."""

    name: str = desert.field(
        fields.String(
            validate=validate.Equal(ProtocolType.PrivateSetIntersection.value)
        )
    )
    arguments: Optional[PrivateSetIntersectionArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(PrivateSetIntersectionArgumentsConfig)),
        default=PrivateSetIntersectionArgumentsConfig(),
    )


@dataclass
class ResultsOnlyProtocolArgumentsConfig:
    """Configuration for the ResultsOnly Protocol arguments."""

    aggregator: Optional[AggregatorConfig] = None
    secure_aggregation: bool = False


@dataclass
class ResultsOnlyProtocolConfig(ProtocolConfig):
    """Configuration for the ResultsOnly Protocol."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(ProtocolType.ResultsOnly.value))
    )
    arguments: Optional[ResultsOnlyProtocolArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(ResultsOnlyProtocolArgumentsConfig)),
        default=ResultsOnlyProtocolArgumentsConfig(),
    )


@dataclass
class FederatedAveragingProtocolArgumentsConfig:
    """Configuration for the FedreatedAveraging Protocol arguments."""

    aggregator: Optional[AggregatorConfig] = None
    steps_between_parameter_updates: Optional[int] = None
    epochs_between_parameter_updates: Optional[int] = None
    auto_eval: bool = True
    secure_aggregation: bool = False


@dataclass
class FederatedAveragingProtocolConfig(ProtocolConfig):
    """Configuration for the FederatedAveraging Protocol."""

    name: str = desert.field(
        fields.String(validate=validate.Equal(ProtocolType.FederatedAveraging.value))
    )
    arguments: Optional[FederatedAveragingProtocolArgumentsConfig] = desert.field(
        fields.Nested(desert.schema_class(FederatedAveragingProtocolArgumentsConfig)),
        default=FederatedAveragingProtocolArgumentsConfig(),
    )


@dataclass
class GenericProtocolConfig(ProtocolConfig):
    """Configuration for unspecified protocol plugins."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )


@dataclass
class TaskConfig:
    """Configuration for the task."""

    protocol: Union[ProtocolConfig._get_subclasses()]  # type: ignore[valid-type] # reason: no dynamic typing # noqa: B950
    algorithm: Union[  # type: ignore[valid-type] # reason: same as above
        Union[AlgorithmConfig._get_subclasses()],
        List[Union[AlgorithmConfig._get_subclasses()]],
    ]
    data_structure: Optional[DataStructureConfig] = None
    aggregator: Optional[AggregatorConfig] = None
    transformation_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )
