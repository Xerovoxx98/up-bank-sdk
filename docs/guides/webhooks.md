# Webhooks

Webhooks allow you to receive real-time notifications when events occur in your Up Bank account.

## How Webhooks Work

1. You register a webhook URL with Up Bank
2. When an event occurs (e.g., a new transaction), Up sends an HTTP POST to your URL
3. Your server processes the webhook payload
4. Your server returns a 2xx response to acknowledge receipt

## Creating a Webhook

```python
from up_bank_sdk import Client

client = Client("up:your-token")

# Create a webhook
webhook = client.webhooks.create(
    url="https://your-server.com/webhooks/up",
    description="My webhook for transaction updates"
)

print(f"Created webhook: {webhook.id}")
print(f"Secret: {webhook.attributes.secret}")  # Save this for verification!
```

## Webhook Events

The Up Bank API sends webhooks for these event types:

| Event | Description |
|-------|-------------|
| `transaction.created` | A new transaction was created |
| `transaction.settled` | A pending transaction was settled |
| `transaction.updated` | A transaction was modified |

## Handling Webhooks

### Basic Webhook Handler

```python
from flask import Flask, request, abort
import hmac
import hashlib

app = Flask(__name__)

# Store your webhook secrets (in production, use a database!)
WEBHOOK_SECRETS = {}

@app.route("/webhooks/up", methods=["POST"])
def handle_webhook():
    # Get webhook ID from headers
    webhook_id = request.headers.get("Up-Webhook-Id")
    delivery_id = request.headers.get("Up-Webhook-Delivery-Id")

    # Get the signature
    signature = request.headers.get("Up-Webhook-Signature")

    # Get the payload
    payload = request.get_data()

    # Verify the signature
    secret = WEBHOOK_SECRETS.get(webhook_id)
    if secret:
        expected = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, f"sha256={expected}"):
            abort(400, "Invalid signature")

    # Process the webhook
    data = request.json
    event_type = data.get("data", {}).get("attributes", {}).get("event_type")

    if event_type == "transaction.created":
        transaction = data["data"]["relationships"]["transaction"]["data"]
        print(f"New transaction: {transaction['id']}")

    # Return success
    return "", 204
```

### Verifying Webhook Signatures

Always verify webhook signatures to ensure requests are from Up Bank:

```python
import hmac
import hashlib

def verify_webhook_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:
    """Verify a webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, f"sha256={expected}")
```

## Webhook Management

### List Webhooks

```python
response = client.webhooks.list()

for webhook in response.data:
    print(f"{webhook.id}: {webhook.attributes.url}")
```

### Get a Webhook

```python
webhook = client.webhooks.get("webhook-id")
print(f"URL: {webhook.attributes.url}")
print(f"Created: {webhook.attributes.created_at}")
```

### Delete a Webhook

```python
client.webhooks.delete("webhook-id")
```

### Ping a Webhook

Test your webhook by sending a ping:

```python
client.webhooks.ping("webhook-id")
# This triggers an immediate webhook delivery
```

## Viewing Webhook Logs

Check delivery history and troubleshoot issues:

```python
response = client.webhooks.logs("webhook-id")

for log in response.data:
    req = log.attributes.request
    resp = log.attributes.response

    print(f"Delivery ID: {log.id}")
    print(f"  Status: {resp.status_code if resp else 'N/A'}")
    print(f"  Method: {req.method if req else 'N/A'}")
    print(f"  URI: {req.uri if req else 'N/A'}")
    print(f"  Created: {log.attributes.created_at}")
```

## Best Practices

### 1. Respond Quickly

Return a 2xx response immediately, then process asynchronously:

```python
@app.route("/webhooks/up", methods=["POST"])
def handle_webhook():
    # Acknowledge immediately
    thread = Thread(target=process_webhook, args=(request.get_data(),))
    thread.start()
    return "", 204

def process_webhook(payload):
    # Process in background
    pass
```

### 2. Handle Duplicate Deliveries

Up Bank may retry deliveries. Use the delivery ID to deduplicate:

```python
processed_ids = set()  # Use Redis or a database in production

@app.route("/webhooks/up", methods=["POST"])
def handle_webhook():
    delivery_id = request.headers.get("Up-Webhook-Delivery-Id")

    if delivery_id in processed_ids:
        return "", 204  # Already processed

    # Process and record
    processed_ids.add(delivery_id)
    # ...
```

### 3. Use HTTPS

Always use HTTPS for webhook URLs to ensure data integrity and security.

### 4. Store Secrets Securely

Store webhook secrets securely and retrieve them when verifying signatures. Don't hardcode them.

## Async Webhook Handling

For async frameworks like FastAPI:

```python
from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

@app.post("/webhooks/up")
async def handle_webhook(request: Request):
    payload = await request.body()
    webhook_id = request.headers.get("Up-Webhook-Id")
    signature = request.headers.get("Up-Webhook-Signature")

    # Get secret (from database, etc.)
    secret = await get_webhook_secret(webhook_id)

    # Verify signature
    if not verify_signature(payload, signature, secret):
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Process webhook
    data = await request.json()
    # ...

    return ""
```
