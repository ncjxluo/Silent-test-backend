# -*- coding: utf-8 -*-
# @Time    : 2026/1/16 15:01
# @Author  : lwc
# @File    : message_services.py
# @Description : 消息中心的service

from app.dao.message_center.message_dao import MessageDao

class MessageService:

    @staticmethod
    async def save_message_channel(mes_name: str, mes_url: str, mes_info: str, is_enable: int):
        data = await MessageDao.save_message_channel(mes_name, mes_url, mes_info, is_enable)
        return data

    @staticmethod
    async def get_message_channel():
        messages = await MessageDao.get_message_channel()
        return {"messages": messages}

    @staticmethod
    async def get_message_channel_status(status:int):
        messages = await MessageDao.get_message_channel_status(status)
        return messages

    @staticmethod
    async def setting_message_status(mes_key:str, is_enable:bool):
        status = 0
        if is_enable:
            status = 1
        res = await MessageDao.setting_message_status(mes_key, is_enable)
        return res

    @staticmethod
    async def delete_message_cchannel(mes_key:str):
        is_delete = 1
        res = await MessageDao.delete_message_cchannel(mes_key, is_delete)
        return res