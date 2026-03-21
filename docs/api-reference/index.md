# API Reference

Complete reference documentation for the up-bank-sdk.

## Overview

The SDK is organized into these main components:

| Component | Description |
|-----------|-------------|
| [`Client`](client.md) | Synchronous client for the Up Bank API |
| [`AsyncClient`](client.md) | Asynchronous client for the Up Bank API |
| [`Config`](client.md) | Configuration options |
| [Resources](resources/accounts.md) | API resource classes |
| [Exceptions](exceptions.md) | Exception hierarchy |

## Quick Reference

```python
from up_bank_sdk import Client, AsyncClient, Config

# Sync client
client = Client("up:your-token")

# Async client
async with AsyncClient("up:your-token") as client:
    await client.accounts.list()

# Custom configuration
config = Config(timeout=60.0, max_retries=5)
client = Client("up:your-token", config=config)
```

## Resource Classes

| Resource | Sync Class | Async Class |
|----------|------------|-------------|
| Accounts | `AccountsResource` | `AsyncAccountsResource` |
| Transactions | `TransactionsResource` | `AsyncTransactionsResource` |
| Categories | `CategoriesResource` | `AsyncCategoriesResource` |
| Tags | `TagsResource` | `AsyncTagsResource` |
| Attachments | `AttachmentsResource` | `AsyncAttachmentsResource` |
| Webhooks | `WebhooksResource` | `AsyncWebhooksResource` |
| Utility | `UtilResource` | `AsyncUtilResource` |

## Data Models

All API responses are deserialized into Pydantic models:

- `Account` - Bank accounts
- `Transaction` - Individual transactions
- `Category` - Transaction categories
- `Tag` - Transaction tags
- `Attachment` - Receipt attachments
- `Webhook` - Webhook configurations
- `WebhookLog` - Webhook delivery logs
- `MoneyObject` - Monetary values

## Pagination

List endpoints return paginated responses:

- `PaginatedResponse[T]` - Sync pagination
- `AsyncPaginatedResponse[T]` - Async pagination with auto-iteration

## Error Handling

All exceptions inherit from `SDKError`:

- `APIError` - HTTP errors from the API
- `AuthenticationError` - 401 errors
- `NotFoundError` - 404 errors
- `RateLimitError` - 429 errors with `retry_after`
- `ServerError` - 5xx errors
