# Categories

API resource for managing Up Bank categories.

## CategoriesResource

Synchronous categories API.

### Import

```python
from up_bank_sdk.api.categories import CategoriesResource
```

### Methods

#### list()

List all categories.

```python
categories = client.categories.list(
    *,
    parent: str | None = None,
) -> list[Category]
```

#### get()

Get a specific category by ID.

```python
category = client.categories.get(category_id: str) -> Category
```

---

## AsyncCategoriesResource

Asynchronous categories API.

### Import

```python
from up_bank_sdk.api.async_api.categories import AsyncCategoriesResource
```

### Methods

Same as `CategoriesResource` but with `async`/`await`:

```python
categories = await client.categories.list()
category = await client.categories.get("category-id")
```

---

## Category Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["categories"]` | Resource type |
| `id` | `str` | Category ID (e.g., `"groceries"`) |
| `attributes` | `CategoryAttributes` | Category details |
| `relationships` | `CategoryRelationships \| None` | Related categories |

### CategoryAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Human-readable category name |

---

## Examples

### List All Categories

```python
categories = client.categories.list()

for cat in categories:
    print(f"{cat.id}: {cat.attributes.name}")
```

### Get Category

```python
category = client.categories.get("groceries")
print(f"Name: {category.attributes.name}")
```

### List Child Categories

```python
# Get subcategories of "Good Life"
children = client.categories.list(parent="good-life")

for cat in children:
    print(f"{cat.id}: {cat.attributes.name}")
```

### Find Root Categories

```python
# Root categories have no parent
root = [c for c in client.categories.list() if c.relationships is None or c.relationships.parent is None]
```

### Using with Transactions

```python
# Filter transactions by category
response = client.transactions.list(category="groceries")

for tx in response.data:
    print(f"{tx.attributes.description}")
```
