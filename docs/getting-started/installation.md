# Installation

## Requirements

- Python 3.12 or higher
- UV (recommended) or pip

## Install from PyPI

=== "UV (Recommended)"

    ```bash
    uv pip install up-bank-sdk
    ```

=== "pip"

    ```bash
    pip install up-bank-sdk
    ```

## Install with Development Dependencies

For local development:

=== "UV"

    ```bash
    uv pip install up-bank-sdk[dev]
    ```

=== "pip"

    ```bash
    pip install up-bank-sdk[dev]
    ```

This installs:
- `pytest` — Testing framework
- `pytest-cov` — Coverage reporting
- `pytest-asyncio` — Async test support
- `ruff` — Linting
- `mypy` — Type checking

## Install from Source

Clone the repository and install in editable mode:

=== "UV"

    ```bash
    git clone https://github.com/Xerovoxx98/up-bank-sdk.git
    cd up-bank-sdk
    uv pip install -e ".[dev]"
    ```

=== "pip"

    ```bash
    git clone https://github.com/Xerovoxx98/up-bank-sdk.git
    cd up-bank-sdk
    pip install -e ".[dev]"
    ```

## Verify Installation

```python
import up_bank_sdk
print(up_bank_sdk.__version__)
```

## Dependencies

The package automatically installs:

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.31.0 | Synchronous HTTP client |
| `httpx` | >=0.27.0 | Asynchronous HTTP client |
| `pydantic` | >=2.0.0 | Data validation and serialization |
| `tenacity` | >=8.0.0 | Retry logic with exponential backoff |

## Next Steps

Once installed, proceed to [Quick Start](quickstart.md) to make your first API call.
