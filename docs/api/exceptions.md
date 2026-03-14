# Exceptions API

## Exception Hierarchy

```tree
BaseError
├─ ApiError
│  ├─ ApiDataError
│  ├─ CredentialError
│  │  ├─ LoginExpiredError
│  │  └─ NotLoginError
│  ├─ RequestGroupResultMissingError
│  ├─ SignInvalidError
│  └─ RateLimitError
├─ NetworkError
├─ HTTPError
└─ LoginError
```

::: core.exceptions
