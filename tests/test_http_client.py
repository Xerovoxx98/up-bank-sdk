"""Tests for the HTTP clients."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from up_bank_sdk.config import Config
from up_bank_sdk.exceptions import (
    APIError,
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from up_bank_sdk.http.sync_client import SyncHTTPClient


class TestSyncHTTPClient:
    """Tests for SyncHTTPClient."""

    @pytest.fixture
    def config(self) -> Config:
        """Create a test config."""
        return Config()

    @pytest.fixture
    def client(self, config: Config) -> SyncHTTPClient:
        """Create a test client."""
        return SyncHTTPClient(config, "test-api-key")

    def test_context_manager(self, client: SyncHTTPClient) -> None:
        """Test that client can be used as context manager."""
        with client as c:
            assert c is client
        # Session should be closed after exiting context

    def test_close_closes_session(self, client: SyncHTTPClient) -> None:
        """Test that close() closes the session."""
        client._get_session()
        client.close()
        assert client._session is None

    def test_close_idempotent(self, client: SyncHTTPClient) -> None:
        """Test that close() can be called multiple times."""
        client.close()
        client.close()  # Should not raise

    def test_authentication_error_401(self, client: SyncHTTPClient) -> None:
        """Test that 401 raises AuthenticationError."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.content = b""

        with pytest.raises(AuthenticationError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 401

    def test_not_found_error_404(self, client: SyncHTTPClient) -> None:
        """Test that 404 raises NotFoundError."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b""

        with pytest.raises(NotFoundError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 404

    def test_invalid_request_error_422(self, client: SyncHTTPClient) -> None:
        """Test that 422 raises InvalidRequestError."""
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.content = b'{"errors": [{"title": "Bad"}]}'
        mock_response.json.return_value = {"errors": [{"title": "Bad"}]}

        with pytest.raises(InvalidRequestError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 422
        assert len(exc_info.value.errors) == 1

    def test_invalid_request_error_422_malformed_json(self, client: SyncHTTPClient) -> None:
        """Test that 422 with malformed JSON raises InvalidRequestError."""
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.content = b"not json"
        mock_response.json.side_effect = Exception("JSON decode error")

        with pytest.raises(InvalidRequestError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 422
        assert exc_info.value.errors == []

    def test_rate_limit_error_429(self, client: SyncHTTPClient) -> None:
        """Test that 429 raises RateLimitError."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.content = b""
        mock_response.headers.get.return_value = "60"

        with pytest.raises(RateLimitError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60

    def test_rate_limit_error_429_invalid_retry_after(self, client: SyncHTTPClient) -> None:
        """Test that 429 with invalid Retry-After sets retry_after to None."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.content = b""
        mock_response.headers.get.return_value = "not-a-number"

        with pytest.raises(RateLimitError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after is None

    def test_rate_limit_error_429_missing_header(self, client: SyncHTTPClient) -> None:
        """Test that 429 without Retry-After header sets retry_after to None."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.content = b""
        mock_response.headers.get.return_value = None

        with pytest.raises(RateLimitError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after is None

    def test_server_error_500(self, client: SyncHTTPClient) -> None:
        """Test that 500 raises ServerError."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b""

        with pytest.raises(ServerError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 500

    def test_server_error_503(self, client: SyncHTTPClient) -> None:
        """Test that 503 raises ServerError."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.content = b""

        with pytest.raises(ServerError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 503

    def test_api_error_unknown_status(self, client: SyncHTTPClient) -> None:
        """Test that unknown status raises APIError."""
        mock_response = MagicMock()
        mock_response.status_code = 418
        mock_response.content = b""

        with pytest.raises(APIError) as exc_info:
            client._handle_response(mock_response)
        assert exc_info.value.status_code == 418

    def test_successful_response_200(self, client: SyncHTTPClient) -> None:
        """Test that 200 returns JSON data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}

        result = client._handle_response(mock_response)
        assert result == {"data": "test"}

    def test_successful_response_201(self, client: SyncHTTPClient) -> None:
        """Test that 201 returns JSON data."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": "created"}

        result = client._handle_response(mock_response)
        assert result == {"data": "created"}

    def test_successful_response_204(self, client: SyncHTTPClient) -> None:
        """Test that 204 returns empty dict."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = b""

        result = client._handle_response(mock_response)
        assert result == {}
