"""Utility API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from up_bank_sdk.models.resources import UtilPingResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import HTTPClientProtocol


class UtilResource:
    """API resource for utility endpoints."""

    def __init__(self, http: HTTPClientProtocol) -> None:
        self._http = http

    def ping(self) -> UtilPingResponse:
        response = self._http.get("/util/ping")
        return UtilPingResponse.model_validate(response)
