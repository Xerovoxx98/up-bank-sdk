# UP Bank SDK

![Tests](https://github.com/Xerovoxx98/up-bank-sdk/actions/workflows/tests.yml/badge.svg) ![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) [![PyPI version](https://badge.fury.io/py/up-bank-sdk.svg)](https://pypi.org/project/up-bank-sdk/) [![PyPI downloads](https://img.shields.io/pypi/dm/up-bank-sdk.svg)](https://pypi.org/project/up-bank-sdk/)

Python SDK for the Up Bank API with sync/async support

## Installation

```bash
pip install up-bank-sdk
```

## Quick Start

### Sync Client

```python
from up_bank_sdk import Client

client = Client("up:your-personal-access-token")

# Ping the API
ping = client.util.ping()
print(f"Status: {ping.meta.status_emoji}")

# List accounts
accounts = client.accounts.list()
for account in accounts:
    print(f"{account.attributes.display_name}: {account.attributes.balance.value}")

# Get paginated transactions (first page of 100)
response = client.transactions.list(page_size=100)
for tx in response.data:
    print(f"{tx.attributes.description}: {tx.attributes.amount.value}")

# Manually fetch next page when needed
if response.has_more:
    next_page = response.get_next()
    for tx in next_page.data:
        print(tx.attributes.description)
```

### Async Client

```python
import asyncio
from up_bank_sdk import AsyncClient

async def main():
    async with AsyncClient("up:your-personal-access-token") as client:
        # All methods are async
        accounts = await client.accounts.list()
        
        # Explicit pagination (same as sync)
        response = await client.transactions.list(page_size=100)
        for tx in response.data:
            print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
        
        # Auto-pagination with async for
        async for tx in client.transactions.list(page_size=100):
            print(tx.attributes.description)

asyncio.run(main())
```

## Features

- **Sync and Async Support**: Choose between synchronous or asynchronous clients
- **Explicit Pagination**: Control when you fetch additional pages via `get_next()`
- **Auto-pagination (async)**: Use `async for` to automatically iterate through all pages
- **Pydantic Models**: Type-safe response objects with proper validation
- **Retry Logic**: Automatic retry with exponential backoff on rate limit (429) and server (5xx) errors
- **Full API Coverage**: Accounts, Transactions, Categories, Tags, Attachments, Webhooks

## Configuration

```python
from up_bank_sdk import Client, AsyncClient, Config

# Default configuration
client = Client("up:your-token")
async_client = AsyncClient("up:your-token")

# Custom configuration
config = Config(
    timeout=60.0,
    max_retries=5,
    retry_wait_min=4.0,
    retry_wait_max=120.0,
)
client = Client("up:your-token", config=config)
async_client = AsyncClient("up:your-token", config=config)
```

## Error Handling

```python
from up_bank_sdk import Client
from up_bank_sdk.exceptions import (
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
```

## Pagination

All list endpoints return a `PaginatedResponse` object:

```python
response = client.transactions.list(page_size=100)

# Access the current page's data
for tx in response.data:
    print(tx.attributes.description)

# Check if there are more pages
if response.has_more:
    # Fetch the next page explicitly
    next_page = response.get_next()
    # next_page is None if no more pages
```

### Async Auto-pagination

With the async client, you can use `async for` to automatically iterate through all pages:

```python
async with AsyncClient("up:your-token") as client:
    # This will fetch all transactions automatically
    async for tx in client.transactions.list(page_size=100):
        print(tx.attributes.description)
```

## API Reference

### Accounts

```python
# List all accounts
accounts = client.accounts.list()

# Filter by type
savers = client.accounts.list(account_type="SAVER")

# Get single account
account = client.accounts.get("account-id")

# List transactions for an account (paginated)
response = client.accounts.list_transactions("account-id", page_size=50)
for tx in response.data:
    print(tx.attributes.description)
if response.has_more:
    next_page = response.get_next()
```

### Transactions

```python
# Get first page of transactions
response = client.transactions.list(page_size=100)
for tx in response.data:
    print(tx.attributes.description)

# Explicitly get next page
while response.has_more:
    response = response.get_next()
    for tx in response.data:
        print(tx.attributes.description)

# Filter transactions
response = client.transactions.list(
    page_size=100,
    status="SETTLED",
    since="2024-01-01T00:00:00+10:00",
    until="2024-12-31T23:59:59+10:00",
    category="food-and-dining",
    tag="Holiday",
)

# Categorize transaction
client.transactions.categorize("tx-id", "restaurants-and-cafes")

# Remove category
client.transactions.categorize("tx-id", None)
```

### Categories

```python
# List all categories
categories = client.categories.list()

# Get children of a category
children = client.categories.list(parent="good-life")

# Get single category
category = client.categories.get("restaurants-and-cafes")
```

### Tags

```python
# List tags (first page)
response = client.tags.list()
for tag in response.data:
    print(tag.id)

# Add tags to transaction
client.tags.add_tags("tx-id", ["Holiday", "Queensland"])

# Remove tags from transaction
client.tags.remove_tags("tx-id", ["Holiday"])
```

### Attachments

```python
# List attachments (first page)
response = client.attachments.list()
for attachment in response.data:
    print(f"Download: {attachment.attributes.file_url}")

# Get single attachment
attachment = client.attachments.get("attachment-id")
```

### Webhooks

```python
# List webhooks
response = client.webhooks.list()
for webhook in response.data:
    print(webhook.attributes.url)

# Create webhook
webhook = client.webhooks.create("https://example.com/webhook")

# Get webhook
webhook = client.webhooks.get("webhook-id")

# Delete webhook
client.webhooks.delete("webhook-id")

# Ping webhook
client.webhooks.ping("webhook-id")

# Get webhook logs
logs_response = client.webhooks.logs("webhook-id")
for log in logs_response.data:
    req = log.attributes.request
    if req and req.method and req.uri:
        print(f"Request: {req.method} {req.uri}")
```

### Utility

```python
# Ping the API
ping = client.util.ping()
print(ping.meta.status_emoji)  # ⚡️
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check up_bank_sdk/

# Type checking
mypy up_bank_sdk/
```

## License

MIT
