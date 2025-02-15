#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :tronscan.py
# @Time :2025/2/14 22:02
# @Author :Jiamid
import requests
import hashlib
import base64


class Troncan:
    api_key = "b45dd399-7257-4064-92b1-d54dae6aae57"
    api_base = 'https://apilist.tronscanapi.com'

    def __init__(self):
        pass

    def sign(self, params: dict):
        sorted_params_keys = sorted(params.keys(), key=lambda x: x)
        sorted_params = {
            key: params[key] for key in sorted_params_keys
        }
        text = '&'.join([f'{k}={v}' for k, v in sorted_params.items()])
        text_and_key = f'{text}&apiKeeeeey={self.api_key}'
        hash_str = hashlib.sha256(text_and_key.encode()).hexdigest()
        sign_str = base64.b64encode(hash_str.encode()).decode()
        return sign_str

    def requests_get(self, api, params):
        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
            'Secret': self.sign(params),
            'Accept': 'application/json, text/plain, */*'
        }
        resp = requests.get(api, headers=headers, params=params)
        data = resp.json()
        return data

    def get_transfers_by_web(self, related_address: str, start: int = 0, limit: int = 20, sort='-timestamp',
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
        data = self.requests_get(api, params)
        return data





if __name__ == '__main__':
    bot = Troncan()
    wallet_address = "TK4Ed2XihVvQgcw7qBvC1Byopf9mq8xAuC"
    b = bot.get_transfers_by_web(wallet_address)
    print(b)
