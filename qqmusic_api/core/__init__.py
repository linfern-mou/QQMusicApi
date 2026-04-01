"""core 模块."""

from .client import Client, ClientConfig
from .exceptions import (
    ApiDataError,
    ApiError,
    BaseError,
    CredentialError,
    HTTPError,
    LoginError,
    LoginExpiredError,
    NetworkError,
    NotLoginError,
    RatelimitedError,
    RequestGroupResultMissingError,
    SignInvalidError,
    _build_api_error,
    _extract_api_error_code,
)
from .request import Request, RequestGroup, RequestGroupResult
from .versioning import DEFAULT_VERSION_POLICY, Platform, VersionPolicy, VersionProfile

__all__ = [
    "DEFAULT_VERSION_POLICY",
    "ApiDataError",
    "ApiError",
    "BaseError",
    "Client",
    "ClientConfig",
    "CredentialError",
    "HTTPError",
    "LoginError",
    "LoginExpiredError",
    "NetworkError",
    "NotLoginError",
    "Platform",
    "RatelimitedError",
    "Request",
    "RequestGroup",
    "RequestGroupResult",
    "RequestGroupResultMissingError",
    "SignInvalidError",
    "VersionPolicy",
    "VersionProfile",
    "_build_api_error",
    "_extract_api_error_code",
]
