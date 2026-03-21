"""Protocol definitions for HTTP clients.

This module defines the interfaces that both sync and async HTTP clients
must implement, allowing API resources to be written once and used with
either client type.
"""

from __future__ import annotations

from typing import Any, Protocol


class HTTPClientProtocol(Protocol):
    """Protocol for sync HTTP clients used by API resources."""

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send GET request to the given path."""
        ...

    def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send POST request to the given path."""
        ...

    def patch(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send PATCH request to the given path."""
        ...

    def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send DELETE request to the given path."""
        ...


class AsyncHTTPClientProtocol(Protocol):
    """Protocol for async HTTP clients used by async API resources."""

    async def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send GET request to the given path."""
        ...

    async def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send POST request to the given path."""
        ...

    async def patch(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send PATCH request to the given path."""
        ...

    async def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send DELETE request to the given path."""
        ...
