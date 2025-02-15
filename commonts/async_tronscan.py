#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :async_tronscan.py
# @Time :2025/2/15 12:06
# @Author :Jiamid
import aiohttp
from loguru import logger
from urllib.parse import urlparse
import random
import hashlib
import base64


class TronscanApi:
    api_base = 'https://apilist.tronscanapi.com'
    web_api_key = "b45dd399-7257-4064-92b1-d54dae6aae57"

    def __init__(self, api_key='0ea19851-df52-4fe3-b686-9a3251d0561f', user_agent='JiamidBot'):
        self.user_agent = user_agent
        self.api_key = api_key

    def sign(self, params: dict):
        sorted_params_keys = sorted(params.keys(), key=lambda x: x)
        sorted_params = {
            key: params[key] for key in sorted_params_keys
        }
        text = '&'.join([f'{k}={v}' for k, v in sorted_params.items()])
        text_and_key = f'{text}&apiKeeeeey={self.web_api_key}'
        hash_str = hashlib.sha256(text_and_key.encode()).hexdigest()
        sign_str = base64.b64encode(hash_str.encode()).decode()
        return sign_str

    async def request(self, method: str, url: str, **kwargs):
        timeout = aiohttp.ClientTimeout(total=10)
        conn = aiohttp.TCPConnector(ssl=False, limit_per_host=1)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            async with session.request(method=method, url=url, **kwargs) as resp:
                data = await resp.json()
                return data

    async def r_get(self, api, params):
        data = await self.request('GET', api, params=params, headers={
            'User-Agent': self.user_agent,
            'TRON-PRO-API-KEY': self.api_key
        })
        return data

    async def x_get(self, api, params):
        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
            'Secret': self.sign(params),
            'Accept': 'application/json, text/plain, */*'
        }
        data = await self.request('GET', api, params=params, headers=headers)
        return data

    async def scan_wallet(self, wallet_addr):
        api = f'{self.api_base}/api/security/account/data'
        params = {'address': wallet_addr}
        data = await self.r_get(api, params)
        return data

    async def get_transfers_by_web(self, related_address: str, start: int = 0, limit: int = 20, sort='-timestamp',
                                   count='true',
                                   filter_token_value=0):
        api = f'{self.api_base}/api/filter/trc20/transfers'
        params = {
            "relatedAddress": related_address,
            "limit": limit,
            "start": start,
            "sort": sort,
            "count": count,
            "filterTokenValue": filter_token_value,
        }
        data = await self.x_get(api, params)
        return data

    async def get_transfers_by_api(self, related_address: str, start: int = 0, limit: int = 20, sort='-timestamp',
                                   count='true',
                                   filter_token_value=0):
        api = f'{self.api_base}/api/filter/trc20/transfers'
        params = {
            "relatedAddress": related_address,
            "limit": limit,
            "start": start,
            "sort": sort,
            "count": count,
            "filterTokenValue": filter_token_value,
        }
        data = await self.r_get(api, params)
        return data


async def test_main():
    api_key = '0ea19851-df52-4fe3-b686-9a3251d0561f'
    ua = 'JiamidBot'
    bot = TronscanApi(api_key, ua)
    address = 'TK4Ed2XihVvQgcw7qBvC1Byopf9mq8xAuC'
    is_safe = await bot.scan_wallet(address)
    print(is_safe)
    trdata = await bot.get_transfers_by_api(address)
    print(trdata)


if __name__ == '__main__':
    import asyncio

    asyncio.run(test_main())
