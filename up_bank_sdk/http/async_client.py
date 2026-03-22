"""Asynchronous HTTP client with retry logic for the Up Bank SDK."""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any

import httpx
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


class AsyncHTTPClient:
    """Asynchronous HTTP client for the Up Bank API."""

    def __init__(self, config: Config, api_key: str) -> None:
        self._config = config
        self._api_key = api_key
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                timeout=self._config.timeout,
            )
        return self._client

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
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
            except ValueError:
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

    async def _do_request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        client = await self._get_client()
        response = await client.request(
            method,
            url,
            **kwargs,
        )
        return self._handle_response(response)

    def _make_url(self, path: str) -> str:
        """Build full URL from path. Handles both relative paths and full URLs."""
        if path.startswith("http"):
            return path
        return f"{self._config.base_url}{path}"

    async def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)

        async def _do_get() -> dict[str, Any]:
            return await self._do_request("GET", url, **kwargs)

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
        )(_do_get)
        return await decorated()

    async def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)

        async def _do_post() -> dict[str, Any]:
            return await self._do_request("POST", url, **kwargs)

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
        )(_do_post)
        return await decorated()

    async def patch(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)

        async def _do_patch() -> dict[str, Any]:
            return await self._do_request("PATCH", url, **kwargs)

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
        )(_do_patch)
        return await decorated()

    async def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self._make_url(path)

        async def _do_delete() -> dict[str, Any]:
            return await self._do_request("DELETE", url, **kwargs)

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
        )(_do_delete)
        return await decorated()

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> AsyncHTTPClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
