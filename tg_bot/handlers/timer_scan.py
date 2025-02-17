# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 14:28
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : timer_scan.py
# @Software: PyCharm
import asyncio
from loguru import logger
import time
from datetime import datetime
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
                this_transfer_ts = token_transfer.get('block_ts', 0)
                transfer_time = datetime.fromtimestamp(this_transfer_ts / 1000)
                if transfer_time.year < 2024:
                    found_end_flag = True
                    break
                from_address = token_transfer.get('from_address', '')
                if from_address in risk_address:
                    token_decimal = token_transfer.get('tokenInfo', {}).get('tokenDecimal', 6)
                    decimal_str = '1' + '0' * token_decimal
                    quant_str = token_transfer.get('quant', '0')
                    number = int(int(quant_str) / int(decimal_str))
                    if number < 1:
                        logger.info(f'{wallet} found risk {detail_link}')
                        continue
                    transaction_id = token_transfer.get('transaction_id', '')
                    detail_link = f'https://tronscan.org/#/transaction/{transaction_id}'
                    transfer_time_str = transfer_time.strftime('%Y/%m/%d')

                    text = (f'钱包: *{wallet}*\n'
                            f'*发现异常交易*\n'
                            f'时间:*{transfer_time_str}*\n'
                            f'数量:*{number}*\n'
                            f'地址:*{from_address}*\n'
                            f'>交易详情: [{transaction_id}]({to_escape_string(detail_link)})')
                    for chat_id in chat_ids:
                        await send_message_to_bot(chat_id, text, parse_mode='MarkdownV2')
                        logger.info(f'{wallet} found risk {detail_link}')

                # if now_ts - this_transfer_ts > end_diff_time:
                #     found_end_flag = True
                #     break
            if len(token_transfers) < limit:
                found_end_flag = True
            if not found_end_flag:
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
