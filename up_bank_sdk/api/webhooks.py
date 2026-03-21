"""Webhooks API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Webhook, WebhookLog
from up_bank_sdk.paginated import PaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import HTTPClientProtocol


class WebhooksResource:
    """API resource for webhooks."""

    def __init__(self, http: HTTPClientProtocol) -> None:
        self._http = http

    def list(
        self,
        *,
        page_size: int | None = None,
    ) -> PaginatedResponse[Webhook]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        def fetch_fn(url: str) -> PaginatedResponse[Webhook]:
            response = self._http.get(url, params={})
            data = response.get("data", [])
            items = [Webhook.model_validate(item) for item in data]
            return PaginatedResponse(
                data=items,
                links=response.get("links", {}),
                fetch_fn=fetch_fn,
            )

        response = self._http.get("/webhooks", params=params)
        data = response.get("data", [])
        items = [Webhook.model_validate(item) for item in data]
        return PaginatedResponse(
            data=items,
            links=response.get("links", {}),
            fetch_fn=fetch_fn,
        )

    def create(
        self,
        url: str,
        *,
        description: str | None = None,
    ) -> Webhook:
        data: dict[str, Any] = {
            "data": {
                "attributes": {
                    "url": url,
                }
            }
        }
        if description is not None:
            data["data"]["attributes"]["description"] = description

        response = self._http.post("/webhooks", json=data)
        return Webhook.model_validate(response.get("data"))

    def get(self, webhook_id: str) -> Webhook:
        response = self._http.get(f"/webhooks/{webhook_id}")
        return Webhook.model_validate(response.get("data"))

    def delete(self, webhook_id: str) -> None:
        self._http.delete(f"/webhooks/{webhook_id}")

    def ping(self, webhook_id: str) -> None:
        self._http.post(f"/webhooks/{webhook_id}/ping")

    def logs(
        self,
        webhook_id: str,
        *,
        page_size: int | None = None,
    ) -> PaginatedResponse[WebhookLog]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        def fetch_fn(url: str) -> PaginatedResponse[WebhookLog]:
            response = self._http.get(url, params={})
            data = response.get("data", [])
            items = [WebhookLog.model_validate(item) for item in data]
            return PaginatedResponse(
                data=items,
                links=response.get("links", {}),
                fetch_fn=fetch_fn,
            )

        response = self._http.get(f"/webhooks/{webhook_id}/logs", params=params)
        data = response.get("data", [])
        items = [WebhookLog.model_validate(item) for item in data]
        return PaginatedResponse(
            data=items,
            links=response.get("links", {}),
            fetch_fn=fetch_fn,
        )
