# -*- coding: utf-8 -*-
# @Time    : 2024/6/23 20:05
# @Author  : Chris
# @Email   : 10512@qq.com
# @File    : task.py
# @Software: PyCharm


import abu
from curl_cffi import requests
from dotenv import load_dotenv
from loguru import logger
from src.utils import save_result, get_proxy, completed_list, data_path, crack_cf, crack_puzzle

success_path = data_path + "success.txt"


@abu.retry_with_method(30, log=True)
def task(t):
    save_result(t)
    proxy = get_proxy()
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "priority": "u=1, i",
        "referer": "https://testnet.lenscan.io/faucet",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "trpc-accept": "application/jsonl",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "x-trpc-source": "nextjs-react"
    }
    while 1:
        try:
            ret = crack_cf(proxy)
            token = ret["data"]["token"]
            break
        except BaseException as e:
            logger.error(f"Failed to crack cf, retrying: {e}")

    while 1:
        try:
            sessionId, moves = crack_puzzle(token)
            break
        except BaseException as e:
            logger.error(f"Failed to crack puzzle, retrying: {e}")

    url = "https://testnet.lenscan.io/api/trpc/faucet.claim"
    params = {"batch": "1"}
    data = {
        "0": {
            "json": {
                "address": t,
                "cfToken": token,
                "gameChallenge": {
                    "sessionId": sessionId,
                    "moves": moves
                }
            }
        }
    }
    resp = requests.post(url, json=data, headers=headers, params=params, proxy=proxy).text
    logger.info(f"Task {t} response: {resp}")
    return True if '"success":true' in resp else False


def format_data(text):
    return text.split("----")


def process(data):
    address, *_, token = format_data(data)
    if address in completed_list:
        logger.warning(f"Task {address} has been completed, skip")
        return
    ret = task(address)
    if ret:
        save_result(data, success_path)


if __name__ == '__main__':
    load_dotenv(override=True)
    process("a----b----c")
