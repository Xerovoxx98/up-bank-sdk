# Transactions

API resource for managing Up Bank transactions.

## TransactionsResource

Synchronous transactions API.

### Import

```python
from up_bank_sdk.api.transactions import TransactionsResource
```

### Methods

#### list()

List transactions with optional filtering (paginated).

```python
response = client.transactions.list(
    *,
    page_size: int | None = None,
    status: str | None = None,
    since: str | None = None,
    until: str | None = None,
    category: str | None = None,
    tag: str | None = None,
) -> PaginatedResponse[Transaction]
```

#### get()

Get a specific transaction by ID.

```python
transaction = client.transactions.get(transaction_id: str) -> Transaction
```

#### categorize()

Set or clear a transaction's category.

```python
client.transactions.categorize(
    transaction_id: str,
    category_id: str | None,
) -> None
```

---

## AsyncTransactionsResource

Asynchronous transactions API.

### Import

```python
from up_bank_sdk.api.async_api.transactions import AsyncTransactionsResource
```

### Methods

Same as `TransactionsResource` but with `async`/`await`:

```python
response = await client.transactions.list(status="settled")
tx = await client.transactions.get("transaction-id")
await client.transactions.categorize("transaction-id", "category-id")
```

---

## Transaction Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["transactions"]` | Resource type |
| `id` | `str` | Transaction ID |
| `attributes` | `TransactionAttributes` | Transaction details |
| `relationships` | `TransactionRelationships \| None` | Related resources |

### TransactionAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `status` | `str` | `"SETTLED"`, `"PENDING"`, or `"HELD"` |
| `description` | `str` | Transaction description |
| `message` | `str \| None` | Optional message |
| `amount` | `MoneyObject` | Transaction amount |
| `foreign_amount` | `MoneyObject \| None` | Foreign currency amount |
| `category` | `CategoryResourceIdentifier \| None` | Category reference |
| `tags` | `list[TagResourceIdentifier]` | Tags applied |
| `created_at` | `str` | ISO 8601 creation timestamp |
| `hold_info` | `HoldInfo \| None` | Hold details (for HELD status) |
| `merchant` | `MerchantInfo \| None` | Merchant information |
| `raw_text` | `str \| None` | Raw text from bank |
| `is_categorizable` | `bool` | Whether categorizable |

---

## Examples

### List Transactions

```python
response = client.transactions.list(page_size=100)

for tx in response.data:
    print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
```

### Get Transaction

```python
tx = client.transactions.get("transaction-id")

print(f"Description: {tx.attributes.description}")
print(f"Amount: {tx.attributes.amount.value} {tx.attributes.amount.currency_code}")
print(f"Status: {tx.attributes.status}")
```

### Filter Transactions

```python
# Settled transactions only
settled = client.transactions.list(status="settled")

# Transactions in date range
filtered = client.transactions.list(
    since="2024-01-01T00:00:00+10:00",
    until="2024-12-31T23:59:59+10:00"
)

# By category
groceries = client.transactions.list(category="groceries")

# By tag
tagged = client.transactions.list(tag="Holiday")
```

### Categorize Transaction

```python
# Set a category
client.transactions.categorize("transaction-id", "restaurants-and-cafes")

# Remove category
client.transactions.categorize("transaction-id", None)
```

### Iterate All Transactions (Async)

```python
async with AsyncClient("up:your-token") as client:
    async for tx in client.transactions.list(page_size=100, status="settled"):
        print(f"{tx.attributes.description}: {tx.attributes.amount.value}")
```

### Hold Info (Pending Transactions)

```python
response = client.transactions.list(status="held")

for tx in response.data:
    if tx.attributes.hold_info:
        print(f"Held amount: {tx.attributes.hold_info.amount.value}")
```
