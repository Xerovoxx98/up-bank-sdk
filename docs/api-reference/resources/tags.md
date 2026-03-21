# Tags

API resource for managing Up Bank tags.

## TagsResource

Synchronous tags API.

### Import

```python
from up_bank_sdk.api.tags import TagsResource
```

### Methods

#### list()

List all tags (paginated).

```python
response = client.tags.list(
    *,
    page_size: int | None = None,
) -> PaginatedResponse[Tag]
```

#### add_tags()

Add tags to a transaction.

```python
client.tags.add_tags(
    transaction_id: str,
    tags: list[str],
) -> None
```

#### remove_tags()

Remove tags from a transaction.

```python
client.tags.remove_tags(
    transaction_id: str,
    tags: list[str],
) -> None
```

---

## AsyncTagsResource

Asynchronous tags API.

### Import

```python
from up_bank_sdk.api.async_api.tags import AsyncTagsResource
```

### Methods

Same as `TagsResource` but with `async`/`await`:

```python
response = await client.tags.list()
await client.tags.add_tags("transaction-id", ["Tag1", "Tag2"])
await client.tags.remove_tags("transaction-id", ["Tag1"])
```

---

## Tag Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["tags"]` | Resource type |
| `id` | `str` | Tag label (e.g., `"Holiday"`) |
| `relationships` | `TagRelationships \| None` | Related transactions |

---

## Examples

### List Tags

```python
response = client.tags.list()

for tag in response.data:
    print(f"{tag.id}")

print(f"Has more: {response.has_more}")
```

### Add Tags to Transaction

```python
client.tags.add_tags(
    transaction_id="transaction-id",
    tags=["Holiday", "Queensland"]
)
```

### Remove Tags from Transaction

```python
client.tags.remove_tags(
    transaction_id="transaction-id",
    tags=["Holiday"]
)
```

### Iterate All Tags (Async)

```python
async with AsyncClient("up:your-token") as client:
    async for tag in client.tags.list(page_size=100):
        print(f"{tag.id}")
```

### Tags with Transactions

```python
# Transactions already have tags embedded
response = client.transactions.list()

for tx in response.data:
    if tx.attributes.tags:
        tag_names = [t.id for t in tx.attributes.tags]
        print(f"{tx.attributes.description}: {tag_names}")
```

### Tag Workflow

```python
# Add multiple tags
client.tags.add_tags("tx-123", ["Business", "Travel"])

# Later, remove one
client.tags.remove_tags("tx-123", ["Travel"])

# Add more
client.tags.add_tags("tx-123", ["Expenses"])
```
