# Accounts

API resource for managing Up Bank accounts.

## AccountsResource

Synchronous accounts API.

### Import

```python
from up_bank_sdk.api.accounts import AccountsResource
```

### Methods

#### list()

List all accounts.

```python
accounts = client.accounts.list(
    *,
    page_size: int | None = None,
    account_type: str | None = None,
    ownership_type: str | None = None,
) -> list[Account]
```

#### get()

Get a specific account by ID.

```python
account = client.accounts.get(account_id: str) -> Account
```

#### list_transactions()

List transactions for a specific account (paginated).

```python
response = client.accounts.list_transactions(
    account_id: str,
    *,
    page_size: int | None = None,
) -> PaginatedResponse[Transaction]
```

---

## AsyncAccountsResource

Asynchronous accounts API.

### Import

```python
from up_bank_sdk.api.async_api.accounts import AsyncAccountsResource
```

### Methods

Same as `AccountsResource` but with `async`/`await`:

```python
accounts = await client.accounts.list()
account = await client.accounts.get("account-id")
response = await client.accounts.list_transactions("account-id")
```

---

## Account Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["accounts"]` | Resource type |
| `id` | `str` | Account ID |
| `attributes` | `AccountAttributes` | Account details |
| `relationships` | `dict \| None` | Related resources |

### AccountAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `display_name` | `str` | Human-readable account name |
| `account_type` | `str` | `"TRANSACTIONAL"` or `"SAVER"` |
| `ownership_type` | `str` | `"INDIVIDUAL"` or `"JOINT"` |
| `balance` | `MoneyObject` | Current balance |
| `created_at` | `str` | ISO 8601 creation timestamp |

---

## Examples

### List All Accounts

```python
accounts = client.accounts.list()

for account in accounts:
    print(f"{account.attributes.display_name}: "
          f"{account.attributes.balance.value} "
          f"{account.attributes.balance.currency_code}")
```

### Get Account by ID

```python
account = client.accounts.get("account-id")

print(f"Name: {account.attributes.display_name}")
print(f"Type: {account.attributes.account_type}")
print(f"Balance: {account.attributes.balance.value}")
```

### Filter by Account Type

```python
# Get only saver accounts
savers = client.accounts.list(account_type="SAVER")

# Get only transactional accounts
spending = client.accounts.list(account_type="TRANSACTIONAL")
```

### List Transactions for Account

```python
response = client.accounts.list_transactions("account-id", page_size=50)

for tx in response.data:
    print(f"{tx.attributes.description}: {tx.attributes.amount.value}")

if response.has_more:
    next_page = response.get_next()
```

### Async Example

```python
async with AsyncClient("up:your-token") as client:
    accounts = await client.accounts.list()

    for account in accounts:
        print(f"{account.attributes.display_name}: "
              f"{account.attributes.balance.value}")
```
