"""Paginated response handling for the Up Bank SDK."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationLinks(BaseModel):
    """Pagination links from API response."""

    prev: str | None = None
    next: str | None = None


class PaginatedResponse(Generic[T]):
    """A page of paginated results with navigation methods.

    Provides access to the current page of results and allows fetching
    subsequent pages via get_next().

    Example usage:
        response = client.transactions.list(page_size=100)
        for tx in response.data:
            print(tx.attributes.description)

        if response.has_more:
            next_page = response.get_next()
            for tx in next_page.data:
                print(tx.attributes.description)
    """

    def __init__(
        self,
        data: list[T],
        links: dict[str, Any],
        fetch_fn: Callable[[str], PaginatedResponse[T]],
    ) -> None:
        self._data = data
        self._links = PaginationLinks(
            prev=links.get("prev"),
            next=links.get("next"),
        )
        self._fetch_fn = fetch_fn

    @property
    def data(self) -> list[T]:
        """The list of items in this page."""
        return self._data

    @property
    def has_more(self) -> bool:
        """True if there is a next page to fetch."""
        return self._links.next is not None

    @property
    def has_prev(self) -> bool:
        """True if there is a previous page."""
        return self._links.prev is not None

    def get_next(self) -> PaginatedResponse[T] | None:
        """Fetch the next page of results.

        Returns:
            PaginatedResponse[T] if there is a next page, None otherwise.
        """
        if not self.has_more:
            return None
        return self._fetch_fn(self._links.next)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[T]:
        """Iterate over items in this page only."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of items in this page."""
        return len(self._data)
