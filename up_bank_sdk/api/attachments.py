"""Attachments API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Attachment
from up_bank_sdk.paginated import PaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import HTTPClientProtocol


class AttachmentsResource:
    """API resource for attachments."""

    def __init__(self, http: HTTPClientProtocol) -> None:
        self._http = http

    def list(
        self,
        *,
        page_size: int | None = None,
    ) -> PaginatedResponse[Attachment]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        def fetch_fn(url: str) -> PaginatedResponse[Attachment]:
            response = self._http.get(url, params={})
            data = response.get("data", [])
            items = [Attachment.model_validate(item) for item in data]
            return PaginatedResponse(
                data=items,
                links=response.get("links", {}),
                fetch_fn=fetch_fn,
            )

        response = self._http.get("/attachments", params=params)
        data = response.get("data", [])
        items = [Attachment.model_validate(item) for item in data]
        return PaginatedResponse(
            data=items,
            links=response.get("links", {}),
            fetch_fn=fetch_fn,
        )

    def get(self, attachment_id: str) -> Attachment:
        response = self._http.get(f"/attachments/{attachment_id}")
        return Attachment.model_validate(response.get("data"))
