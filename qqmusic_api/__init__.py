"""QQMusic API 公开入口."""

from .core.client import Client
from .core.exceptions import (
    ApiError,
    GlobalAuthFailedError,
    HTTPError,
    LoginError,
    LoginExpiredError,
    NetworkError,
    NotLoginError,
    SignInvalidError,
)
from .core.versioning import Platform
from .models.request import Credential

__version__ = "0.5.0"

__all__ = [
    "ApiError",
    "Client",
    "Credential",
    "GlobalAuthFailedError",
    "HTTPError",
    "LoginError",
    "LoginExpiredError",
    "NetworkError",
    "NotLoginError",
    "Platform",
    "SignInvalidError",
    "__version__",
]
