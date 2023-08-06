"""Types for hub-related code."""
from typing import Dict, Final, List, Literal, TypedDict, Union

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from typing_extensions import NotRequired

from bitfount.federated.monitoring.types import ProgressCounterDict
from bitfount.federated.types import SerializedProtocol
from bitfount.types import (
    _JSONDict,
    _S3PresignedPOSTFields,
    _S3PresignedPOSTURL,
    _S3PresignedURL,
)

# Hub/AM URLs
PRODUCTION_HUB_URL: Final[str] = "https://hub.bitfount.com"
PRODUCTION_AM_URL: Final[str] = "https://am.hub.bitfount.com"
_STAGING_HUB_URL: Final[str] = "https://hub.staging.bitfount.com"
_STAGING_AM_URL: Final[str] = "https://am.hub.staging.bitfount.com"
_DEV_HUB_URL: Final[str] = "http://localhost:3000"
_DEV_AM_URL: Final[str] = "http://localhost:3001"

# IDP URLs
_PRODUCTION_IDP_URL: Final[str] = (
    "https://prod-bitfount.eu.auth0.com/"
    "samlp/8iCJ33Kp6hc9ofrXTzr5GLxMRHWrlzZO?SAMLRequest="
)
_STAGING_IDP_URL: Final[str] = (
    "https://dev-bitfount.eu.auth0.com/"
    "samlp/Wk4XZHDKfY8F3OYcKdagIHETt6JYwX08?SAMLRequest="
)
_DEV_IDP_URL: Final[str] = (
    "https://dev-bitfount.eu.auth0.com/"
    "samlp/MP8oao6gcJd4jARwzJiJlEiK59ZeLCt3?SAMLRequest="
)


# General JSONs
class _HubSuccessResponseJSON(TypedDict):
    """Generic hub success response JSON."""

    success: Literal[True]
    message: str


class _HubFailureResponseJSON(TypedDict):
    """Generic hub failure response JSON."""

    success: Literal[False]
    errorMessage: str


_HubResponseJSON = Union[_HubSuccessResponseJSON, _HubFailureResponseJSON]


# Hub-related JSON.
class _PodDetailsResponseJSON(TypedDict):
    """Response JSON from GET /api/pods/[userName]/[podName]."""

    podIdentifier: str
    podName: str
    podDisplayName: str
    podPublicKey: str
    accessManagerPublicKey: str
    description: str
    # dataSchema: str  # present but should not be used
    schemaStorageKey: str
    isOnline: bool
    providerUserName: str
    visibility: Literal["public", "private"]
    schemaDownloadUrl: _S3PresignedURL


class _MultiPodDetailsResponseJSON(TypedDict):
    """Response JSON from GET /api/pods."""

    podIdentifier: str
    name: str
    podDisplayName: str
    isOnline: bool
    podPublicKey: str
    accessManagerPublicKey: str
    description: str
    providerUserName: str
    podPagePath: str


class _PodRegistrationResponseJSON(TypedDict):
    """Response JSON from POST /api/pods."""

    success: bool
    alreadyExisted: bool
    message: str
    uploadUrl: _S3PresignedPOSTURL
    uploadFields: _S3PresignedPOSTFields


class _PodRegistrationFailureJSON(TypedDict):
    """Failure response JSON from POST /api/pods."""

    success: Literal[False]
    alreadyExisted: bool
    errorMessage: str


class _ModelDetailsResponseJSON(TypedDict):
    """Response JSON from GET /api/models when getting specific model."""

    modelDownloadUrl: _S3PresignedURL
    modelHash: str
    weightsDownloadUrl: NotRequired[_S3PresignedURL]
    modelVersion: int


class _MultiModelDetailsResponseJSON(TypedDict):
    """Response JSON from GET /api/models when getting all models."""

    modellerName: str
    modelName: str
    modelStorageKey: str
    modelVersion: int


class _ModelUploadResponseJSON(TypedDict):
    """Response JSON from POST /api/models."""

    # This is not a 1-to-1 mapping with the actual return types (i.e. some are
    # only returned on success, some only on failure), but is enough for our
    # use case.
    uploadUrl: _S3PresignedPOSTURL
    uploadFields: _S3PresignedPOSTFields
    success: bool
    alreadyExisted: bool
    version: int
    errorMessage: NotRequired[str]


class _MonitorPostJSON(TypedDict):
    """Form of the JSON object for sending to the task monitoring service."""

    taskId: str
    senderId: str
    recipientId: NotRequired[str]
    timestamp: str  # ISO 8601 format timestamp
    privacy: str  # one of monitoring.MonitorRecordPrivacy's values
    # one of _BitfountMessageType's names or monitoring.AdditionalMonitorMessageTypes
    type: str
    message: NotRequired[str]
    metadata: NotRequired[_JSONDict]
    progress: NotRequired[Dict[str, ProgressCounterDict]]
    resourceUsage: NotRequired[Dict[str, float]]


class _RegisterUserPublicKeyPOSTJSON(TypedDict):
    """Form of POST JSON for registering user public key.

    API: POST /api/[username]/keys

    The public key should be in OpenSSH format.
    """

    key: str  # should be in ssh format


class _PublicKeyJSON(TypedDict):
    """Public Key JSON from Hub.

    Keys will be returned in PEM format.
    """

    public_key: str
    id: str
    active: bool


class _ActivePublicKey(TypedDict):
    """Parsed public key with metadata from the hub."""

    public_key: RSAPublicKey
    id: str
    active: bool


class _UserRSAPublicKeysResponseJSON(TypedDict):
    """Response JSON from GET /api/{username}/keys.

    Keys will be returned in PEM format.
    """

    maximumOffset: int
    keys: List[_PublicKeyJSON]


class _CreatedResourceResponseJSON(TypedDict):
    """Response JSON for resource creation."""

    id: Union[str, int]


# Access Manager-related JSON
class _AccessManagerKeyResponseJSON(TypedDict):
    """Response JSON from GET /api/access-manager-key."""

    accessManagerPublicKey: str


class _SAMLChallengeResponseJSON(TypedDict):
    """Response JSON from GET /api/saml."""

    samlRequest: str
    id: str


class _SAMLAdditionalInfoPOSTJSON(TypedDict):
    """Required keys for JSON POST /api/saml."""

    # If this issue gets resolved then we can actually add the SAML response
    # fields to this as extras: https://github.com/python/mypy/issues/4617
    originalSAMLRequestID: str
    podIdentifier: str
    modellerName: str
    modellerProtocolRequest: SerializedProtocol
    identityProvider: Literal["SAML"]


class _OIDCAccessCheckPostJSON(TypedDict):
    """Required keys for OIDC JSON POST /api/access."""

    podIdentifier: str
    modellerProtocolRequest: SerializedProtocol
    modellerName: str
    modellerToken: str
    identityProvider: Literal["OIDC"]


class _SignatureBasedAccessCheckPostJSON(TypedDict):
    """Required keys for Signatured based JSON POST /api/access.

    NOTE: unsignedTask and taskSignature are byte-strings but will need to be b64
          encoded to allow them to be sent as JSON.
    """

    podIdentifier: str
    modellerName: str
    modellerProtocolRequest: SerializedProtocol
    unsignedTask: str  # b64 encoded byte-string
    taskSignature: str  # b64 encoded byte-string
    identityProvider: Literal["SIGNATURE"]


class _AMAccessCheckResponseJSON(TypedDict):
    """Response JSON from Access Manager access check.

    Covers:
        - POST /api/access
    """

    code: Literal[
        # Common response types
        "ACCEPT",
        # /api/access response types
        "NO_ACCESS",
        "INVALID_PROOF_OF_IDENTITY",
        "UNAUTHORISED",
        "NO_PROOF_OF_IDENTITY",
    ]


# Auth0 related types
class _DeviceCodeRequestDict(TypedDict):
    """Data dictionary for POST request to /oauth/device/code.

    See: https://auth0.com/docs/api/authentication?http#device-authorization-flow
    """

    audience: str
    scope: str
    client_id: str


class _DeviceCodeResponseJSON(TypedDict):
    """JSON response for POST /oauth/device/code.

    See: https://auth0.com/docs/api/authentication?http#device-authorization-flow
    """

    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class _DeviceAccessTokenRequestDict(TypedDict):
    """Data dictionary for device code POST request to /oauth/token.

    See: https://auth0.com/docs/api/authentication?http#device-authorization-flow48
    """

    grant_type: Literal["urn:ietf:params:oauth:grant-type:device_code"]
    client_id: str
    device_code: str


class _DeviceAccessTokenResponseJSON(TypedDict):
    """Success JSON response for POST /oauth/token.

    For Device Authorization Flow.

    See: https://auth0.com/docs/api/authentication?http#device-authorization-flow48
    """

    access_token: str
    id_token: str
    refresh_token: str
    scope: str
    expires_in: int
    token_type: Literal["Bearer"]


class _TokenRefreshRequestDict(TypedDict):
    """Data dictionary for token refresh POST request to /oauth/token.

    This is not the full potential params, but is enough for us.

    See: https://auth0.com/docs/api/authentication?http#refresh-token
    """

    grant_type: Literal["refresh_token"]
    client_id: str
    refresh_token: str


class _TokenRefreshResponseJSON(TypedDict):
    """Success JSON response for refresh token POST /oauth/token.

    See: https://auth0.com/docs/api/authentication?http#refresh-token

    Note that our response will include a new refresh token as we are using
    refresh token rotation.

    See: https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation
    """

    access_token: str
    id_token: str
    refresh_token: str  # see docstring
    scope: str
    expires_in: int
    token_type: Literal["Bearer"]


class _DeviceAccessTokenFailResponseJSON(TypedDict):
    """Fail JSON response for POST /oauth/token.

    For Device Authorization Flow.

    See: https://auth0.com/docs/api/authentication?http#device-authorization-flow48
    """

    error: str
    error_description: str


class _PKCEAccessTokenRequestDict(TypedDict):
    """Data dictionary for ACF with PKCE code POST request to /oauth/token.

    See: https://auth0.com/docs/api/authentication?http#authorization-code-flow-with-pkce45  # noqa: B950
    """

    grant_type: Literal["authorization_code"]
    client_id: str
    code: str
    code_verifier: str
    redirect_uri: str


class _PKCEAccessTokenResponseJSON(TypedDict):
    """Success JSON response for POST /oauth/token.

    For Authorization Code Flow with PKCE.

    See: https://auth0.com/docs/api/authentication?http#authorization-code-flow-with-pkce45  # noqa: B950
    """

    access_token: str
    refresh_token: str
    id_token: str
    token_type: Literal["Bearer"]
    expires_in: int
