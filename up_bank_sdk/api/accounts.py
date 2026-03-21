"""Accounts API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Account, Transaction
from up_bank_sdk.paginated import PaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import HTTPClientProtocol


class AccountsResource:
    """API resource for accounts."""

    def __init__(self, http: HTTPClientProtocol) -> None:
        self._http = http

    def list(
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

        response = self._http.get("/accounts", params=params)
        data = response.get("data", [])
        return [Account.model_validate(item) for item in data]

    def get(self, account_id: str) -> Account:
        response = self._http.get(f"/accounts/{account_id}")
        return Account.model_validate(response.get("data"))

    def list_transactions(
        self,
        account_id: str,
        *,
        page_size: int | None = None,
    ) -> PaginatedResponse[Transaction]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        def fetch_fn(url: str) -> PaginatedResponse[Transaction]:
            response = self._http.get(url, params={})
            data = response.get("data", [])
            items = [Transaction.model_validate(item) for item in data]
            return PaginatedResponse(
                data=items,
                links=response.get("links", {}),
                fetch_fn=fetch_fn,
            )

        response = self._http.get(
            f"/accounts/{account_id}/transactions",
            params=params,
        )
        data = response.get("data", [])
        items = [Transaction.model_validate(item) for item in data]
        return PaginatedResponse(
            data=items,
            links=response.get("links", {}),
            fetch_fn=fetch_fn,
        )
