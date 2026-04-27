# -*- coding: utf-8 -*-
# @Time    : 2026/1/16 15:04
# @Author  : lwc
# @File    : message_dao.py
# @Description : 消息操作数据库的方法
from sqlalchemy.sql.coercions import expect

from app.core.db import async_session
from sqlmodel import select,delete,update,insert
from sqlalchemy import func, and_
from typing import List,Set
import uuid
from app.models.str_sys_message import StrSysMessage

class MessageDao:

    @staticmethod
    async def save_message_channel(mes_name: str, mes_url: str, mes_info: str, is_enable: int):
        try:
            async with async_session() as session:
                mes = StrSysMessage(
                    mes_name = mes_name,
                    mes_url = mes_url,
                    mes_info = mes_info,
                    is_enable = is_enable
                )
                session.add(mes)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}


    @staticmethod
    async def get_message_channel():
        """
        获取全部的消息通道数据
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrSysMessage
            ).where(StrSysMessage.is_delete==0)
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def get_message_channel_status(status:int):
        """
        获取启用状态的消息通道数据
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrSysMessage
            ).where(and_(StrSysMessage.is_delete==0,StrSysMessage.is_enable==status))
            result = await session.execute(quary)
            res_data = result.scalars().all()
            print(res_data)
        return res_data

    @staticmethod
    async def setting_message_status(mes_key:str, is_enable:int):
        """
        对消息状态进行启用和禁用的设置
        :return:
        """
        try:
            async with async_session() as session:
                updata_sql = update(StrSysMessage).where(and_(
                            StrSysMessage.mes_key == mes_key
                        )).values(
                            is_enable = is_enable
                        )
                await session.execute(updata_sql)
                await session.commit()
            return {"msg": "更新状态成功"}
        except Exception as e:
            return {"msg": "更新状态失败"}

    @staticmethod
    async def delete_message_cchannel(mes_key:str, is_delete:int):
        try:
            async with async_session() as session:
                updata_sql = update(StrSysMessage).where(and_(
                            StrSysMessage.mes_key == mes_key
                        )).values(
                            is_delete = is_delete
                        )
                await session.execute(updata_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}
        return res

    @staticmethod
    async def get_message(mes_key: str):
        """
        获取特定的消息通道数据
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrSysMessage
            ).where(StrSysMessage.mes_key == mes_key)
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data