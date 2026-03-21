"""Async pagination utilities for the Up Bank SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationLinks(BaseModel):
    """Pagination links from API response."""

    prev: str | None = None
    next: str | None = None


class AsyncPaginatedResponse(Generic[T]):
    """A page of paginated results with navigation methods.

    Provides access to the current page of results and allows fetching
    subsequent pages via get_next() or async iteration.

    Example usage:
        # Explicit pagination
        response = await client.transactions.list(page_size=100)
        for tx in response.data:
            print(tx.attributes.description)
        if response.has_more:
            next_page = await response.get_next()

        # Auto-pagination with async for
        async for tx in client.transactions.list(page_size=100):
            print(tx.attributes.description)
    """

    def __init__(
        self,
        data: list[T],
        links: dict[str, Any],
        fetch_fn: Callable[[str], Awaitable[AsyncPaginatedResponse[T]]],
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

    async def get_next(self) -> AsyncPaginatedResponse[T] | None:
        """Fetch the next page of results.

        Returns:
            AsyncPaginatedResponse[T] if there is a next page, None otherwise.
        """
        if not self.has_more:
            return None
        return await self._fetch_fn(self._links.next)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[T]:
        """Iterate over items in this page only."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of items in this page."""
        return len(self._data)

    async def __aiter__(self) -> AsyncIterator[T]:
        """Async iterator that auto-paginates through all pages."""
        current: AsyncPaginatedResponse[T] | None = self
        while current is not None:
            for item in current._data:
                yield item
            current = await current.get_next()
