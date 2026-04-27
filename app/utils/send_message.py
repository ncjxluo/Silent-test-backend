# -*- coding: utf-8 -*-
# @Time    : 2026/3/16 16:57
# @Author  : lwc
# @File    : send_message.py
# @Description : 发送消息的模块

import httpx

async def send_mes(mes_url:str, mes_info:str):
    """
    发送消息的函数
    :param mes_url: 机器人的链接
    :param mes_info: 发送的内容
    :return:
    """
    headers = {"Content-Type": "application/json"}
    message_info = {
        "msgtype": "text",
        "text": {
            "content": f"{mes_info}",
            "mentioned_mobile_list": ["@all"]
        }
    }
    async with httpx.AsyncClient() as client:
        mes_response = await client.post(
            url=mes_url,
            json=message_info,
            headers=headers
        )