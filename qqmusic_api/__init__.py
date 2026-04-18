"""QQMusic API 公开入口."""

from .core.client import Client
from .core.exceptions import (
    ApiError,
    HTTPError,
    LoginError,
    LoginExpiredError,
    NetworkError,
    NotLoginError,
    RatelimitedError,
    SignInvalidError,
)
from .core.versioning import Platform
from .models.request import Credential

__version__ = "0.5.2"

__all__ = [
    "ApiError",
    "Client",
    "Credential",
    "HTTPError",
    "LoginError",
    "LoginExpiredError",
    "NetworkError",
    "NotLoginError",
    "Platform",
    "RatelimitedError",
    "SignInvalidError",
    "__version__",
]
