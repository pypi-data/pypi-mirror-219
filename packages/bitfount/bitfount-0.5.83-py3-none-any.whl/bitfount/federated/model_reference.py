"""References to custom models."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Optional, Type, Union, cast

from marshmallow import fields

from bitfount.data.datastructure import (
    DataStructure,
    registry as datastructure_registry,
)
from bitfount.data.schema import BitfountSchema
from bitfount.federated.logging import _get_federated_logger
from bitfount.hub.exceptions import ModelUploadError
from bitfount.hub.helper import _default_bitfounthub
from bitfount.hub.utils import hash_file_contents
from bitfount.models.base_models import _BaseModelRegistryMixIn
from bitfount.types import (
    T_FIELDS_DICT,
    T_NESTED_FIELDS,
    DistributedModelProtocol,
    _BaseSerializableObjectMixIn,
    _StrAnyDict,
)
from bitfount.utils import (
    _get_non_abstract_classes_from_module,
    _handle_fatal_error,
    delegates,
)

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub
    from bitfount.hub.types import _ModelUploadResponseJSON
    from bitfount.models.bitfount_model import BitfountModel
    from bitfount.runners.config_schemas import JWT, APIKeys

logger = _get_federated_logger(__name__)


@delegates()
class BitfountModelReference(_BaseModelRegistryMixIn, _BaseSerializableObjectMixIn):
    """Describes a local or remote reference to a `BitfountModel` class.

    :::tip

    To use another user's custom model, simply provide that user's username instead of
    your own (along with the name of the model as the `model_ref` argument).

    :::

    Args:
        model_ref: Either path to model file or name of model on hub.
        datastructure: `DataStructure` to be passed to the model when initialised. This
            is an optional argument as it is only required for `get_model` to perform
            validation on the model before uploading it to the hub. Ensure that you
            provide this argument if you want to use `get_model` to upload your model.
        model_version: The version of the model you wish to use. Defaults to
            the latest version.
        schema: The `BitfountSchema` object associated with the datasource
            on which the model will be trained on.
        username: The username of the model owner. Defaults to bitfount session username
            if not provided.
        hub: Required for upload/download of model. This attribute is set after
            initialisation on the worker side as the hub is not serialized. Defaults to
            None.
        hyperparameters: Hyperparameters to be passed to the model constructor after it
            has been loaded from file or hub. Defaults to None.
        private: Boolean flag to set the model to be private to control useage or
            publicly accessible to all users.
        new_version: Whether to upload a new version of the model to the hub.
            Defaults to False.
        secrets: The secrets to use when creating a `BitfountHub` instance. Defaults to
            None.

    Raises:
        ValueError: If `username` is not provided and `hub` is not provided.
    """

    datastructure: DataStructure
    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_ref": fields.Method(
            serialize="get_model_ref", deserialize="load_model_ref"
        ),
        "model_version": fields.Int(allow_none=True),
        # The hub should not be serialized but can be deserialized if provided
        "hub": fields.Raw(allow_none=True, load_only=True),
        "username": fields.Str(allow_none=True),
        "hyperparameters": fields.Dict(keys=fields.Str()),
        "param_clipping": fields.Dict(
            keys=fields.String(), values=fields.Integer(), allow_none=True
        ),
        "schema": fields.Nested(BitfountSchema._Schema),
        "private": fields.Bool(allow_none=True),
        "new_version": fields.Bool(allow_none=True),
    }
    # TODO: [BIT-1954] Maybe this should actually fall under the hyperparameters
    #  rather than populating the top level with additional fields. Or at least
    #  a `other_kwargs` (terrible name, don't use that) so that we can add more
    #  to it in the future.
    nested_fields: ClassVar[T_NESTED_FIELDS] = {"datastructure": datastructure_registry}

    def __init__(
        self,
        model_ref: Union[Path, str],
        datastructure: Optional[DataStructure] = None,
        model_version: Optional[int] = None,
        schema: Optional[BitfountSchema] = None,
        username: Optional[str] = None,
        hub: Optional[BitfountHub] = None,
        hyperparameters: Optional[_StrAnyDict] = None,
        private: bool = False,
        new_version: bool = False,
        secrets: Optional[Union[APIKeys, JWT]] = None,
    ):
        self.class_name = type(self).__name__
        self.model_ref = model_ref
        self.model_version = model_version
        self.schema = schema if schema else BitfountSchema()
        self.hub = _default_bitfounthub(hub, username=username, secrets=secrets)
        self.hyperparameters = hyperparameters if hyperparameters is not None else {}
        self.username = username or self.hub.username
        self.private = private
        self.new_version = new_version
        if datastructure:
            self.datastructure = datastructure

    def _get_model_from_path(self) -> Type[BitfountModel]:
        """Returns model class from path.

        Returns:
            The model class.
        """
        self.model_ref = cast(Path, self.model_ref)
        return _get_non_abstract_classes_from_module(self.model_ref)[
            self.model_ref.stem
        ]

    def _upload_model_to_hub(self) -> Optional[_ModelUploadResponseJSON]:
        """Uploads model to hub under the logged-in user's account."""
        # model_ref is path to model code file
        self.model_ref = cast(Path, self.model_ref)
        try:
            response = self.hub.send_model(self.model_ref, self.private)
            logger.info("Model has been uploaded to the hub.")
            return response
        except ModelUploadError as ex:
            _handle_fatal_error(ex)

    def _get_model_from_hub(
        self, project_id: Optional[str] = None
    ) -> Type[BitfountModel]:
        """Returns model class from hub from user denoted by `self.username`.

        Returns:
            The model class.
        """
        # model_ref is the name of a model on the hub
        self.model_ref = cast(str, self.model_ref)
        model_cls = self.hub.get_model(
            self.username, self.model_ref, self.model_version, project_id
        )

        # Check that the model has been retrieved correctly
        if not model_cls:
            raise ValueError(
                "Unable to retrieve model from hub, check logs for details."
            )
        return model_cls

    def get_weights(self, project_id: Optional[str] = None) -> Optional[bytes]:
        """Gets weights file uploaded for the model if one exists.

        Returns:
            The weights file as a byte stream.
        """
        if isinstance(self.model_ref, Path):
            raise TypeError(
                "Invalid model reference. get_weights can only be"
                "called on uploaded models and you have specified "
                f"a Path as model_ref: {self.model_ref}."
            )
        if not self.model_version:
            raise ValueError(
                "You must specify model_version in BitfountModelReference "
                "constructor to get model weights file."
            )
        return self.hub.get_weights(
            self.username, self.model_ref, self.model_version, project_id
        )

    def get_model(self, project_id: Optional[str] = None) -> Type[BitfountModel]:
        """Gets the model referenced.

        If the model is a Path to a `BitfountModel`, it will upload it to BitfountHub
        and return the model class. If it is a name of a model on the hub, it will
        download the model from the hub and return the model class.

        Returns:
            The model class.

        Raises:
            TypeError: If the model is not a Path or a string.
            TypeError: If the model does not implement `DistributedModelProtocol`.
            ValueError: If a `BitfountHub` instance has not been provided or if there
                was a communication error with the hub.
            ValueError: If a datastructure has not been provided.
        """
        if isinstance(self.model_ref, Path):
            model_cls = self._get_model_from_path()
            hash = hash_file_contents(self.model_ref)

            # Check that chosen model is compatible with federation by checking if it
            # implements `DistributedModelProtocol`. The only way to do this is to
            # instantiate the model and perform an `isinstance` check.
            if self.datastructure is None:
                raise ValueError(
                    "Datastructure must be provided to instantiate model "
                    "so that the type of the model can be validated."
                )
            model = model_cls(
                datastructure=self.datastructure,
                schema=self.schema,
                **self.hyperparameters,
            )
            if not isinstance(model, DistributedModelProtocol):
                raise TypeError(
                    f"Model {self.model_ref.stem} does not implement "
                    f"DistributedModelProtocol."
                )
            # Try to get the given (or latest if not provided)
            # model version from the hub
            model_response = self.hub._get_model_response(
                username=self.username,
                model_name=self.model_ref.stem,
                model_version=self.model_version,
            )

            # Check hash of the last or given version before uploading,
            # and only upload new version if they are different.
            # Also upload model if new_version is `True`
            if (
                model_response is None
                or model_response["modelHash"] != hash
                or self.new_version
            ):
                self._upload_model_to_hub()

            # self.model_ref is set to the name of the model so that the model doesn't
            # get unnecessarily re-uploaded if `get_model` is called multiple times
            self.model_ref = self.model_ref.stem
        elif isinstance(self.model_ref, str):
            model_cls = self._get_model_from_hub(project_id=project_id)
        else:
            raise TypeError(f"Model of type {type(self.model_ref)} not recognised.")

        return model_cls

    def send_weights(self, pretrained_file: Union[Path, str]) -> None:
        """Sends the model weights from a pretrained file to Hub.

        Args:
            pretrained_file: The path to the pretrained model file.

        Raises:
            ValueError: If `model_version` has not been set on BitfountModelReference
            instance.
        """
        if isinstance(self.model_ref, Path):
            model_name = self.model_ref.stem
        else:
            model_name = self.model_ref
        if not self.model_version:
            raise ValueError(
                "You must specify model_version in BitfountModelReference "
                "constructor to upload model weights file."
            )
        if isinstance(pretrained_file, str):
            pretrained_file = Path(pretrained_file)
        return self.hub.send_weights(model_name, self.model_version, pretrained_file)
