"""Async client for the Up Bank SDK."""

from __future__ import annotations

from up_bank_sdk.api.async_api import (
    AsyncAccountsResource,
    AsyncAttachmentsResource,
    AsyncCategoriesResource,
    AsyncTagsResource,
    AsyncTransactionsResource,
    AsyncUtilResource,
    AsyncWebhooksResource,
)
from up_bank_sdk.config import Config
from up_bank_sdk.http.async_client import AsyncHTTPClient


class AsyncClient:
    """Async client for interacting with the Up Bank API.

    Usage:
        async with AsyncClient("up:token") as client:
            response = await client.transactions.list(page_size=100)
            for tx in response.data:
                print(tx.attributes.description)

            # Or use auto-pagination:
            async for tx in client.transactions.list(page_size=100):
                print(tx.attributes.description)
    """

    def __init__(
        self,
        api_key: str,
        *,
        config: Config | None = None,
    ) -> None:
        self._config = config or Config()
        self._http = AsyncHTTPClient(self._config, api_key)

        self.accounts = AsyncAccountsResource(self._http)
        self.transactions = AsyncTransactionsResource(self._http)
        self.categories = AsyncCategoriesResource(self._http)
        self.tags = AsyncTagsResource(self._http)
        self.attachments = AsyncAttachmentsResource(self._http)
        self.webhooks = AsyncWebhooksResource(self._http)
        self.util = AsyncUtilResource(self._http)

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        await self._http.close()
