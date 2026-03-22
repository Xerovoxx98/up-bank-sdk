"""Tests for the main Client."""

from __future__ import annotations

from unittest.mock import patch

from up_bank_sdk.client import Client
from up_bank_sdk.config import Config


class TestClientContextManager:
    """Tests for Client context manager support."""

    def test_context_manager_enters(self) -> None:
        """Test that client can be used with context manager."""
        with Client("test-api-key") as client:
            assert client is not None
            assert isinstance(client, Client)

    def test_context_manager_exits_and_closes(self) -> None:
        """Test that context manager exits and closes the client."""
        client = Client("test-api-key")
        with patch.object(client._http, "close") as mock_close:
            with client:
                pass
            mock_close.assert_called_once()

    def test_close_closes_http_client(self) -> None:
        """Test that close() closes the HTTP client."""
        client = Client("test-api-key")
        with patch.object(client._http, "close") as mock_close:
            client.close()
            mock_close.assert_called_once()

    def test_close_idempotent(self) -> None:
        """Test that close() can be called multiple times."""
        client = Client("test-api-key")
        with patch.object(client._http, "close"):
            client.close()
            client.close()  # Should not raise

    def test_client_with_config(self) -> None:
        """Test that client accepts custom config."""
        config = Config(timeout=60.0)
        with Client("test-api-key", config=config) as client:
            assert client._config.timeout == 60.0

    def test_client_resources_initialized(self) -> None:
        """Test that all resources are initialized."""
        client = Client("test-api-key")
        assert client.accounts is not None
        assert client.transactions is not None
        assert client.categories is not None
        assert client.tags is not None
        assert client.attachments is not None
        assert client.webhooks is not None
        assert client.util is not None
