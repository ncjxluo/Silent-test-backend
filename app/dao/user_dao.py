# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 18:14
# @Author  : lwc
# @File    : user_dao.py
# @Description : 访问数据库用户表的操作

from app.core.db import async_session
from app.models.str_sys_user import StrSysUser
from sqlmodel import select

class UserDao:

    @staticmethod
    async def login(username:str, password:str):
        async with async_session() as session:
            result = await session.execute(select(StrSysUser).where(StrSysUser.username==username).where(StrSysUser.passwd==password))
            user = result.scalar_one_or_none()
        print(user)
        return user
