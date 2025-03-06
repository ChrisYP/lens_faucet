# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 20:06
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : main.py
# @Software: PyCharm
# main.py
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from loguru import logger
from src.task import process
import abu

logger.add("logs/{time:YYYY-MM-DD}.log", level="DEBUG", rotation='00:00', retention="3 days")


def main(tasks, workers=None):
    workers = workers or os.cpu_count() * 2
    total_tasks = len(tasks)
    logger.info(f"开始处理任务, 任务数量: {total_tasks}, 线程数: {workers}")
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = (executor.submit(process, task) for task in tasks)
        for completed_tasks, future in enumerate(as_completed(futures), 1):
            future.result()
            current_percentage = (completed_tasks / total_tasks) * 100
            logger.debug(f"完成进度: {completed_tasks}/{total_tasks} ({current_percentage:.2f}%)")

    end_time = time.perf_counter()
    logger.debug(f"总耗时: {end_time - start_time:.2f}秒")


if __name__ == '__main__':
    timer = abu.SetInterval(lambda: load_dotenv(override=True), 3)
    with open("data/data.txt", "r") as f:
        data = f.read().strip().split("\n")
    main(data, int(os.getenv("WORKERS")) or os.cpu_count() * 2)
    timer.cancel()
