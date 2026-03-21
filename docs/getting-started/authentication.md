# Authentication

The Up Bank API uses personal access tokens for authentication. This guide explains how to obtain and use your token.

## Obtaining a Token

### Step 1: Open the Up App

1. Open the Up app on your device
2. Navigate to **Settings** (gear icon)

### Step 2: Create Personal Access Token

1. Go to **Data sharing** → **Personal Access Token**
2. Tap **Create new token**
3. Give your token a descriptive name (e.g., "My Python SDK")
4. Set expiration if desired
5. Tap **Create**

### Step 3: Copy Your Token

Your token will look something like:

```
up:yeah:Gkbg3PSPoEnxHnmPqmFkkXphqJmuveKFyfjJeptwDRZXPyVjdwuqVGSqTJywVNaQMBKQWprWfTqTPNBNhZm
```

!!! warning "Token Security"
    Your personal access token grants full access to your Up Bank account via the API. Treat it like a password:
    
    - **Never** commit it to version control
    - **Never** log it or display it in error messages
    - **Never** share it publicly

## Using Your Token

### Environment Variable (Recommended)

Store your token in an environment variable and access it at runtime:

```bash
# Linux/macOS
export UP_API_TOKEN="up:your-token"

# Windows (Command Prompt)
set UP_API_TOKEN=up:your-token

# Windows (PowerShell)
$env:UP_API_TOKEN = "up:your-token"
```

Then in Python:

```python
import os
from up_bank_sdk import Client

token = os.environ.get("UP_API_TOKEN")
client = Client(token)
```

### Dotenv File

Use a `.env` file for local development:

```bash
# .env (add this to .gitignore!)
UP_API_TOKEN=up:your-token
```

Install python-dotenv:

```bash
pip install python-dotenv
```

Load it in your application:

```python
from dotenv import load_dotenv
import os
from up_bank_sdk import Client

load_dotenv()  # Load .env file
client = Client(os.environ["UP_API_TOKEN"])
```

### Direct Initialization

For quick scripts or testing:

```python
from up_bank_sdk import Client

client = Client("up:your-token")
```

!!! warning "Avoid Hardcoding"
    Never hardcode your token directly in source code, even for "quick tests". Use environment variables or a `.env` file.

## Verifying Authentication

After initializing your client, verify it works:

```python
from up_bank_sdk import Client

client = Client("up:your-token")

try:
    ping = client.util.ping()
    print(f"Connected! Status: {ping.meta.status_emoji}")
except Exception as e:
    print(f"Authentication failed: {e}")
```

## Token Permissions

The personal access token inherits all permissions from your Up Bank account:

- **Read** account information and transaction history
- **Read** account balances
- **Read** categories and tags
- **Manage** webhooks
- **Modify** transaction categories (if applicable)

## Token Expiration

Up Bank personal access tokens can optionally expire. If your token expires:

1. Create a new token in the Up app
2. Update your environment variable or `.env` file
3. Restart your application

## Security Best Practices

1. **Use environment variables** in production
2. **Use `.env` files** for local development (and add `.env` to `.gitignore`)
3. **Rotate tokens periodically** if your security policy requires it
4. **Monitor API usage** for unexpected activity
5. **Delete unused tokens** from the Up app
