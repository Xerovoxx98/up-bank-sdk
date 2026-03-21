"""Async accounts API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Account, Transaction
from up_bank_sdk.paginated_async import AsyncPaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import AsyncHTTPClientProtocol


class AsyncAccountsResource:
    """Async API resource for accounts."""

    def __init__(self, http: AsyncHTTPClientProtocol) -> None:
        self._http = http

    async def list(
        self,
        *,
        page_size: int | None = None,
        account_type: str | None = None,
        ownership_type: str | None = None,
    ) -> list[Account]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size
        if account_type is not None:
            params["filter[accountType]"] = account_type
        if ownership_type is not None:
            params["filter[ownershipType]"] = ownership_type

        response = await self._http.get("/accounts", params=params)
        data = response.get("data", [])
        return [Account.model_validate(item) for item in data]

    async def get(self, account_id: str) -> Account:
        response = await self._http.get(f"/accounts/{account_id}")
        return Account.model_validate(response.get("data"))

    async def list_transactions(
        self,
        account_id: str,
        *,
        page_size: int | None = None,
    ) -> AsyncPaginatedResponse[Transaction]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        async def fetch_fn(url: str) -> AsyncPaginatedResponse[Transaction]:
            resp = await self._http.get(url, params={})
            data = resp.get("data", [])
            items = [Transaction.model_validate(item) for item in data]
            return AsyncPaginatedResponse(
                data=items,
                links=resp.get("links", {}),
                fetch_fn=fetch_fn,
            )

        resp = await self._http.get(
            f"/accounts/{account_id}/transactions",
            params=params,
        )
        data = resp.get("data", [])
        items = [Transaction.model_validate(item) for item in data]
        return AsyncPaginatedResponse(
            data=items,
            links=resp.get("links", {}),
            fetch_fn=fetch_fn,
        )
