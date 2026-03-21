"""Tests for the Up Bank SDK exceptions."""

from __future__ import annotations

import pytest

from up_bank_sdk.exceptions import (
    APIError,
    AuthenticationError,
    ErrorDetail,
    ErrorSource,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    SDKError,
    ServerError,
)


class TestSDKError:
    """Tests for SDKError base exception."""

    def test_message_stored(self) -> None:
        """Test that the message is stored correctly."""
        error = SDKError("Something went wrong")
        assert error.message == "Something went wrong"
        assert str(error) == "Something went wrong"


class TestAPIError:
    """Tests for APIError exception."""

    def test_status_code_stored(self) -> None:
        """Test that status code is stored."""
        error = APIError(400, "Bad request")
        assert error.status_code == 400
        assert error.message == "Bad request"

    def test_errors_list(self) -> None:
        """Test errors list initialization."""
        error_detail = ErrorDetail(
            status="422",
            title="Invalid Request",
            detail="The request was invalid",
        )
        error = APIError(422, "Invalid request", errors=[error_detail])
        assert len(error.errors) == 1
        assert error.errors[0].title == "Invalid Request"


class TestAuthenticationError:
    """Tests for AuthenticationError exception."""

    def test_is_api_error(self) -> None:
        """Test that it's an APIError subclass."""
        error = AuthenticationError(401, "Invalid token")
        assert isinstance(error, APIError)
        assert error.status_code == 401


class TestNotFoundError:
    """Tests for NotFoundError exception."""

    def test_is_api_error(self) -> None:
        """Test that it's an APIError subclass."""
        error = NotFoundError(404, "Resource not found")
        assert isinstance(error, APIError)
        assert error.status_code == 404


class TestRateLimitError:
    """Tests for RateLimitError exception."""

    def test_retry_after(self) -> None:
        """Test retry_after is stored."""
        error = RateLimitError(429, "Rate limited", retry_after=60)
        assert error.retry_after == 60

    def test_retry_after_default_none(self) -> None:
        """Test retry_after defaults to None."""
        error = RateLimitError(429, "Rate limited")
        assert error.retry_after is None


class TestServerError:
    """Tests for ServerError exception."""

    def test_is_api_error(self) -> None:
        """Test that it's an APIError subclass."""
        error = ServerError(500, "Internal server error")
        assert isinstance(error, APIError)
        assert error.status_code == 500
