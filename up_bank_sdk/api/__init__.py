"""API module."""

from up_bank_sdk.api.accounts import AccountsResource
from up_bank_sdk.api.attachments import AttachmentsResource
from up_bank_sdk.api.categories import CategoriesResource
from up_bank_sdk.api.tags import TagsResource
from up_bank_sdk.api.transactions import TransactionsResource
from up_bank_sdk.api.util import UtilResource
from up_bank_sdk.api.webhooks import WebhooksResource

__all__ = [
    "AccountsResource",
    "AttachmentsResource",
    "CategoriesResource",
    "TagsResource",
    "TransactionsResource",
    "UtilResource",
    "WebhooksResource",
]
