# Client

The main client classes for interacting with the Up Bank API.

## Client

Synchronous client for the Up Bank API.

### Import

```python
from up_bank_sdk import Client
```

### Initialization

```python
client = Client(api_key: str, *, config: Config | None = None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | Required | Your Up Bank personal access token |
| `config` | `Config` | `None` | Optional configuration overrides |

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `accounts` | `AccountsResource` | Accounts API |
| `transactions` | `TransactionsResource` | Transactions API |
| `categories` | `CategoriesResource` | Categories API |
| `tags` | `TagsResource` | Tags API |
| `attachments` | `AttachmentsResource` | Attachments API |
| `webhooks` | `WebhooksResource` | Webhooks API |
| `util` | `UtilResource` | Utility endpoints |

### Example

```python
from up_bank_sdk import Client

client = Client("up:your-token")

# List accounts
accounts = client.accounts.list()

# Get transaction
tx = client.transactions.get("transaction-id")
```

---

## AsyncClient

Asynchronous client for the Up Bank API.

### Import

```python
from up_bank_sdk import AsyncClient
```

### Initialization

```python
async with AsyncClient(api_key: str, *, config: Config | None = None) as client:
    # ...
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | Required | Your Up Bank personal access token |
| `config` | `Config` | `None` | Optional configuration overrides |

### Attributes

Same as `Client`, but with async variants:

| Attribute | Type | Description |
|-----------|------|-------------|
| `accounts` | `AsyncAccountsResource` | Accounts API |
| `transactions` | `AsyncTransactionsResource` | Transactions API |
| `categories` | `AsyncCategoriesResource` | Categories API |
| `tags` | `AsyncTagsResource` | Tags API |
| `attachments` | `AsyncAttachmentsResource` | Attachments API |
| `webhooks` | `AsyncWebhooksResource` | Webhooks API |
| `util` | `AsyncUtilResource` | Utility endpoints |

### Example

```python
import asyncio
from up_bank_sdk import AsyncClient

async def main():
    async with AsyncClient("up:your-token") as client:
        # List accounts
        accounts = await client.accounts.list()

        # Auto-paginate transactions
        async for tx in client.transactions.list(page_size=100):
            print(tx.attributes.description)

asyncio.run(main())
```

---

## Config

Configuration options for the SDK.

### Import

```python
from up_bank_sdk import Config
```

### Initialization

```python
config = Config(
    base_url: str = "https://api.up.com.au/api/v1",
    timeout: float = 30.0,
    max_retries: int = 3,
    retry_wait_multiplier: float = 1.0,
    retry_wait_min: float = 2.0,
    retry_wait_max: float = 30.0,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | `str` | `"https://api.up.com.au/api/v1"` | API base URL |
| `timeout` | `float` | `30.0` | Request timeout in seconds |
| `max_retries` | `int` | `3` | Maximum retry attempts |
| `retry_wait_multiplier` | `float` | `1.0` | Exponential backoff multiplier |
| `retry_wait_min` | `float` | `2.0` | Minimum wait between retries (seconds) |
| `retry_wait_max` | `float` | `30.0` | Maximum wait between retries (seconds) |

### Example

```python
from up_bank_sdk import Client, Config

config = Config(
    timeout=60.0,
    max_retries=5,
    retry_wait_min=4.0,
    retry_wait_max=120.0,
)

client = Client("up:your-token", config=config)
```

---

## PaginatedResponse

Paginated response for synchronous clients.

### Type Parameters

- `T` - The type of items in the response

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `data` | `list[T]` | Items on the current page |
| `has_more` | `bool` | `True` if a next page exists |
| `has_prev` | `bool` | `True` if a previous page exists |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_next()` | `PaginatedResponse[T] \| None` | Fetch the next page |
| `get_prev()` | `PaginatedResponse[T] \| None` | Fetch the previous page |
| `__iter__()` | `Iterator[T]` | Iterate over current page items |
| `__len__()` | `int` | Number of items on current page |

### Example

```python
response = client.transactions.list(page_size=100)

for tx in response.data:
    print(tx.attributes.description)

if response.has_more:
    next_page = response.get_next()
```

---

## AsyncPaginatedResponse

Paginated response for asynchronous clients with auto-pagination support.

### Type Parameters

- `T` - The type of items in the response

### Properties

Same as `PaginatedResponse`:

| Property | Type | Description |
|----------|------|-------------|
| `data` | `list[T]` | Items on the current page |
| `has_more` | `bool` | `True` if a next page exists |
| `has_prev` | `bool` | `True` if a previous page exists |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_next()` | `Awaitable[AsyncPaginatedResponse[T] \| None]` | Fetch the next page |
| `__aiter__()` | `AsyncIterator[T]` | Auto-paginate through all pages |

### Example

```python
# Explicit pagination
response = await client.transactions.list(page_size=100)

for tx in response.data:
    print(tx.attributes.description)

if response.has_more:
    next_page = await response.get_next()

# Auto-pagination
async for tx in client.transactions.list(page_size=100):
    print(tx.attributes.description)
```
