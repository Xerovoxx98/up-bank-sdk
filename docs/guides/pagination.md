# Pagination

The Up Bank API returns paginated results. This guide explains how to handle pagination with the SDK.

## Understanding Pagination

When you request a list of transactions (or other resources), the API returns a single "page" of results along with links to navigate to other pages.

!!! info "Page Size"
    The `page_size` parameter controls how many items are returned per page (up to the API's maximum). A smaller page size means more requests but less data per request.

## Explicit Pagination (Sync & Async)

Both sync and async clients support explicit pagination where you control when to fetch the next page.

### Sync Client

```python
# Get first page of transactions
response = client.transactions.list(page_size=100)

# Access the current page's data
for tx in response.data:
    print(tx.attributes.description)

# Check if there are more pages
if response.has_more:
    # Explicitly fetch next page
    next_page = response.get_next()
    for tx in next_page.data:
        print(tx.attributes.description)
```

### Async Client

```python
# Get first page of transactions
response = await client.transactions.list(page_size=100)

# Access the current page's data
for tx in response.data:
    print(tx.attributes.description)

# Check if there are more pages
if response.has_more:
    # Explicitly fetch next page
    next_page = await response.get_next()
    for tx in next_page.data:
        print(tx.attributes.description)
```

## Auto-pagination (Async Only)

The async client supports auto-pagination using `async for`. This automatically fetches the next page when you exhaust the current one.

```python
async with AsyncClient("up:your-token") as client:
    # This will iterate through ALL transactions automatically
    # Fetching new pages as needed
    async for tx in client.transactions.list(page_size=100):
        print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
```

!!! warning "Auto-pagination Fetches All Pages"
    Auto-pagination will continue fetching pages until all items are exhausted. For large datasets, this could result in many API calls. Use `break` to exit early if needed:

    ```python
    async for tx in client.transactions.list(page_size=100):
        print(tx.attributes.description)
        if some_condition:
            break  # Stop pagination
    ```

## PaginatedResponse Properties

| Property | Type | Description |
|----------|------|-------------|
| `data` | `list[T]` | Items on the current page |
| `has_more` | `bool` | `True` if a next page exists |
| `has_prev` | `bool` | `True` if a previous page exists |

## PaginatedResponse Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_next()` | `PaginatedResponse[T] \| None` | Fetch the next page |
| `get_prev()` | `PaginatedResponse[T] \| None` | Fetch the previous page (if available) |
| `__iter__()` | `Iterator[T]` | Iterate over current page items |
| `__len__()` | `int` | Number of items on current page |

## Manual Page Iteration

### Sync Client

```python
response = client.transactions.list(page_size=100)
page_num = 1

while response is not None:
    print(f"=== Page {page_num} ===")
    for tx in response.data:
        print(f"  {tx.attributes.description}")

    if response.has_more:
        response = response.get_next()
        page_num += 1
    else:
        response = None
```

### Async Client with Explicit Pagination

```python
response = await client.transactions.list(page_size=100)
page_num = 1

while response is not None:
    print(f"=== Page {page_num} ===")
    for tx in response.data:
        print(f"  {tx.attributes.description}")

    if response.has_more:
        response = await response.get_next()
        page_num += 1
    else:
        response = None
```

## Choosing a Page Size

| Page Size | Use Case |
|-----------|----------|
| 10-50 | UI display, small result sets |
| 100 | General purpose, good balance |
| 200+ | Batch processing, data export |

!!! tip "API Limits"
    The Up Bank API may impose limits on page size. Check the API documentation for current limits.

## Pagination with Filters

You can combine pagination with filtering:

```python
# Get all settled transactions from 2024
response = client.transactions.list(
    page_size=100,
    status="settled",
    since="2024-01-01T00:00:00+10:00",
    until="2024-12-31T23:59:59+10:00"
)

while response is not None:
    for tx in response.data:
        print(f"{tx.attributes.description}: {tx.attributes.amount.value}")

    if response.has_more:
        response = response.get_next()
    else:
        response = None
```

## Nested Resource Pagination

Some endpoints return paginated results for related resources:

```python
# List transactions for a specific account
response = client.accounts.list_transactions("account-id", page_size=100)

for tx in response.data:
    print(f"{tx.attributes.description}")
```
