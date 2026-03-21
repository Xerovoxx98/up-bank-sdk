# up-bank-sdk

[![PyPI version](https://img.shields.io/pypi/v/up-bank-sdk.svg)](https://pypi.org/project/up-bank-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/up-bank-sdk.svg)](https://pypi.org/project/up-bank-sdk/)
[![License](https://img.shields.io/github/license/Xerovoxx98/up-bank-sdk.svg)](https://github.com/Xerovoxx98/up-bank-sdk/blob/main/LICENSE)

Python SDK for the [Up Bank API](https://developer.up.com.au/) with full sync and async support.

## Features

- **Sync and Async Clients** — Choose the programming model that fits your needs
- **Explicit Pagination** — Control when you fetch additional pages via `get_next()`
- **Auto-pagination (async)** — Use `async for` to automatically iterate through all pages
- **Pydantic Models** — Type-safe response objects with automatic validation
- **Retry Logic** — Automatic retry with exponential backoff on rate limit (429) and server (5xx) errors
- **Full API Coverage** — Accounts, Transactions, Categories, Tags, Attachments, Webhooks

## Quick Start

### Synchronous

```python
from up_bank_sdk import Client

client = Client("up:your-personal-access-token")

# List accounts
accounts = client.accounts.list()
for account in accounts:
    print(f"{account.attributes.display_name}: {account.attributes.balance.value}")

# Get paginated transactions
response = client.transactions.list(page_size=100)
for tx in response.data:
    print(f"{tx.attributes.description}: {tx.attributes.amount.value}")

# Manually fetch next page
if response.has_more:
    next_page = response.get_next()
```

### Asynchronous

```python
import asyncio
from up_bank_sdk import AsyncClient

async def main():
    async with AsyncClient("up:your-personal-access-token") as client:
        # List transactions with auto-pagination
        async for tx in client.transactions.list(page_size=100, status="settled"):
            print(f"{tx.attributes.description}: {tx.attributes.amount.value}")

asyncio.run(main())
```

## Installation

```bash
pip install up-bank-sdk
```

For development:

```bash
pip install up-bank-sdk[dev]
```

## Requirements

- Python 3.12+
- `requests` (sync) or `httpx` (async)
- `pydantic` for data validation
- `tenacity` for retry logic

## License

This project is licensed under the MIT License.
