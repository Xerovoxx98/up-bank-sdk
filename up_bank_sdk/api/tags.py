"""Tags API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Tag
from up_bank_sdk.paginated import PaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import HTTPClientProtocol

type TagList = list[str]


class TagsResource:
    """API resource for tags."""

    def __init__(self, http: HTTPClientProtocol) -> None:
        self._http = http

    def list(
        self,
        *,
        page_size: int | None = None,
    ) -> PaginatedResponse[Tag]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        def fetch_fn(url: str) -> PaginatedResponse[Tag]:
            response = self._http.get(url, params={})
            data = response.get("data", [])
            items = [Tag.model_validate(item) for item in data]
            return PaginatedResponse(
                data=items,
                links=response.get("links", {}),
                fetch_fn=fetch_fn,
            )

        response = self._http.get("/tags", params=params)
        data = response.get("data", [])
        items = [Tag.model_validate(item) for item in data]
        return PaginatedResponse(
            data=items,
            links=response.get("links", {}),
            fetch_fn=fetch_fn,
        )

    def add_tags(
        self,
        transaction_id: str,
        tags: TagList,
    ) -> None:
        data = {
            "data": [{"type": "tags", "id": tag_label} for tag_label in tags],
        }
        self._http.post(
            f"/transactions/{transaction_id}/relationships/tags",
            json=data,
        )

    def remove_tags(
        self,
        transaction_id: str,
        tags: TagList,
    ) -> None:
        data = {
            "data": [{"type": "tags", "id": tag_label} for tag_label in tags],
        }
        self._http.delete(
            f"/transactions/{transaction_id}/relationships/tags",
            json=data,
        )
