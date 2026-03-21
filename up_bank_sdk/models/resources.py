"""Resource models for the Up Bank SDK."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from up_bank_sdk.models.base import MoneyObject, UpModel


class AccountAttributes(UpModel):
    """Attributes for an account."""

    display_name: str = Field(alias="displayName")
    account_type: str = Field(alias="accountType")
    ownership_type: str = Field(alias="ownershipType")
    balance: MoneyObject
    created_at: str = Field(alias="createdAt")


class Account(UpModel):
    """Account resource."""

    type: Literal["accounts"] = "accounts"
    id: str
    attributes: AccountAttributes
    relationships: dict[str, Any] | None = None


class HoldInfo(UpModel):
    """Hold info for a pending transaction."""

    amount: MoneyObject
    foreign_amount: MoneyObject | None = Field(default=None, alias="foreignAmount")


class CategoryResourceIdentifier(UpModel):
    """Category resource identifier."""

    type: Literal["categories"] = "categories"
    id: str


class TagResourceIdentifier(UpModel):
    """Tag resource identifier."""

    type: Literal["tags"] = "tags"
    id: str


class MerchantInfo(UpModel):
    """Merchant information."""

    name: str | None = None
    logo: str | None = None


class TransactionAttributes(UpModel):
    """Attributes for a transaction."""

    status: str
    raw_text: str | None = Field(default=None, alias="rawText")
    description: str
    message: str | None = None
    is_categorizable: bool = Field(alias="isCategorizable")
    hold_info: HoldInfo | None = Field(default=None, alias="holdInfo")
    amount: MoneyObject
    foreign_amount: MoneyObject | None = Field(default=None, alias="foreignAmount")
    category: CategoryResourceIdentifier | None = None
    tags: list[TagResourceIdentifier] = Field(default_factory=list)
    created_at: str = Field(alias="createdAt")
    merchant: MerchantInfo | None = None


class TransactionRelationships(UpModel):
    """Relationships for a transaction."""

    account: dict[str, Any] | None = None
    category: dict[str, Any] | None = None
    tags: TransactionTagsRelationship | None = None
    attachment: dict[str, Any] | None = None


class TransactionTagsRelationship(UpModel):
    """Tags relationship wrapper for transactions."""

    data: list[TagResourceIdentifier] = Field(default_factory=list)


class Transaction(UpModel):
    """Transaction resource."""

    type: Literal["transactions"] = "transactions"
    id: str
    attributes: TransactionAttributes
    relationships: TransactionRelationships | None = None


class CategoryAttributes(UpModel):
    """Attributes for a category."""

    name: str


class CategoryParent(UpModel):
    """Parent category reference."""

    data: CategoryResourceIdentifier | None = None
    related: str | None = None


class CategoryChildren(UpModel):
    """Children categories reference."""

    data: list[CategoryResourceIdentifier] = Field(default_factory=list)
    related: str | None = None


class CategoryRelationships(UpModel):
    """Relationships for a category."""

    parent: CategoryParent | None = None
    children: CategoryChildren | None = None


class Category(UpModel):
    """Category resource."""

    type: Literal["categories"] = "categories"
    id: str
    attributes: CategoryAttributes
    relationships: CategoryRelationships | None = None


class TagRelationships(UpModel):
    """Relationships for a tag."""

    transactions: dict[str, Any] | None = None


class Tag(UpModel):
    """Tag resource."""

    type: Literal["tags"] = "tags"
    id: str
    relationships: TagRelationships | None = None


class AttachmentAttributes(UpModel):
    """Attributes for an attachment."""

    created_at: str | None = Field(default=None, alias="createdAt")
    file_url: str | None = Field(default=None, alias="fileURL")
    file_url_expires_at: str | None = Field(default=None, alias="fileURLExpiresAt")
    file_extension: str | None = Field(default=None, alias="fileExtension")
    file_content_type: str | None = Field(default=None, alias="fileContentType")


class AttachmentRelationships(UpModel):
    """Relationships for an attachment."""

    transaction: dict[str, Any] | None = None


class Attachment(UpModel):
    """Attachment resource."""

    type: Literal["attachments"] = "attachments"
    id: str
    attributes: AttachmentAttributes
    relationships: AttachmentRelationships | None = None


class WebhookAttributes(UpModel):
    """Attributes for a webhook."""

    url: str
    description: str | None = None
    secret: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")


class Webhook(UpModel):
    """Webhook resource."""

    type: Literal["webhooks"] = "webhooks"
    id: str
    attributes: WebhookAttributes


class WebhookLogRequest(UpModel):
    """Request portion of a webhook log."""

    uri: str | None = Field(default=None, alias="requestUri")
    method: str | None = Field(default=None, alias="requestMethod")
    headers: dict[str, str] | None = Field(default=None, alias="requestHeaders")
    body: str | None = Field(default=None, alias="requestBody")


class WebhookLogResponseData(UpModel):
    """Response portion of a webhook log."""

    status_code: int | None = Field(default=None, alias="responseStatusCode")
    headers: dict[str, str] | None = Field(default=None, alias="responseHeaders")
    body: str | None = Field(default=None, alias="responseBody")


class WebhookLogAttributes(UpModel):
    """Attributes for a webhook log."""

    request: WebhookLogRequest | None = None
    response: WebhookLogResponseData | None = None
    created_at: str | None = Field(default=None, alias="createdAt")


class WebhookLog(UpModel):
    """Webhook log resource."""

    type: Literal["webhook-delivery-logs"] = "webhook-delivery-logs"
    id: str
    attributes: WebhookLogAttributes


class UtilPingResponse(UpModel):
    """Response from the util/ping endpoint."""

    meta: PingMeta


class PingMeta(UpModel):
    """Meta information for ping response."""

    id: str
    status_emoji: str = Field(alias="statusEmoji")
