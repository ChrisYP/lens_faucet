# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 21:04
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : timer_task.py
# @Software: PyCharm
import os

import abu
import vthread

import pytz
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from src.runner import Runner


@vthread.pool(3)
def run_task(name):
    t = Runner(name)
    t.run()


def trigger():
    while 1:
        run_task("name")


if __name__ == '__main__':
    executor_key = 'executor_model'
    executors = {
        executor_key: ThreadPoolExecutor(os.cpu_count() // 2)
    }
    scheduler = BlockingScheduler(executors=executors, timezone=pytz.timezone("Asia/Shanghai"))

    scheduler.add_job(trigger, 'cron', hour=21, minute=19, second=55, misfire_grace_time=36000)

    scheduler.add_job(abu.over, 'cron', hour=21, minute=19, second=58, misfire_grace_time=36000)

    scheduler.start()
