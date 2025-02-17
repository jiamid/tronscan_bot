# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 11:28
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : aps_scheduler.py
# @Software: PyCharm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta


class SchedulerManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler({
            'apscheduler.executors.processpool': {
                'type': 'processpool',
                'max_workers': '10'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '10',
            'apscheduler.timezone': 'Asia/Shanghai',  # 设置时区
        })

    def get_task_ids(self):
        jobs = self.scheduler.get_jobs()  # 获取全部的jobs
        ids = [job.id for job in jobs]
        return ids

    def check_in_tasks(self, task_id):
        ids = self.get_task_ids()
        if task_id in ids:
            return True
        return False

    def add_task(self, task, task_id):
        if self.check_in_tasks(task_id):
            return False
        self.scheduler.add_job(task, id=task_id,
                               replace_existing=True,
                               trigger='interval',
                               minutes=120,
                               next_run_time=datetime.now() + timedelta(seconds=10)
                               )
        return True

    def remove_task(self, task_id):
        if not self.check_in_tasks(task_id):
            return False
        self.scheduler.remove_job(task_id)
        return True

    def run(self):
        self.scheduler.start()


scheduler_manager = SchedulerManager()
