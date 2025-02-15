# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 16:08
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : bot_webhook.py
# @Software: PyCharm
from fastapi import APIRouter
from commonts.settings import settings
from typing import Annotated
from fastapi import Header
from loguru import logger
from aiogram import types
from tg_bot.bot import bot, dp

router = APIRouter()


@router.post(settings.webhook_path)
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != settings.secret_token:
        logger.error(f"Wrong secret token ! {x_telegram_bot_api_secret_token}")
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)
