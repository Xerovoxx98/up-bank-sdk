# Webhooks

API resource for managing Up Bank webhooks.

## WebhooksResource

Synchronous webhooks API.

### Import

```python
from up_bank_sdk.api.webhooks import WebhooksResource
```

### Methods

#### list()

List all webhooks (paginated).

```python
response = client.webhooks.list(
    *,
    page_size: int | None = None,
) -> PaginatedResponse[Webhook]
```

#### create()

Create a new webhook.

```python
webhook = client.webhooks.create(
    url: str,
    *,
    description: str | None = None,
) -> Webhook
```

#### get()

Get a specific webhook by ID.

```python
webhook = client.webhooks.get(webhook_id: str) -> Webhook
```

#### delete()

Delete a webhook.

```python
client.webhooks.delete(webhook_id: str) -> None
```

#### ping()

Send a test ping to a webhook.

```python
client.webhooks.ping(webhook_id: str) -> None
```

#### logs()

Get delivery logs for a webhook (paginated).

```python
response = client.webhooks.logs(
    webhook_id: str,
    *,
    page_size: int | None = None,
) -> PaginatedResponse[WebhookLog]
```

---

## AsyncWebhooksResource

Asynchronous webhooks API.

### Import

```python
from up_bank_sdk.api.async_api.webhooks import AsyncWebhooksResource
```

### Methods

Same as `WebhooksResource` but with `async`/`await`:

```python
response = await client.webhooks.list()
webhook = await client.webhooks.create("https://example.com/webhook")
await client.webhooks.delete("webhook-id")
await client.webhooks.ping("webhook-id")
response = await client.webhooks.logs("webhook-id")
```

---

## Webhook Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["webhooks"]` | Resource type |
| `id` | `str` | Webhook ID |
| `attributes` | `WebhookAttributes` | Webhook details |

### WebhookAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `url` | `str` | The URL receiving webhook requests |
| `description` | `str \| None` | Optional description |
| `secret` | `str \| None` | Secret for signature verification |
| `created_at` | `str \| None` | Creation timestamp (ISO 8601) |

---

## WebhookLog Model

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `Literal["webhook-delivery-logs"]` | Resource type |
| `id` | `str` | Delivery log ID |
| `attributes` | `WebhookLogAttributes` | Delivery details |

### WebhookLogAttributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `request` | `WebhookLogRequest \| None` | Request that was sent |
| `response` | `WebhookLogResponseData \| None` | Response received |
| `created_at` | `str \| None` | Delivery timestamp |

### WebhookLogRequest

| Attribute | Type | Description |
|-----------|------|-------------|
| `uri` | `str \| None` | Request URI |
| `method` | `str \| None` | HTTP method |
| `headers` | `dict \| None` | Request headers |
| `body` | `str \| None` | Request body |

### WebhookLogResponseData

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | `int \| None` | HTTP status code |
| `headers` | `dict \| None` | Response headers |
| `body` | `str \| None` | Response body |

---

## Examples

### Create Webhook

```python
webhook = client.webhooks.create(
    url="https://your-server.com/webhooks/up",
    description="Transaction notifications"
)

print(f"Created: {webhook.id}")
print(f"Secret: {webhook.attributes.secret}")  # Save this!
```

### List Webhooks

```python
response = client.webhooks.list()

for wh in response.data:
    print(f"{wh.id}: {wh.attributes.url}")
```

### Delete Webhook

```python
client.webhooks.delete("webhook-id")
```

### Test Webhook (Ping)

```python
client.webhooks.ping("webhook-id")
# Up will immediately send a test webhook to your URL
```

### View Delivery Logs

```python
response = client.webhooks.logs("webhook-id")

for log in response.data:
    req = log.attributes.request
    resp = log.attributes.response

    print(f"Delivery: {log.id}")
    if req:
        print(f"  Request: {req.method} {req.uri}")
    if resp:
        print(f"  Response: {resp.status_code}")
```

### Signature Verification

```python
import hmac
import hashlib

def verify(secret: str, payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, f"sha256={expected}")
```

### Async Webhook Handler (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhooks/up")
async def handle_webhook(request: Request):
    payload = await request.body()
    webhook_id = request.headers.get("Up-Webhook-Id")
    signature = request.headers.get("Up-Webhook-Signature")

    # Verify signature...

    data = await request.json()
    event = data.get("data", {}).get("attributes", {}).get("event_type")
    print(f"Received: {event}")

    return ""
```
