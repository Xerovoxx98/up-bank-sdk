"""Tests for the Up Bank SDK paginated response."""

from __future__ import annotations

from typing import Any

from up_bank_sdk.paginated import PaginatedResponse


class TestPaginatedResponse:
    """Tests for PaginatedResponse class."""

    def test_empty_response(self) -> None:
        """Test with empty initial response."""

        def fetch_fn(url: str) -> PaginatedResponse[dict[str, Any]]:
            return PaginatedResponse(
                data=[],
                links={"next": None},
                fetch_fn=fetch_fn,
            )

        response = fetch_fn("https://api.example.com/page1")
        assert len(response.data) == 0
        assert response.has_more is False

    def test_single_page(self) -> None:
        """Test with a single page of results."""

        def fetch_fn(url: str) -> PaginatedResponse[dict[str, Any]]:
            return PaginatedResponse(
                data=[{"id": "1"}, {"id": "2"}],
                links={"next": None},
                fetch_fn=fetch_fn,
            )

        response = fetch_fn("https://api.example.com/page1")
        assert len(response.data) == 2
        assert response.data[0]["id"] == "1"
        assert response.data[1]["id"] == "2"
        assert response.has_more is False

    def test_has_more(self) -> None:
        """Test has_more property."""
        response = PaginatedResponse(
            data=[{"id": "1"}],
            links={"next": "https://api.example.com/page2"},
            fetch_fn=lambda url: PaginatedResponse(
                data=[], links={"next": None}, fetch_fn=lambda u: None
            ),  # type: ignore
        )
        assert response.has_more is True

        response2 = PaginatedResponse(
            data=[{"id": "1"}],
            links={"next": None},
            fetch_fn=lambda url: None,  # type: ignore
        )
        assert response2.has_more is False

    def test_has_prev(self) -> None:
        """Test has_prev property."""
        response = PaginatedResponse(
            data=[{"id": "1"}],
            links={"prev": None, "next": None},
            fetch_fn=lambda url: None,  # type: ignore
        )
        assert response.has_prev is False

    def test_iter(self) -> None:
        """Test iteration over data."""
        response = PaginatedResponse(
            data=[{"id": "1"}, {"id": "2"}],
            links={"next": None},
            fetch_fn=lambda url: None,  # type: ignore
        )
        results = list(response)
        assert len(results) == 2
        assert results[0]["id"] == "1"

    def test_len(self) -> None:
        """Test __len__ method."""
        response = PaginatedResponse(
            data=[{"id": "1"}, {"id": "2"}],
            links={"next": None},
            fetch_fn=lambda url: None,  # type: ignore
        )
        assert len(response) == 2

    def test_get_next_returns_none_when_no_more(self) -> None:
        """Test get_next returns None when there is no next page."""

        def fetch_fn(url: str) -> PaginatedResponse[dict[str, Any]]:
            return PaginatedResponse(
                data=[],
                links={"next": None},
                fetch_fn=fetch_fn,
            )

        response = PaginatedResponse(
            data=[{"id": "1"}],
            links={"next": None},
            fetch_fn=fetch_fn,
        )
        assert response.get_next() is None

    def test_get_next_returns_next_page(self) -> None:
        """Test get_next returns the next page."""
        page_count = 0

        def fetch_fn(url: str) -> PaginatedResponse[dict[str, Any]]:
            nonlocal page_count
            page_count += 1
            if page_count == 1:
                return PaginatedResponse(
                    data=[{"id": "1"}],
                    links={"next": "https://api.example.com/page2"},
                    fetch_fn=fetch_fn,
                )
            else:
                return PaginatedResponse(
                    data=[{"id": "2"}],
                    links={"next": None},
                    fetch_fn=fetch_fn,
                )

        response = fetch_fn("https://api.example.com/page1")
        assert len(response.data) == 1
        assert response.data[0]["id"] == "1"

        next_page = response.get_next()
        assert next_page is not None
        assert len(next_page.data) == 1
        assert next_page.data[0]["id"] == "2"
