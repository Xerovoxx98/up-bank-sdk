# Exceptions

Exception hierarchy for error handling.

## Exception Hierarchy

```
SDKError (Base exception)
└── APIError
    ├── AuthenticationError    # 401 - invalid or missing token
    ├── NotFoundError         # 404 - resource not found
    ├── InvalidRequestError   # 422 - malformed request
    ├── RateLimitError       # 429 - too many requests
    └── ServerError          # 5xx - server error
```

## SDKError

Base exception for all SDK errors.

### Import

```python
from up_bank_sdk.exceptions import SDKError
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Human-readable error message |

---

## APIError

HTTP error from the API.

### Import

```python
from up_bank_sdk.exceptions import APIError
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | `int` | HTTP status code |
| `message` | `str` | Error message |
| `errors` | `list[ErrorDetail]` | Detailed error list |

### ErrorDetail

| Attribute | Type | Description |
|-----------|------|-------------|
| `status` | `str` | Error status code |
| `title` | `str` | Error title |
| `detail` | `str` | Detailed error message |
| `source` | `ErrorSource \| None` | Error source location |

### ErrorSource

| Attribute | Type | Description |
|-----------|------|-------------|
| `parameter` | `str \| None` | Parameter causing the error |
| `pointer` | `str \| None` | Pointer to error location |

---

## AuthenticationError

401 Unauthorized - invalid or missing API token.

### Import

```python
from up_bank_sdk.exceptions import AuthenticationError
```

### Example

```python
try:
    client = Client("invalid-token")
    client.util.ping()
except AuthenticationError:
    print("Invalid API token!")
```

---

## NotFoundError

404 Not Found - the requested resource doesn't exist.

### Import

```python
from up_bank_sdk.exceptions import NotFoundError
```

### Example

```python
try:
    account = client.accounts.get("nonexistent-id")
except NotFoundError:
    print("Account not found")
```

---

## InvalidRequestError

422 Invalid Request - the request was malformed or invalid.

### Import

```python
from up_bank_sdk.exceptions import InvalidRequestError
```

### Example

```python
try:
    # Invalid request
    client.accounts.get("")
except InvalidRequestError as e:
    print(f"Invalid request: {e.message}")
    for error in e.errors:
        print(f"  {error.title}: {error.detail}")
```

---

## RateLimitError

429 Too Many Requests - rate limit exceeded.

### Import

```python
from up_bank_sdk.exceptions import RateLimitError
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `retry_after` | `int \| None` | Seconds to wait before retrying |

### Example

```python
try:
    accounts = client.accounts.list()
except RateLimitError as e:
    print(f"Rate limited! Retry after {e.retry_after} seconds")
```

---

## ServerError

5xx Server Error - Up Bank server error.

### Import

```python
from up_bank_sdk.exceptions import ServerError
```

### Example

```python
try:
    accounts = client.accounts.list()
except ServerError as e:
    print(f"Server error: {e.status_code}")
```

---

## Error Handling Examples

### Basic

```python
from up_bank_sdk import Client
from up_bank_sdk.exceptions import SDKError

client = Client("up:your-token")

try:
    account = client.accounts.get("id")
except SDKError as e:
    print(f"Error: {e.message}")
```

### Detailed

```python
from up_bank_sdk.exceptions import APIError, RateLimitError

try:
    client.accounts.list()
except APIError as e:
    print(f"API Error: {e.status_code} - {e.message}")
    if e.errors:
        for error in e.errors:
            print(f"  {error.title}: {error.detail}")
except RateLimitError as e:
    print(f"Rate limited! Retry after {e.retry_after}s")
```

### Catching Multiple

```python
from up_bank_sdk.exceptions import (
    NotFoundError,
    RateLimitError,
    ServerError,
)

try:
    client.accounts.get("id")
except (NotFoundError, RateLimitError, ServerError) as e:
    print(f"Request failed: {e.message}")
```
