#!/usr/bin/env python3
"""Integration test script for the Up Bank SDK.

This script exercises all API endpoints. Set UP_API_TOKEN environment variable
to your Up Bank personal access token.

Usage:
    $ UP_API_TOKEN="up:xxx" python scripts/test_integration.py
"""

import asyncio
import os
import sys
from up_bank_sdk import Client, AsyncClient


def main() -> None:
    token = os.environ.get("UP_API_TOKEN")
    if not token:
        print("Error: UP_API_TOKEN environment variable not set")
        print("Get your token from the Up app: Settings > Data sharing > Personal Access Token")
        sys.exit(1)

    print("Using UP_API_TOKEN from environment.")
    client = Client(token)

    print("\n" + "=" * 60)
    print("SYNC CLIENT TESTS")
    print("=" * 60)
    _test_sync_client(client)

    print("\n" + "=" * 60)
    print("ASYNC CLIENT TESTS")
    print("=" * 60)
    asyncio.run(_test_async_client(token))

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 60)


def _test_sync_client(client: Client) -> None:
    print("\n--- Testing util/ping ---")
    ping = client.util.ping()
    print(f"Ping status: {ping.meta.status_emoji}")

    print("\n--- Testing accounts.list ---")
    accounts = client.accounts.list()
    print(f"Found {len(accounts)} accounts:")
    for account in accounts:
        print(
            f"  - {account.attributes.display_name} ({account.attributes.account_type}): "
            f"{account.attributes.balance.value} {account.attributes.balance.currency_code}"
        )

    if accounts:
        account_id = accounts[0].id
        print(f"\n--- Testing accounts.get({account_id}) ---")
        account = client.accounts.get(account_id)
        print(f"Account: {account.attributes.display_name}")

        print(f"\n--- Testing accounts.list_transactions({account_id}) ---")
        response = client.accounts.list_transactions(account_id, page_size=5)
        print(f"First page has {len(response.data)} transactions")
        print(f"Has more: {response.has_more}")

    print("\n--- Testing categories.list ---")
    categories = client.categories.list()
    print(f"Found {len(categories)} categories")
    for cat in categories[:5]:
        print(f"  - {cat.id}: {cat.attributes.name}")
    if len(categories) > 5:
        print(f"  ... and {len(categories) - 5} more")

    if categories:
        cat_id = categories[0].id
        print(f"\n--- Testing categories.get({cat_id}) ---")
        cat = client.categories.get(cat_id)
        print(f"Category: {cat.attributes.name}")

    print("\n--- Testing tags.list ---")
    response = client.tags.list()
    print(f"First page has {len(response.data)} tags")
    print(f"Has more: {response.has_more}")
    for tag in response.data[:10]:
        print(f"  - {tag.id}")

    print("\n--- Testing transactions.list ---")
    response = client.transactions.list(page_size=10)
    print(f"First page has {len(response.data)} transactions")
    print(f"Has more: {response.has_more}")
    for tx in response.data[:5]:
        print(
            f"  - {tx.attributes.description}: {tx.attributes.amount.value} "
            f"{tx.attributes.amount.currency_code} ({tx.attributes.status})"
        )

    if response.has_more:
        print("\n--- Fetching next page of transactions ---")
        next_page = response.get_next()
        if next_page:
            print(f"Next page has {len(next_page.data)} transactions")

    if response.data:
        tx_id = response.data[0].id
        print(f"\n--- Testing transactions.get({tx_id}) ---")
        tx = client.transactions.get(tx_id)
        print(f"Transaction: {tx.attributes.description}")

    print("\n--- Testing attachments.list ---")
    response = client.attachments.list()
    print(f"First page has {len(response.data)} attachments")
    print(f"Has more: {response.has_more}")
    if response.data:
        att = response.data[0]
        print(f"  First: {att.id} - {att.attributes.file_extension}")
        print(f"\n--- Testing attachments.get({att.id}) ---")
        att = client.attachments.get(att.id)
        print(
            f"Attachment: {att.attributes.file_extension} - expires: {att.attributes.file_url_expires_at}"
        )

    print("\n--- Testing webhooks.list ---")
    response = client.webhooks.list()
    print(f"First page has {len(response.data)} webhooks")
    print(f"Has more: {response.has_more}")

    if response.data:
        wh = response.data[0]
        print(f"\n--- Testing webhooks.get({wh.id}) ---")
        webhook = client.webhooks.get(wh.id)
        print(f"Webhook: {webhook.attributes.url}")

        print(f"\n--- Testing webhooks.ping({wh.id}) ---")
        try:
            client.webhooks.ping(wh.id)
            print("Ping sent successfully")
        except Exception as e:
            print(f"Ping error: {e}")

        print(f"\n--- Testing webhooks.logs({wh.id}) ---")
        try:
            logs_response = client.webhooks.logs(wh.id)
            print(f"First page has {len(logs_response.data)} log entries")
        except Exception as e:
            print(f"Logs error: {e}")
    else:
        print("\n--- Testing webhooks.create ---")
        try:
            webhook = client.webhooks.create("https://example.com/test-webhook")
            print(f"Created webhook: {webhook.id} -> {webhook.attributes.url}")
            print(f"Deleting webhook {webhook.id}...")
            client.webhooks.delete(webhook.id)
            print("Deleted successfully")
        except Exception as e:
            print(f"Webhook create/delete error: {e}")


async def _test_async_client(token: str) -> None:
    async with AsyncClient(token) as client:
        print("\n--- Testing util/ping ---")
        ping = await client.util.ping()
        print(f"Ping status: {ping.meta.status_emoji}")

        print("\n--- Testing accounts.list ---")
        accounts = await client.accounts.list()
        print(f"Found {len(accounts)} accounts:")
        for account in accounts:
            print(
                f"  - {account.attributes.display_name} ({account.attributes.account_type}): "
                f"{account.attributes.balance.value} {account.attributes.balance.currency_code}"
            )

        if accounts:
            account_id = accounts[0].id
            print(f"\n--- Testing accounts.get({account_id}) ---")
            account = await client.accounts.get(account_id)
            print(f"Account: {account.attributes.display_name}")

            print(f"\n--- Testing accounts.list_transactions({account_id}) ---")
            response = await client.accounts.list_transactions(account_id, page_size=5)
            print(f"First page has {len(response.data)} transactions")
            print(f"Has more: {response.has_more}")

        print("\n--- Testing categories.list ---")
        categories = await client.categories.list()
        print(f"Found {len(categories)} categories")
        for cat in categories[:5]:
            print(f"  - {cat.id}: {cat.attributes.name}")
        if len(categories) > 5:
            print(f"  ... and {len(categories) - 5} more")

        if categories:
            cat_id = categories[0].id
            print(f"\n--- Testing categories.get({cat_id}) ---")
            cat = await client.categories.get(cat_id)
            print(f"Category: {cat.attributes.name}")

        print("\n--- Testing tags.list ---")
        response = await client.tags.list()
        print(f"First page has {len(response.data)} tags")
        print(f"Has more: {response.has_more}")
        for tag in response.data[:10]:
            print(f"  - {tag.id}")

        print("\n--- Testing transactions.list ---")
        response = await client.transactions.list(page_size=10)
        print(f"First page has {len(response.data)} transactions")
        print(f"Has more: {response.has_more}")
        for tx in response.data[:5]:
            print(
                f"  - {tx.attributes.description}: {tx.attributes.amount.value} "
                f"{tx.attributes.amount.currency_code} ({tx.attributes.status})"
            )

        if response.has_more:
            print("\n--- Fetching next page of transactions (explicit pagination) ---")
            next_page = await response.get_next()
            if next_page:
                print(f"Next page has {len(next_page.data)} transactions")

        if response.data:
            tx_id = response.data[0].id
            print(f"\n--- Testing transactions.get({tx_id}) ---")
            tx = await client.transactions.get(tx_id)
            print(f"Transaction: {tx.attributes.description}")

        print("\n--- Testing attachments.list ---")
        response = await client.attachments.list()
        print(f"First page has {len(response.data)} attachments")
        print(f"Has more: {response.has_more}")
        if response.data:
            att = response.data[0]
            print(f"  First: {att.id} - {att.attributes.file_extension}")
            print(f"\n--- Testing attachments.get({att.id}) ---")
            att = await client.attachments.get(att.id)
            print(
                f"Attachment: {att.attributes.file_extension} - expires: {att.attributes.file_url_expires_at}"
            )

        print("\n--- Testing webhooks.list ---")
        response = await client.webhooks.list()
        print(f"First page has {len(response.data)} webhooks")
        print(f"Has more: {response.has_more}")

        if response.data:
            wh = response.data[0]
            print(f"\n--- Testing webhooks.get({wh.id}) ---")
            webhook = await client.webhooks.get(wh.id)
            print(f"Webhook: {webhook.attributes.url}")

            print(f"\n--- Testing webhooks.ping({wh.id}) ---")
            try:
                await client.webhooks.ping(wh.id)
                print("Ping sent successfully")
            except Exception as e:
                print(f"Ping error: {e}")

            print(f"\n--- Testing webhooks.logs({wh.id}) ---")
            try:
                logs_response = await client.webhooks.logs(wh.id)
                print(f"First page has {len(logs_response.data)} log entries")
            except Exception as e:
                print(f"Logs error: {e}")
        else:
            print("\n--- Testing webhooks.create ---")
            try:
                webhook = await client.webhooks.create("https://example.com/test-webhook")
                print(f"Created webhook: {webhook.id} -> {webhook.attributes.url}")
                print(f"Deleting webhook {webhook.id}...")
                await client.webhooks.delete(webhook.id)
                print("Deleted successfully")
            except Exception as e:
                print(f"Webhook create/delete error: {e}")

        print("\n--- Testing auto-pagination with async for ---")
        print("Fetching transactions using async iteration:")
        count = 0
        response = await client.transactions.list(page_size=5)
        async for tx in response:
            print(f"  - {tx.attributes.description}")
            count += 1
            if count >= 5:
                break
        print(f"  ... (fetched {count} transactions via auto-pagination)")


if __name__ == "__main__":
    main()
