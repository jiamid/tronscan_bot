# -*- coding: utf-8 -*-
# @Time    : 2024/7/26 17:18
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : messages.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from loguru import logger
from aiogram import types
from aiogram import F
import re
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from commonts.util import to_escape_string
from commonts.storage_manager import timer_task_storage
from tg_bot.bot import telegram_router
from tg_bot.handlers.base_list_storage_api import BaseListStorageApi


@telegram_router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    await message.answer(f"Your ID: {message.from_user.id},Chat ID: {message.chat.id}")


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'*Hello {to_escape_string(message.from_user.first_name)}*', parse_mode='MarkdownV2')


@telegram_router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(f'*Hello {to_escape_string(message.from_user.first_name)}*\n'
                         f'\n`/list_wallets`'
                         f'\n`/add_wallet 地址`'
                         f'\n`/del_wallet 地址`'
                         f'\n`/scan_wallet 地址`'
                         f'\n`/scan_transfers 地址`'
                         f'\n`/join`'
                         f'\n`/exit`'
                         f'\n\n', parse_mode='MarkdownV2')


wallet_api = BaseListStorageApi(timer_task_storage, 'wallets', 'wallet', True)(
    telegram_router)
