# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 14:28
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : timer_scan.py
# @Software: PyCharm
import asyncio
from loguru import logger
import time
from commonts.storage_manager import timer_task_storage
from commonts.util import to_escape_string
from tg_bot.bot import send_message_to_bot
from commonts.settings import settings
from commonts.async_tronscan import TronscanApi


async def scan_wallet_transfers(wallet: str, chat_ids: list) -> None:
    # now_ts = int(time.time() * 1000)
    logger.info(f'start run scan {wallet} ')
    try:
        client = TronscanApi(settings.tronscan_api_key)
        start = 0
        limit = 50
        found_end_flag = False
        # end_diff_time = 1000 * 60 * 60 * 24 * 5 # 5天
        while not found_end_flag:
            transfers_data = await client.get_transfers_by_api(wallet, start, limit)
            normal_address_infos = transfers_data.get('normalAddressInfo', {})
            risk_address = []
            for normal_addr, risk_info in normal_address_infos.items():
                if risk_info.get('risk', False) is True:
                    risk_address.append(normal_addr)
            token_transfers = transfers_data.get('token_transfers', [])
            for token_transfer in token_transfers:
                # this_transfer_ts = token_transfer.get('block_ts', 0)
                from_address = token_transfer.get('from_address', '')
                if from_address in risk_address:
                    transaction_id = token_transfer.get('transaction_id', '')
                    detail_link = f'https://tronscan.org/#/transaction/{transaction_id}'
                    text = (f'钱包: *{wallet}*\n 发现异常交易地址:*{from_address}*\n'
                            f'>交易详情: [{transaction_id}]({to_escape_string(detail_link)})\n')
                    for chat_id in chat_ids:
                        await send_message_to_bot(chat_id, text, parse_mode='MarkdownV2')
                        logger.info(f'{wallet} found risk {detail_link}')

                # if now_ts - this_transfer_ts > end_diff_time:
                #     found_end_flag = True
                #     break
            if len(token_transfers) < limit:
                found_end_flag = True
            else:
                await asyncio.sleep(1)
                start += limit
    except Exception as e:
        logger.error(f'run scan {wallet} fail {e}')


def decimal_to_base36(n):
    if n == 0:
        return '0'
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    result = ''

    while n > 0:
        n, remainder = divmod(n, 36)
        result = digits[remainder] + result

    return result


async def do_scan() -> None:
    """Send the alarm message."""
    wallets = timer_task_storage.get_value('wallets', [])
    logger.info(f'start run scan {wallets} ')
    chat_ids = timer_task_storage.get_value('chat_ids', [])
    for wallet in wallets:
        await scan_wallet_transfers(wallet, chat_ids)
