"""Async categories API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Category

if TYPE_CHECKING:
    from up_bank_sdk._protocols import AsyncHTTPClientProtocol


class AsyncCategoriesResource:
    """Async API resource for categories."""

    def __init__(self, http: AsyncHTTPClientProtocol) -> None:
        self._http = http

    async def list(
        self,
        *,
        parent: str | None = None,
    ) -> list[Category]:
        params: dict[str, Any] = {}
        if parent is not None:
            params["filter[parent]"] = parent

        response = await self._http.get("/categories", params=params)
        data = response.get("data", [])
        return [Category.model_validate(item) for item in data]

    async def get(self, category_id: str) -> Category:
        response = await self._http.get(f"/categories/{category_id}")
        return Category.model_validate(response.get("data"))
