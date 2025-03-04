# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 21:17
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : utils.py
# @Software: PyCharm

import os
import random
import string

import requests
from dotenv import load_dotenv


def get_proxy():
    return os.getenv("PROXY").replace(os.getenv("PROXY_RANDOM"),
                                      "".join(random.sample(
                                          string.ascii_letters + string.digits,
                                          10)))


def get_project_root():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


data_path = os.path.join(get_project_root() + "/data/")


def save_result(content: str, path: str = data_path + "completed.txt"):
    with open(path, "a") as f1:
        f1.write(f"{content}\n")


try:
    with open(data_path + "completed.txt", "r") as f:
        completed_list = [line.strip().split('----')[0] for line in f if line.strip().split('----')[0]]
except FileNotFoundError:
    completed_list = []


def crack_puzzle():
    resp = requests.post("http://api.nocaptcha.cn/api/wanda/lenscan/universal", headers={
        "User-Token": os.getenv("USER_TOKEN"),
    }, json={
        "difficulty": "hard",
    }).json()

    data = resp["data"]
    sessionId = data["sessionId"]
    moves = data["moves"]
    return sessionId, moves


def crack_cf(proxy):
    href = "https://testnet.lenscan.io/faucet"
    sitekey = "0x4AAAAAAA1z6BHznYZc0TNL"
    resp = requests.post("http://api.nocaptcha.io/api/wanda/cloudflare/universal",
                         headers={"User-Token": os.getenv("USER_TOKEN")},
                         json={"href": href, "proxy": proxy, "sitekey": sitekey}, timeout=120).json()
    return resp


if __name__ == '__main__':
    load_dotenv(override=True)
    for _ in range(10):
        print(get_proxy())
