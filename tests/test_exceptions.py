"""Tests for the Up Bank SDK exceptions."""

from __future__ import annotations

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


class TestInvalidRequestError:
    """Tests for InvalidRequestError exception."""

    def test_is_api_error(self) -> None:
        """Test that it's an APIError subclass."""
        error = InvalidRequestError(422, "Invalid request")
        assert isinstance(error, APIError)
        assert error.status_code == 422

    def test_errors_stored(self) -> None:
        """Test that errors list is stored."""
        error_detail = ErrorDetail(
            status="422",
            title="Validation Error",
            detail="Field is required",
        )
        error = InvalidRequestError(422, "Invalid request", errors=[error_detail])
        assert len(error.errors) == 1
        assert error.errors[0].detail == "Field is required"


class TestErrorDetail:
    """Tests for ErrorDetail class."""

    def test_attributes_stored(self) -> None:
        """Test that all attributes are stored."""
        source = ErrorSource(parameter="amount", pointer="/data/amount")
        detail = ErrorDetail(
            status="422",
            title="Invalid Value",
            detail="Amount must be positive",
            source=source,
        )
        assert detail.status == "422"
        assert detail.title == "Invalid Value"
        assert detail.detail == "Amount must be positive"
        assert detail.source is not None
        assert detail.source.parameter == "amount"
        assert detail.source.pointer == "/data/amount"

    def test_source_optional(self) -> None:
        """Test that source is optional."""
        detail = ErrorDetail(
            status="422",
            title="Invalid Value",
            detail="Amount must be positive",
        )
        assert detail.source is None


class TestErrorSource:
    """Tests for ErrorSource class."""

    def test_parameter_only(self) -> None:
        """Test ErrorSource with only parameter."""
        source = ErrorSource(parameter="amount")
        assert source.parameter == "amount"
        assert source.pointer is None

    def test_pointer_only(self) -> None:
        """Test ErrorSource with only pointer."""
        source = ErrorSource(pointer="/data/amount")
        assert source.pointer == "/data/amount"
        assert source.parameter is None

    def test_both_none(self) -> None:
        """Test ErrorSource with both None."""
        source = ErrorSource()
        assert source.parameter is None
        assert source.pointer is None
