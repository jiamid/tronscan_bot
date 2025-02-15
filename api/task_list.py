# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 15:25
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : task_list.py
# @Software: PyCharm
from fastapi import APIRouter
from commonts.scheduler_manager import scheduler_manager

router = APIRouter()


@router.get("/task_list")
async def task_list():
    jobs = scheduler_manager.scheduler.get_jobs()  # 获取全部的jobs
    jobs_info = []
    for job in jobs:
        info = {}
        info['id'] = job.id
        info['next_run_time'] = job.next_run_time
        jobs_info.append(info)
    return jobs_info
