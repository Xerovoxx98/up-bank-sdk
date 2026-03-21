"""Tests for the Up Bank SDK models."""

from __future__ import annotations

import pytest

from up_bank_sdk.models.resources import (
    Account,
    AccountAttributes,
    Attachment,
    AttachmentAttributes,
    Category,
    CategoryAttributes,
    CategoryChildren,
    CategoryParent,
    HoldInfo,
    MoneyObject,
    PingMeta,
    Tag,
    TagResourceIdentifier,
    Transaction,
    TransactionAttributes,
    TransactionRelationships,
    UtilPingResponse,
    Webhook,
    WebhookAttributes,
    WebhookLog,
    WebhookLogAttributes,
    WebhookLogRequest,
    WebhookLogResponseData,
)


class TestMoneyObject:
    """Tests for MoneyObject model."""

    def test_parse_minimal(self) -> None:
        """Test parsing a minimal money object."""
        data = {
            "currencyCode": "AUD",
            "value": "10.50",
            "valueInBaseUnits": 1050,
        }
        money = MoneyObject.model_validate(data)
        assert money.currency_code == "AUD"
        assert money.value == "10.50"
        assert money.value_in_base_units == 1050

    def test_extra_fields_ignored(self) -> None:
        """Test that extra fields are ignored."""
        data = {
            "currencyCode": "AUD",
            "value": "10.50",
            "valueInBaseUnits": 1050,
            "extraField": "should be ignored",
        }
        money = MoneyObject.model_validate(data)
        assert not hasattr(money, "extra_field")


class TestAccount:
    """Tests for Account model."""

    def test_parse_account(self) -> None:
        """Test parsing a full account response."""
        data = {
            "type": "accounts",
            "id": "abc123",
            "attributes": {
                "displayName": "Spending",
                "accountType": "TRANSACTIONAL",
                "ownershipType": "INDIVIDUAL",
                "balance": {
                    "currencyCode": "AUD",
                    "value": "100.00",
                    "valueInBaseUnits": 10000,
                },
                "createdAt": "2024-01-01T00:00:00+11:00",
            },
            "relationships": {},
            "links": {
                "self": "https://api.up.com.au/api/v1/accounts/abc123",
            },
        }
        account = Account.model_validate(data)
        assert account.type == "accounts"
        assert account.id == "abc123"
        assert account.attributes.display_name == "Spending"
        assert account.attributes.account_type == "TRANSACTIONAL"
        assert account.attributes.balance.value == "100.00"


class TestTransaction:
    """Tests for Transaction model."""

    def test_parse_transaction(self) -> None:
        """Test parsing a transaction response."""
        data = {
            "type": "transactions",
            "id": "tx123",
            "attributes": {
                "status": "SETTLED",
                "rawText": "UBER TRIP",
                "description": "Uber Trip",
                "message": None,
                "isCategorizable": True,
                "holdInfo": None,
                "amount": {
                    "currencyCode": "AUD",
                    "value": "-25.00",
                    "valueInBaseUnits": -2500,
                },
                "foreignAmount": None,
                "category": {
                    "type": "categories",
                    "id": "transport",
                },
                "tags": [],
                "createdAt": "2024-01-01T12:00:00+11:00",
                "merchant": {
                    "name": "Uber",
                    "logo": "https://example.com/uber.png",
                },
            },
            "relationships": {
                "account": {
                    "data": {"type": "accounts", "id": "acc123"},
                },
                "category": {
                    "data": {"type": "categories", "id": "transport"},
                },
                "tags": {"data": []},
                "attachment": None,
            },
        }
        tx = Transaction.model_validate(data)
        assert tx.type == "transactions"
        assert tx.id == "tx123"
        assert tx.attributes.status == "SETTLED"
        assert tx.attributes.description == "Uber Trip"
        assert tx.attributes.amount.value == "-25.00"
        assert tx.attributes.merchant.name == "Uber"

    def test_parse_hold_info(self) -> None:
        """Test parsing a held/pending transaction."""
        data = {
            "type": "transactions",
            "id": "tx456",
            "attributes": {
                "status": "HELD",
                "rawText": None,
                "description": "Pending Purchase",
                "message": None,
                "isCategorizable": True,
                "holdInfo": {
                    "amount": {
                        "currencyCode": "AUD",
                        "value": "-50.00",
                        "valueInBaseUnits": -5000,
                    },
                    "foreignAmount": None,
                },
                "amount": {
                    "currencyCode": "AUD",
                    "value": "-50.00",
                    "valueInBaseUnits": -5000,
                },
                "foreignAmount": None,
                "category": None,
                "tags": [],
                "createdAt": "2024-01-01T12:00:00+11:00",
                "merchant": None,
            },
            "relationships": {},
        }
        tx = Transaction.model_validate(data)
        assert tx.attributes.status == "HELD"
        assert tx.attributes.hold_info is not None
        assert tx.attributes.hold_info.amount.value == "-50.00"


class TestCategory:
    """Tests for Category model."""

    def test_parse_category(self) -> None:
        """Test parsing a category response."""
        data = {
            "type": "categories",
            "id": "good-life",
            "attributes": {
                "name": "Good Life",
            },
            "relationships": {
                "parent": {"data": None},
                "children": {
                    "data": [
                        {"type": "categories", "id": "hobbies"},
                        {"type": "categories", "id": "restaurants-and-cafes"},
                    ],
                    "related": "https://api.up.com.au/api/v1/categories?filter[parent]=good-life",
                },
            },
            "links": {
                "self": "https://api.up.com.au/api/v1/categories/good-life",
            },
        }
        cat = Category.model_validate(data)
        assert cat.type == "categories"
        assert cat.id == "good-life"
        assert cat.attributes.name == "Good Life"
        assert cat.relationships.parent.data is None
        assert len(cat.relationships.children.data) == 2


class TestUtilPing:
    """Tests for util/ping response."""

    def test_parse_ping(self) -> None:
        """Test parsing ping response."""
        data = {
            "meta": {
                "id": "3b5d17a4-6778-48dc-ae7d-9f8aace2e2fc",
                "statusEmoji": "⚡️",
            }
        }
        response = UtilPingResponse.model_validate(data)
        assert response.meta.id == "3b5d17a4-6778-48dc-ae7d-9f8aace2e2fc"
        assert response.meta.status_emoji == "⚡️"
