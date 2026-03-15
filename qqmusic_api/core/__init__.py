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
    RateLimitError,
    RequestGroupResultMissingError,
    SignInvalidError,
    build_api_error,
    extract_api_error_code,
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
    "RateLimitError",
    "Request",
    "RequestGroup",
    "RequestGroupResult",
    "RequestGroupResultMissingError",
    "SignInvalidError",
    "VersionPolicy",
    "VersionProfile",
    "build_api_error",
    "extract_api_error_code",
]
