"""Tests for async pagination."""

from __future__ import annotations

import pytest

from up_bank_sdk.paginated_async import AsyncPaginatedResponse


class TestAsyncPaginatedResponse:
    """Tests for AsyncPaginatedResponse class."""

    def test_empty_response(self) -> None:
        """Test with empty initial response."""

        def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[],
                links={"next": None},
                fetch_fn=fetch_fn,  # type: ignore
            )

        response = AsyncPaginatedResponse(
            data=[],
            links={"next": None},
            fetch_fn=fetch_fn,  # type: ignore
        )
        assert len(response.data) == 0
        assert response.has_more is False

    def test_single_page(self) -> None:
        """Test with a single page of results."""

        def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[{"id": "1"}, {"id": "2"}],
                links={"next": None},
                fetch_fn=fetch_fn,  # type: ignore
            )

        response = AsyncPaginatedResponse(
            data=[{"id": "1"}, {"id": "2"}],
            links={"next": None},
            fetch_fn=fetch_fn,  # type: ignore
        )
        assert len(response.data) == 2
        assert response.data[0]["id"] == "1"
        assert response.data[1]["id"] == "2"
        assert response.has_more is False

    def test_has_more(self) -> None:
        """Test has_more property."""

        def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[{"id": "1"}],
                links={"next": "https://api.example.com/page2"},
                fetch_fn=fetch_fn,  # type: ignore
            )

        response = AsyncPaginatedResponse(
            data=[{"id": "1"}],
            links={"next": "https://api.example.com/page2"},
            fetch_fn=fetch_fn,  # type: ignore
        )
        assert response.has_more is True

    def test_has_prev(self) -> None:
        """Test has_prev property."""

        def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[{"id": "1"}],
                links={"prev": None, "next": None},
                fetch_fn=fetch_fn,  # type: ignore
            )

        response = AsyncPaginatedResponse(
            data=[{"id": "1"}],
            links={"prev": None, "next": None},
            fetch_fn=fetch_fn,  # type: ignore
        )
        assert response.has_prev is False

    def test_iter(self) -> None:
        """Test iteration over data."""

        def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[{"id": "1"}, {"id": "2"}],
                links={"next": None},
                fetch_fn=fetch_fn,  # type: ignore
            )

        response = AsyncPaginatedResponse(
            data=[{"id": "1"}, {"id": "2"}],
            links={"next": None},
            fetch_fn=fetch_fn,  # type: ignore
        )
        results = list(response)
        assert len(results) == 2
        assert results[0]["id"] == "1"

    def test_len(self) -> None:
        """Test __len__ method."""

        def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[{"id": "1"}, {"id": "2"}],
                links={"next": None},
                fetch_fn=fetch_fn,  # type: ignore
            )

        response = AsyncPaginatedResponse(
            data=[{"id": "1"}, {"id": "2"}],
            links={"next": None},
            fetch_fn=fetch_fn,  # type: ignore
        )
        assert len(response) == 2

    @pytest.mark.asyncio
    async def test_get_next_returns_none_when_no_more(self) -> None:
        """Test get_next returns None when there is no next page."""

        async def fetch_fn(url: str) -> AsyncPaginatedResponse[dict[str, object]]:
            return AsyncPaginatedResponse(
                data=[],
                links={"next": None},
                fetch_fn=fetch_fn,
            )

        response = AsyncPaginatedResponse(
            data=[{"id": "1"}],
            links={"next": None},
            fetch_fn=fetch_fn,
        )
        result = await response.get_next()
        assert result is None

    @pytest.mark.skip(reason="Async pagination is tested via integration tests")
    @pytest.mark.asyncio
    async def test_get_next_returns_next_page(self) -> None:
        """Test get_next returns the next page via integration tests."""
        pass
