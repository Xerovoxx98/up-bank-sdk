"""Main client for the Up Bank SDK."""

from __future__ import annotations

from up_bank_sdk.api import (
    AccountsResource,
    AttachmentsResource,
    CategoriesResource,
    TagsResource,
    TransactionsResource,
    UtilResource,
    WebhooksResource,
)
from up_bank_sdk.config import Config
from up_bank_sdk.http.sync_client import SyncHTTPClient


class Client:
    """Main client for interacting with the Up Bank API."""

    def __init__(
        self,
        api_key: str,
        *,
        config: Config | None = None,
    ) -> None:
        self._config = config or Config()
        self._http = SyncHTTPClient(self._config, api_key)

        self.accounts = AccountsResource(self._http)
        self.transactions = TransactionsResource(self._http)
        self.categories = CategoriesResource(self._http)
        self.tags = TagsResource(self._http)
        self.attachments = AttachmentsResource(self._http)
        self.webhooks = WebhooksResource(self._http)
        self.util = UtilResource(self._http)

    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()
