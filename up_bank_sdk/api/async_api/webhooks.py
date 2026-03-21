"""Async webhooks API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from up_bank_sdk.models.resources import Webhook, WebhookLog
from up_bank_sdk.paginated_async import AsyncPaginatedResponse

if TYPE_CHECKING:
    from up_bank_sdk._protocols import AsyncHTTPClientProtocol


class AsyncWebhooksResource:
    """Async API resource for webhooks."""

    def __init__(self, http: AsyncHTTPClientProtocol) -> None:
        self._http = http

    async def list(
        self,
        *,
        page_size: int | None = None,
    ) -> AsyncPaginatedResponse[Webhook]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        async def fetch_fn(url: str) -> AsyncPaginatedResponse[Webhook]:
            resp = await self._http.get(url, params={})
            data = resp.get("data", [])
            items = [Webhook.model_validate(item) for item in data]
            return AsyncPaginatedResponse(
                data=items,
                links=resp.get("links", {}),
                fetch_fn=fetch_fn,
            )

        resp = await self._http.get("/webhooks", params=params)
        data = resp.get("data", [])
        items = [Webhook.model_validate(item) for item in data]
        return AsyncPaginatedResponse(
            data=items,
            links=resp.get("links", {}),
            fetch_fn=fetch_fn,
        )

    async def create(
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

        response = await self._http.post("/webhooks", json=data)
        return Webhook.model_validate(response.get("data"))

    async def get(self, webhook_id: str) -> Webhook:
        response = await self._http.get(f"/webhooks/{webhook_id}")
        return Webhook.model_validate(response.get("data"))

    async def delete(self, webhook_id: str) -> None:
        await self._http.delete(f"/webhooks/{webhook_id}")

    async def ping(self, webhook_id: str) -> None:
        await self._http.post(f"/webhooks/{webhook_id}/ping")

    async def logs(
        self,
        webhook_id: str,
        *,
        page_size: int | None = None,
    ) -> AsyncPaginatedResponse[WebhookLog]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page[size]"] = page_size

        async def fetch_fn(url: str) -> AsyncPaginatedResponse[WebhookLog]:
            resp = await self._http.get(url, params={})
            data = resp.get("data", [])
            items = [WebhookLog.model_validate(item) for item in data]
            return AsyncPaginatedResponse(
                data=items,
                links=resp.get("links", {}),
                fetch_fn=fetch_fn,
            )

        resp = await self._http.get(f"/webhooks/{webhook_id}/logs", params=params)
        data = resp.get("data", [])
        items = [WebhookLog.model_validate(item) for item in data]
        return AsyncPaginatedResponse(
            data=items,
            links=resp.get("links", {}),
            fetch_fn=fetch_fn,
        )
