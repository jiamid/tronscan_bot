# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 17:24
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : main.py
# @Software: PyCharm
from fastapi import FastAPI
from loguru import logger
from commonts.logger import init_logging
from commonts.settings import settings
from tg_bot.bot import bot
from contextlib import asynccontextmanager
from commonts.scheduler_manager import scheduler_manager
from api import router
from tg_bot import handlers


async def init_scheduler():
    logger.info("🚀 Starting scheduler")
    scheduler_manager.run()
    # from tg_bot.handlers.timer_scan import do_scan
    # from commonts.storage_manager import timer_task_storage
    # chat_ids = timer_task_storage.get_value('chat_ids', [])
    # if chat_ids:
    #     status = scheduler_manager.add_task(do_scan, 'timer_scan')
    #     if status:
    #         logger.info(f'🚀 timer_scan start success')


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Starting Application")
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != f'{settings.base_webhook_url}{settings.webhook_path}':
        logger.info(f'set webhook {settings.webhook_path}')
        await bot.set_webhook(
            url=f'{settings.base_webhook_url}{settings.webhook_path}',
            secret_token=settings.secret_token,
            drop_pending_updates=True,
            max_connections=100,
        )
    await init_scheduler()
    yield
    logger.info("⛔ Stopping Application")


app = FastAPI(lifespan=lifespan,
              title='BotService',
              docs_url='/docs' if settings.debug else None,
              redoc_url='/redoc' if settings.debug else None,
              )
app.include_router(router)

if __name__ == '__main__':
    from uvicorn import run

    init_logging()
    logger.info("bot start")
    run(app, host='0.0.0.0', port=9999)
