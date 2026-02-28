# -*- coding: utf-8 -*-
# @Time    : 2026/2/28 16:20
# @Author  : lwc
# @File    : manage_dao.py
# @Description : 系统一些管理功能的数据库操作(小功能)
from httpx import delete

from app.core.db import async_session
from app.models.str_sys_notice import StrSysNotice
from app.models.str_sys_memo import StrSysMemo
from sqlmodel import select,desc,and_,delete,update
from sqlalchemy import func
import uuid

class ManageDao:

    @staticmethod
    async def get_notice():
        """
        获取系统里程碑数据
        :return: 返回搜索到的数据
        """
        async with async_session() as session:
            query = select(StrSysNotice.notice_title,StrSysNotice.notice_content,StrSysNotice.created_at).order_by(desc(StrSysNotice.created_at))
            result = await session.execute(query)
            notice_data = result.mappings().all()
        return notice_data

    @staticmethod
    async def get_memos(user_key:str,current_page:int, current_count:int):
        """
        获取个人的代办事项
        :return: 返回搜索到的数据
        """
        async with async_session() as session:
            query = select(StrSysMemo.memo_key,StrSysMemo.memo_title,StrSysMemo.memo_content,StrSysMemo.memo_level,StrSysMemo.memo_complete,StrSysMemo.created_at).where(
                and_(
                    StrSysMemo.user_key == user_key,
                    StrSysMemo.is_delete == '0'
                )
            ).order_by(desc(StrSysMemo.memo_complete)).offset(
                (current_page - 1) * current_count).limit(current_count)
            result = await session.execute(query)
            memos_data = result.mappings().all()
        return memos_data

    @staticmethod
    async def get_memos_count(user_key: str):
        """
        获取个人的代办事项的数量
        :return: 返回搜索到的数据
        """
        async with async_session() as session:
            query = select(func.count(StrSysMemo.memo_key)).where(
                and_(
                    StrSysMemo.user_key == user_key,
                    StrSysMemo.is_delete == '0'
                )
            )
            result = await session.execute(query)
            memos_count = result.one()
        return memos_count

    @staticmethod
    async def add_memo(user_key:str, memo_title:str, memo_content:str, memo_level:str, memo_complete:str):
        """
        增加待办事项
        :return: 返回成功或失败的字典数据
        """
        try:
            async with async_session() as session:
                memo_key = uuid.uuid4()
                memo = StrSysMemo(
                    memo_key = memo_key,
                    user_key = user_key,
                    memo_title= memo_title,
                    memo_content= memo_content,
                    memo_level= memo_level,
                    memo_complete=memo_complete
                )
                session.add(memo)
                await session.commit()
            return {"msg":"新增成功"}
        except Exception as e:
            return {"msg":"新增失败"}

    @staticmethod
    async def del_memo(memo_key: str):
        """
        删除待办事项
        :return: 返回成功或失败的字典数据
        """
        try:
            async with async_session() as session:
                d_sql = delete(StrSysMemo).where(
                    StrSysMemo.memo_key == memo_key
                )
                await session.execute(d_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def edit_memo(memo_key: str, memo_complete:str):
        """
        编辑待办事项
        :return: 返回成功或失败的字典数据
        """
        try:
            async with async_session() as session:
                e_sql = update(StrSysMemo).where(
                    StrSysMemo.memo_key == memo_key # type: ignore
                ).values(
                    memo_complete = memo_complete
                )
                await session.execute(e_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            print(e)
            return {"msg": "编辑失败"}