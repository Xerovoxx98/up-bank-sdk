# Error Handling

The SDK provides a hierarchy of exceptions to help you handle errors gracefully.

## Exception Hierarchy

```
SDKError (Base exception)
└── APIError
    ├── AuthenticationError    # 401 - invalid or missing token
    ├── NotFoundError         # 404 - resource not found
    ├── InvalidRequestError   # 422 - malformed request
    ├── RateLimitError        # 429 - too many requests
    └── ServerError          # 5xx - server error
```

## Catching Exceptions

### Basic Error Handling

```python
from up_bank_sdk import Client
from up_bank_sdk.exceptions import (
    SDKError,
    APIError,
    NotFoundError,
    RateLimitError,
    AuthenticationError,
)

client = Client("up:your-token")

try:
    account = client.accounts.get("invalid-id")
except NotFoundError:
    print("Account not found")
except AuthenticationError:
    print("Invalid API token")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after} seconds")
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
except SDKError as e:
    print(f"SDK error: {e.message}")
```

### Catching All Errors

```python
try:
    account = client.accounts.get("account-id")
    transactions = client.transactions.list()
except SDKError as e:
    print(f"An error occurred: {e.message}")
```

## Exception Details

### SDKError

Base exception for all SDK errors.

```python
try:
    # ...
except SDKError as e:
    print(e.message)  # Human-readable message
    print(str(e))       # Same as message
```

### APIError

HTTP error from the API.

```python
try:
    # ...
except APIError as e:
    print(e.status_code)  # HTTP status code (e.g., 404)
    print(e.message)      # Error message
    print(e.errors)       # List of ErrorDetail objects
```

### ErrorDetail

Detailed error information for 422 responses:

```python
try:
    # ...
except InvalidRequestError as e:
    for error in e.errors:
        print(f"  {error.title}: {error.detail}")
        if error.source:
            print(f"    Parameter: {error.source.parameter}")
```

### RateLimitError

Special handling for rate limit errors:

```python
try:
    # ...
except RateLimitError as e:
    print(f"Rate limited!")
    print(f"Retry after: {e.retry_after} seconds")
    # Use retry_after to wait before retrying
    time.sleep(e.retry_after)
```

## Retry Logic

The SDK automatically retries on certain errors:

| Error | Retry? |
|-------|--------|
| RateLimitError (429) | Yes |
| ServerError (5xx) | Yes |
| Network errors | Yes |
| Other errors (4xx) | No |

### Configuring Retries

```python
from up_bank_sdk import Client, Config

config = Config(
    max_retries=5,              # Maximum retry attempts
    retry_wait_min=2.0,         # Minimum wait between retries (seconds)
    retry_wait_max=30.0,        # Maximum wait between retries (seconds)
    retry_wait_multiplier=1.0,  # Exponential backoff multiplier
)

client = Client("up:your-token", config=config)
```

### Manual Retry

For more control, implement your own retry logic:

```python
import time
from up_bank_sdk import Client
from up_bank_sdk.exceptions import RateLimitError

def fetch_with_retry(client, account_id, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return client.accounts.get(account_id)
        except RateLimitError as e:
            if attempt == max_attempts - 1:
                raise
            wait_time = e.retry_after or 1
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
```

## Common Error Scenarios

### Invalid Account ID

```python
try:
    account = client.accounts.get("invalid-id")
except NotFoundError:
    print("Account not found")
```

### Invalid API Token

```python
try:
    client = Client("invalid-token")
    client.util.ping()
except AuthenticationError:
    print("Invalid API token")
```

### Network Errors

```python
try:
    accounts = client.accounts.list()
except SDKError as e:
    print(f"Network error: {e.message}")
```

## Error Prevention Tips

1. **Validate IDs before making requests** when possible
2. **Handle rate limits** by respecting `Retry-After` headers
3. **Use appropriate timeouts** to avoid hanging requests
4. **Implement circuit breakers** for critical integrations

## Debugging Errors

### Enable Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Inspect Error Details

```python
try:
    client.accounts.get("invalid-id")
except APIError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Errors: {e.errors}")
```
