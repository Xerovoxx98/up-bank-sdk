# Attachments

API resource for managing Up Bank receipt attachments.

## AttachmentsResource

Synchronous attachments API.

### Import

```python
from up_bank_sdk.api.attachments import AttachmentsResource
```

### Methods

#### list()

List all attachments (paginated).

```python
response = client.attachments.list(
    *,
    page_size: int | None = None,
) -> PaginatedResponse[Attachment]
```

#### get()

Get a specific attachment by ID.

```python
attachment = client.attachments.get(attachment_id: str) -> Attachment
```

---

## AsyncAttachmentsResource

Asynchronous attachments API.

### Import

```python
from up_bank_sdk.api.async_api.attachments import AsyncAttachmentsResource
```

### Methods

Same as `AttachmentsResource` but with `async`/`await`:

```python
response = await client.attachments.list()
attachment = await client.attachments.get("attachment-id")
```

---

## Attachment Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["attachments"]` | Resource type |
| `id` | `str` | Attachment ID |
| `attributes` | `AttachmentAttributes` | Attachment details |
| `relationships` | `AttachmentRelationships \| None` | Related transaction |

### AttachmentAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `file_url` | `str \| None` | URL to download the attachment |
| `file_url_expires_at` | `str \| None` | When the URL expires (ISO 8601) |
| `file_extension` | `str \| None` | File extension (e.g., `"pdf"`) |
| `file_content_type` | `str \| None` | MIME type (e.g., `"image/png"`) |
| `created_at` | `str \| None` | When attached (ISO 8601) |

---

## Examples

### List Attachments

```python
response = client.attachments.list()

for att in response.data:
    print(f"{att.id}: {att.attributes.file_extension}")
    if att.attributes.file_url:
        print(f"  URL: {att.attributes.file_url}")
```

### Get Attachment

```python
attachment = client.attachments.get("attachment-id")

print(f"Type: {attachment.attributes.file_content_type}")
print(f"Extension: {attachment.attributes.file_extension}")
print(f"Expires: {attachment.attributes.file_url_expires_at}")
```

### Check Expired URLs

```python
from datetime import datetime

attachment = client.attachments.get("attachment-id")

if attachment.attributes.file_url_expires_at:
    expires = datetime.fromisoformat(
        attachment.attributes.file_url_expires_at.replace("Z", "+00:00")
    )
    if datetime.now(expires.tzinfo) > expires:
        print("URL has expired!")
    else:
        print(f"URL valid until {expires}")
```

### Download Attachment

```python
import httpx

attachment = client.attachments.get("attachment-id")

if attachment.attributes.file_url:
    # Download the file
    response = httpx.get(attachment.attributes.file_url)
    response.raise_for_status()

    # Save to file
    filename = f"receipt.{attachment.attributes.file_extension}"
    with open(filename, "wb") as f:
        f.write(response.content)
```

### Using with Transactions

```python
# Attachments are linked to transactions
response = client.transactions.list()

for tx in response.data:
    if tx.relationships and tx.relationships.attachment:
        att_id = tx.relationships.attachment["data"]["id"]
        att = client.attachments.get(att_id)
        print(f"Transaction {tx.id} has attachment: {att.attributes.file_extension}")
```
