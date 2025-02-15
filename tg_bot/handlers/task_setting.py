# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 16:04
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : task_setting.py
# @Software: PyCharm
from loguru import logger
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.bot import telegram_router
from commonts.storage_manager import timer_task_storage
from commonts.scheduler_manager import scheduler_manager
from tg_bot.handlers.timer_scan import do_scan
from commonts.settings import settings
from commonts.async_tronscan import TronscanApi


@telegram_router.message(Command("scan_wallet"))
async def scan_wallet(message: Message) -> None:
    white_chat_ids = timer_task_storage.get_value('chat_ids', [])
    chat_id = message.chat.id
    if chat_id not in white_chat_ids:
        await message.answer(f'非法指令')
        return
    args = message.text.split()[1:]
    if not args:
        await message.answer("Pls With Address")
        return
    addr = args[0]
    client = TronscanApi(settings.tronscan_api_key)
    safe_data = await client.scan_wallet(addr)
    safe_info_map = {
        "send_ad_by_memo": "帐户是否经常发送广告",
        "has_fraud_transaction": "账户是否有欺诈交易",
        "fraud_token_creator": "帐户是否为欺诈令牌的创建者",
        "is_black_list": "账户是否在黑名单中"
    }
    text = f'*{addr}*\n'
    for key,value in safe_info_map.items():
        flag = '否'
        if safe_data.get(key,False):
            flag = '是'
        text += f'>{value}: *{flag}* \n'

    await message.answer(text, parse_mode='MarkdownV2')


@telegram_router.message(Command("join"))
async def join_team(message: Message) -> None:
    args = message.text.split()[1:]
    if not args:
        await message.answer("Pls With Password")
        return
    pwd = args[0]
    if pwd != settings.password:
        logger.info(f'{message.chat.id} join fail pwd error')
        await message.answer("Fail to join")
    else:
        timer_task_storage.add_to_key('chat_ids', message.chat.id)
        logger.info(f'{message.chat.id} join success')
        await message.answer("Success to join")
        status = scheduler_manager.add_task(do_scan, 'timer_scan')
        if status:
            logger.info(f'timer_scan start success by {message.chat.id}')
            await message.answer("Start timer_scan")


@telegram_router.message(Command("exit"))
async def exit_item(message: Message) -> None:
    timer_task_storage.del_from_key('chat_ids', message.chat.id)
    logger.info(f'{message.chat.id} exit success')
    await message.answer("Success to exit")
    chat_ids = timer_task_storage.get_value('chat_ids', [])
    if not chat_ids:
        remove_status = scheduler_manager.remove_task('timer_scan')
        if remove_status:
            await message.answer("Remove timer_scan success")
            logger.info(f'timer_scan remove success')
        else:
            await message.answer("Remove timer_scan fail")
            logger.info(f'timer_scan remove fail')
