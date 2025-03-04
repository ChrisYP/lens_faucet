# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 21:05
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : runner.py
# @Software: PyCharm
import time

from loguru import logger


class Runner:
    def __init__(self, name):
        self.name = name

    def run(self):
        time.sleep(.5)
        logger.info(f'{self.name} running...')
