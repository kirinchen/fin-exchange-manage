import asyncio
import os
import sys
from bfxapi import Client, Order
from bfxapi.models import Notification

import config


async def _gen_client(account_name: str = ''):
    bfx = Client(
        API_KEY=config.env(f'bitfinex-api-key{account_name}'),
        API_SECRET=config.env(f'bitfinex-api-secret{account_name}')
    )
    return bfx


class BitfinexExpandClient:

    def __init__(self, client: Client):
        self.client: Client = client

    async def cancel_funding_all(self, currency: str):
        endpoint = "auth/w/funding/offer/cancel/all"
        # endpoint = "auth/w/funding/keep"
        payload = {
            "currency": currency
        }
        raw_notification = await self.client.rest.post(endpoint, payload)
        return Notification.from_raw_notification(raw_notification)


def gen_request_client(account_name: str = '') -> (Client, BitfinexExpandClient):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result: Client = loop.run_until_complete(_gen_client(account_name))
    return result, BitfinexExpandClient(result)
