import asyncio
import os
import sys
from bfxapi import Client, Order

import config


async def _gen_client():
    bfx = Client(
        API_KEY=config.env('bitfinex-api-key'),
        API_SECRET=config.env('bitfinex-api-secret')
    )
    return bfx


def gen_request_client() -> Client:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(_gen_client())
    return result
