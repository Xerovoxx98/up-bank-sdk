"""Synchronous HTTP client with retry logic for the Up Bank SDK."""

from __future__ import annotations

import logging
from typing import Any

import requests  # type: ignore[import-untyped]
from tenacity import (
    RetryCallState,
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from up_bank_sdk.config import Config
from up_bank_sdk.exceptions import (
    APIError,
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

logger = logging.getLogger(__name__)


def _retry_if_retryable(call_state: RetryCallState) -> bool:
    if call_state.outcome is None:
        return False
    exc = call_state.outcome.exception()
    if exc is None:
        return False
    return isinstance(exc, (RateLimitError, ServerError))


class SyncHTTPClient:
    """Synchronous HTTP client for the Up Bank API."""

    def __init__(self, config: Config, api_key: str) -> None:
        self._config = config
        self._api_key = api_key
        self._session: requests.Session | None = None

    def _get_session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(
                {
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
            )
        return self._session

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        status = response.status_code

        if status == 200 or status == 201:
            return response.json()  # type: ignore[no-any-return]

        if status == 204:
            return {}

        if status == 401:
            raise AuthenticationError(
                status,
                "Authentication failed. Check your API token.",
            )

        if status == 404:
            raise NotFoundError(
                status,
                "Resource not found.",
            )

        if status == 422:
            try:
                json_body = response.json() if response.content else {}
            except Exception:
                json_body = {}
            errors = json_body.get("errors", [])
            raise InvalidRequestError(
                status,
                "Invalid request.",
                errors=errors,
            )

        if status == 429:
            try:
                retry_after_str = response.headers.get("Retry-After", "0")
                retry_after = int(retry_after_str) if retry_after_str else None
            except (ValueError, TypeError):
                retry_after = None
            raise RateLimitError(
                status,
                "Rate limit exceeded.",
                retry_after=retry_after,
            )

        if status >= 500:
            raise ServerError(
                status,
                f"Server error: {status}",
            )

        raise APIError(
            status,
            f"Unexpected error: {status}",
        )

    def _do_request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        session = self._get_session()
        response = session.request(
            method,
            url,
            timeout=self._config.timeout,
            **kwargs,
        )
        return self._handle_response(response)

    def _make_url(self, path: str) -> str:
        """Build full URL from path. Handles both relative paths and full URLs."""
        if path.startswith("http"):
            return path
        return f"{self._config.base_url}{path}"

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)
        decorated = retry(
            retry=_retry_if_retryable,
            wait=wait_exponential(
                multiplier=self._config.retry_wait_multiplier,
                min=self._config.retry_wait_min,
                max=self._config.retry_wait_max,
            ),
            stop=stop_after_attempt(self._config.max_retries),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )(self._do_request)
        return decorated("GET", url, **kwargs)

    def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)
        decorated = retry(
            retry=_retry_if_retryable,
            wait=wait_exponential(
                multiplier=self._config.retry_wait_multiplier,
                min=self._config.retry_wait_min,
                max=self._config.retry_wait_max,
            ),
            stop=stop_after_attempt(self._config.max_retries),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )(self._do_request)
        return decorated("POST", url, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)
        decorated = retry(
            retry=_retry_if_retryable,
            wait=wait_exponential(
                multiplier=self._config.retry_wait_multiplier,
                min=self._config.retry_wait_min,
                max=self._config.retry_wait_max,
            ),
            stop=stop_after_attempt(self._config.max_retries),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )(self._do_request)
        return decorated("PATCH", url, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)
        decorated = retry(
            retry=_retry_if_retryable,
            wait=wait_exponential(
                multiplier=self._config.retry_wait_multiplier,
                min=self._config.retry_wait_min,
                max=self._config.retry_wait_max,
            ),
            stop=stop_after_attempt(self._config.max_retries),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True,
        )(self._do_request)
        return decorated("DELETE", url, **kwargs)

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._session is not None:
            self._session.close()
            self._session = None

    def __enter__(self) -> SyncHTTPClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        self.close()
