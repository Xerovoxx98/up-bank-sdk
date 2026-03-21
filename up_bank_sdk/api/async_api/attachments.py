"""Async attachments API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Attachment
from up_bank_sdk.paginated_async import AsyncPaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import AsyncHTTPClientProtocol


class AsyncAttachmentsResource:
    """Async API resource for attachments."""

    def __init__(self, http: AsyncHTTPClientProtocol) -> None:
        self._http = http

    async def list(
        self,
        *,
        page_size: int | None = None,
    ) -> AsyncPaginatedResponse[Attachment]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        async def fetch_fn(url: str) -> AsyncPaginatedResponse[Attachment]:
            resp = await self._http.get(url, params={})
            data = resp.get("data", [])
            items = [Attachment.model_validate(item) for item in data]
            return AsyncPaginatedResponse(
                data=items,
                links=resp.get("links", {}),
                fetch_fn=fetch_fn,
            )

        resp = await self._http.get("/attachments", params=params)
        data = resp.get("data", [])
        items = [Attachment.model_validate(item) for item in data]
        return AsyncPaginatedResponse(
            data=items,
            links=resp.get("links", {}),
            fetch_fn=fetch_fn,
        )

    async def get(self, attachment_id: str) -> Attachment:
        response = await self._http.get(f"/attachments/{attachment_id}")
        return Attachment.model_validate(response.get("data"))
