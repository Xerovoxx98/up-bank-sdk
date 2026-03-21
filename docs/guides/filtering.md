# Filtering

The Up Bank API supports filtering on various endpoints. This guide shows how to use filters effectively.

## Available Filters

### Transactions

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | `str` | Filter by status: `"settled"`, `"pending"`, `"held"` |
| `since` | `str` | ISO 8601 datetime - transactions after this time |
| `until` | `str` | ISO 8601 datetime - transactions before this time |
| `category` | `str` | Category ID to filter by |
| `tag` | `str` | Tag label to filter by |

### Accounts

| Parameter | Type | Description |
|-----------|------|-------------|
| `account_type` | `str` | `"TRANSACTIONAL"` or `"SAVER"` |
| `ownership_type` | `str` | `"INDIVIDUAL"` or `"JOINT"` |

### Categories

| Parameter | Type | Description |
|-----------|------|-------------|
| `parent` | `str` | Parent category ID to get children of |

## Transaction Filters

### Filter by Status

```python
# Only settled transactions
response = client.transactions.list(status="settled")

# Only pending transactions
response = client.transactions.list(status="pending")
```

### Filter by Date Range

```python
# Transactions in January 2024
response = client.transactions.list(
    since="2024-01-01T00:00:00+10:00",
    until="2024-01-31T23:59:59+10:00"
)
```

### Filter by Category

```python
# Transactions in a specific category
response = client.transactions.list(category="groceries")

# Combine with other filters
response = client.transactions.list(
    category="restaurants-and-cafes",
    status="settled"
)
```

### Filter by Tag

```python
# Transactions with a specific tag
response = client.transactions.list(tag="Holiday")

# Combine tag with other filters
response = client.transactions.list(
    tag="Business",
    status="settled",
    since="2024-01-01T00:00:00+10:00"
)
```

### Combining Filters

```python
# All filters can be combined
response = client.transactions.list(
    page_size=100,
    status="settled",
    since="2024-01-01T00:00:00+10:00",
    until="2024-12-31T23:59:59+10:00",
    category="good-life",
    tag="Holiday"
)
```

## Account Filters

### Filter by Account Type

```python
# Only spending accounts
spending = client.accounts.list(account_type="TRANSACTIONAL")

# Only saver accounts
savers = client.accounts.list(account_type="SAVER")
```

### Filter by Ownership Type

```python
# Only individual accounts
individual = client.accounts.list(ownership_type="INDIVIDUAL")

# Only joint accounts
joint = client.accounts.list(ownership_type="JOINT")
```

## Category Filters

### Get Child Categories

```python
# Get subcategories of "Good Life"
children = client.categories.list(parent="good-life")

for cat in children:
    print(f"{cat.id}: {cat.attributes.name}")
```

## Date Format Requirements

Dates must be in ISO 8601 format with timezone:

```
YYYY-MM-DDTHH:MM:SS+HH:MM
```

Examples:
- `2024-01-15T00:00:00+10:00` — January 15, 2024, 10am Sydney time
- `2024-06-01T00:00:00+00:00` — June 1, 2024, midnight UTC

!!! tip "Timezone Aware Dates"
    Always include a timezone offset. Without it, the API may assume UTC or server local time, which could cause unexpected results.

## Common Use Cases

### Monthly Spending Report

```python
from datetime import datetime, timedelta

# Get current month's transactions
today = datetime.now()
first_of_month = today.replace(day=1, hour=0, minute=0, second=0)

response = client.transactions.list(
    status="settled",
    since=first_of_month.isoformat()
)

total = 0
for tx in response.data:
    amount = float(tx.attributes.amount.value)
    total += amount

print(f"Monthly spending: ${total:.2f}")
```

### Year-End Summary

```python
response = client.transactions.list(
    status="settled",
    since="2024-01-01T00:00:00+10:00",
    until="2024-12-31T23:59:59+10:00"
)

# Count transactions by category
category_totals = {}
while response is not None:
    for tx in response.data:
        if tx.attributes.category:
            cat_id = tx.attributes.category.id
            amount = float(tx.attributes.amount.value)
            category_totals[cat_id] = category_totals.get(cat_id, 0) + amount

    if response.has_more:
        response = response.get_next()
    else:
        response = None
```

### Finding Specific Transactions

```python
# Find transactions with a specific description
response = client.transactions.list(status="settled")

for tx in response.data:
    if "UBER" in tx.attributes.description.upper():
        print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
```
