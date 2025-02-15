# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:19
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from fastapi import APIRouter
from api.bot_webhook import router as bot_router
from api.task_list import router as task_list_router

router = APIRouter()
router.include_router(bot_router)
router.include_router(task_list_router)
