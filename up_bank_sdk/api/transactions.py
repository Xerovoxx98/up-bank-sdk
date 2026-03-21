"""Transactions API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Transaction
from up_bank_sdk.paginated import PaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import HTTPClientProtocol


class TransactionsResource:
    """API resource for transactions."""

    def __init__(self, http: HTTPClientProtocol) -> None:
        self._http = http

    def list(
        self,
        *,
        page_size: int | None = None,
        status: str | None = None,
        since: str | None = None,
        until: str | None = None,
        category: str | None = None,
        tag: str | None = None,
    ) -> PaginatedResponse[Transaction]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size
        if status is not None:
            params["filter[status]"] = status
        if since is not None:
            params["filter[since]"] = since
        if until is not None:
            params["filter[until]"] = until
        if category is not None:
            params["filter[category]"] = category
        if tag is not None:
            params["filter[tag]"] = tag

        def fetch_fn(url: str) -> PaginatedResponse[Transaction]:
            response = self._http.get(url, params={})
            data = response.get("data", [])
            items = [Transaction.model_validate(item) for item in data]
            return PaginatedResponse(
                data=items,
                links=response.get("links", {}),
                fetch_fn=fetch_fn,
            )

        response = self._http.get("/transactions", params=params)
        data = response.get("data", [])
        items = [Transaction.model_validate(item) for item in data]
        return PaginatedResponse(
            data=items,
            links=response.get("links", {}),
            fetch_fn=fetch_fn,
        )

    def get(self, transaction_id: str) -> Transaction:
        response = self._http.get(f"/transactions/{transaction_id}")
        return Transaction.model_validate(response.get("data"))

    def categorize(
        self,
        transaction_id: str,
        category_id: str | None,
    ) -> None:
        data: dict[str, Any] = {"data": None}
        if category_id is not None:
            data["data"] = {"type": "categories", "id": category_id}

        self._http.patch(
            f"/transactions/{transaction_id}/relationships/category",
            json=data,
        )
