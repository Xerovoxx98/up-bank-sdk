"""Async utility API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from up_bank_sdk.models.resources import UtilPingResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import AsyncHTTPClientProtocol


class AsyncUtilResource:
    """Async API resource for utility endpoints."""

    def __init__(self, http: AsyncHTTPClientProtocol) -> None:
        self._http = http

    async def ping(self) -> UtilPingResponse:
        response = await self._http.get("/util/ping")
        return UtilPingResponse.model_validate(response)
