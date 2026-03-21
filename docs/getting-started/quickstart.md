# Quick Start

This guide shows you how to make your first API calls with the up-bank-sdk.

## Get Your API Token

Before you can use the SDK, you need a personal access token from Up Bank:

1. Open the Up app
2. Go to **Settings** → **Data sharing** → **Personal Access Token**
3. Create a new token
4. Copy the token (it starts with `up:`)

## First API Call

### Synchronous Client

```python
from up_bank_sdk import Client

# Initialize the client with your API token
client = Client("up:your-personal-access-token")

# Ping the API to verify connectivity
ping = client.util.ping()
print(f"Status: {ping.meta.status_emoji}")  # ⚡️

# List all accounts
accounts = client.accounts.list()
for account in accounts:
    print(f"{account.attributes.display_name}: {account.attributes.balance.value}")
```

### Asynchronous Client

```python
import asyncio
from up_bank_sdk import AsyncClient

async def main():
    async with AsyncClient("up:your-personal-access-token") as client:
        # Ping the API
        ping = await client.util.ping()
        print(f"Status: {ping.meta.status_emoji}")

        # List accounts
        accounts = await client.accounts.list()
        for account in accounts:
            print(f"{account.attributes.display_name}: {account.attributes.balance.value}")

asyncio.run(main())
```

## Working with Transactions

### List Transactions

```python
# Get paginated transactions
response = client.transactions.list(page_size=100)

print(f"Found {len(response.data)} transactions on this page")
print(f"Has more pages: {response.has_more}")

# Iterate over current page
for tx in response.data:
    print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
```

### Fetch Next Page

```python
response = client.transactions.list(page_size=100)

# Check if there are more pages
if response.has_more:
    # Explicitly fetch next page
    next_page = response.get_next()
    for tx in next_page.data:
        print(tx.attributes.description)
```

### Auto-pagination (Async Only)

With the async client, you can use `async for` to automatically iterate through all pages:

```python
async with AsyncClient("up:your-token") as client:
    # This will fetch ALL transactions automatically
    async for tx in client.transactions.list(page_size=100):
        print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
```

## Filtering Transactions

```python
# Filter by status (settled, pending, held)
response = client.transactions.list(status="settled")

# Filter by date range
response = client.transactions.list(
    since="2024-01-01T00:00:00+10:00",
    until="2024-12-31T23:59:59+10:00"
)

# Filter by category
response = client.transactions.list(category="groceries")

# Filter by tag
response = client.transactions.list(tag="Groceries")
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

## Next Steps

- Learn about [pagination](pagination.md) patterns
- Explore [filtering](filtering.md) options
- Set up [webhooks](webhooks.md) for real-time updates
- Handle [errors](error-handling.md) gracefully
