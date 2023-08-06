"""Custom exceptions for the hub package."""
from bitfount.exceptions import BitfountError


class AuthenticatedUserError(BitfountError, ValueError):
    """Error related to user authentication."""

    pass


class PodDoesNotExistError(BitfountError):
    """Errors related to references to a non-existent Pod."""

    pass


class SchemaUploadError(BitfountError, ValueError):
    """Could not upload schema to hub."""

    pass


class ModelUploadError(BitfountError):
    """Error occurred whilst uploading model to hub."""

    pass


class ModelValidationError(ModelUploadError):
    """Error occurred in validating model format."""

    pass


class ModelTooLargeError(ModelUploadError, ValueError):
    """The model is too large to upload to the hub."""

    pass
