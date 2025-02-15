# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 15:19
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : async_task_manager.py
# @Software: PyCharm
import asyncio
from typing import Callable


class AsyncTaskManager:

    def __init__(self, max_sem: int):
        self.sem = asyncio.Semaphore(max_sem)
        self.tasks = []

    async def run_with_sem(self, task: Callable, **kwargs):
        async with self.sem:
            await task(**kwargs)

    async def add_task(self, task: Callable, **kwargs):
        new_task = asyncio.create_task(self.run_with_sem(task, **kwargs))
        self.tasks.append(new_task)

    async def run(self):
        await asyncio.gather(*self.tasks)
