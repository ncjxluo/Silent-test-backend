# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:44
# @Author  : lwc
# @File    : users_dao.py
# @Description :

from app.core.db import async_session
from app.models.str_sys_user import StrSysUser
from app.models.str_sys_dept import StrSysDept
from sqlmodel import select
from sqlalchemy import func


class UsersDao:

    @staticmethod
    async def get_users(use_key:str, current_page: int, current_count: int):
        async with async_session() as session:
            query = select(StrSysUser.user_key,StrSysUser.nickname,StrSysUser.username,StrSysUser.email,StrSysUser.phone,StrSysUser.status,StrSysDept.dept_name.label('dept'),StrSysUser.created_at).join(
                StrSysDept, StrSysUser.dept_key == StrSysDept.dept_key,isouter=True # type: ignore
            ).where(StrSysUser.user_key != use_key).order_by(StrSysUser.created_at).offset((current_page - 1) * current_count).limit(current_count)
            result = await session.execute(query)
            users = result.mappings().all()
        return users

    @staticmethod
    async def get_users_count(use_key: str):
        async with async_session() as session:
            query = select(func.count(StrSysUser.user_key)).where(StrSysUser.user_key != use_key)
            result = await session.execute(query)
            users_count = result.one()
        return users_count