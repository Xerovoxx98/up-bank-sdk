"""Async tags API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Tag
from up_bank_sdk.paginated_async import AsyncPaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import AsyncHTTPClientProtocol

type TagList = list[str]


class AsyncTagsResource:
    """Async API resource for tags."""

    def __init__(self, http: AsyncHTTPClientProtocol) -> None:
        self._http = http

    async def list(
        self,
        *,
        page_size: int | None = None,
    ) -> AsyncPaginatedResponse[Tag]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        async def fetch_fn(url: str) -> AsyncPaginatedResponse[Tag]:
            resp = await self._http.get(url, params={})
            data = resp.get("data", [])
            items = [Tag.model_validate(item) for item in data]
            return AsyncPaginatedResponse(
                data=items,
                links=resp.get("links", {}),
                fetch_fn=fetch_fn,
            )

        resp = await self._http.get("/tags", params=params)
        data = resp.get("data", [])
        items = [Tag.model_validate(item) for item in data]
        return AsyncPaginatedResponse(
            data=items,
            links=resp.get("links", {}),
            fetch_fn=fetch_fn,
        )

    async def add_tags(
        self,
        transaction_id: str,
        tags: TagList,
    ) -> None:
        data = {
            "data": [{"type": "tags", "id": tag_label} for tag_label in tags],
        }
        await self._http.post(
            f"/transactions/{transaction_id}/relationships/tags",
            json=data,
        )

    async def remove_tags(
        self,
        transaction_id: str,
        tags: TagList,
    ) -> None:
        data = {
            "data": [{"type": "tags", "id": tag_label} for tag_label in tags],
        }
        await self._http.delete(
            f"/transactions/{transaction_id}/relationships/tags",
            json=data,
        )
