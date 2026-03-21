"""Custom exceptions for the Up Bank SDK."""

from __future__ import annotations


class SDKError(Exception):
    """Base exception for all SDK errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class APIError(SDKError):
    """HTTP error from the API."""

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        errors: list[ErrorDetail] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.errors = errors or []


class ErrorDetail:
    """Detail of an error from the API."""

    def __init__(
        self,
        status: str,
        title: str,
        detail: str,
        *,
        source: ErrorSource | None = None,
    ) -> None:
        self.status = status
        self.title = title
        self.detail = detail
        self.source = source


class ErrorSource:
    """Source of an error from the API."""

    def __init__(
        self,
        *,
        parameter: str | None = None,
        pointer: str | None = None,
    ) -> None:
        self.parameter = parameter
        self.pointer = pointer


class AuthenticationError(APIError):
    """401 Not Authorized - invalid or missing token."""

    pass


class NotFoundError(APIError):
    """404 Not Found - resource does not exist."""

    pass


class InvalidRequestError(APIError):
    """422 Invalid Request - malformed data."""

    pass


class RateLimitError(APIError):
    """429 Too Many Requests."""

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        retry_after: int | None = None,
        errors: list[ErrorDetail] | None = None,
    ) -> None:
        super().__init__(status_code, message, errors=errors)
        self.retry_after = retry_after


class ServerError(APIError):
    """5xx Server Error."""

    pass
