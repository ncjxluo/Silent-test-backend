# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 10:17
# @Author  : lwc
# @File    : sys_dao.py
# @Description :

from app.core.db import async_session
from sqlmodel import select,delete,update
from sqlalchemy import func
from app.models.str_sys_user import StrSysUser
from datetime import datetime


class SysDao:

    @staticmethod
    async def update_hearbeat_time(use_key:str,heartbeat_time:datetime):
        try:
            async with async_session() as session:
                u_sql = update(StrSysUser).where(
                    StrSysUser.user_key == use_key
                ).values(
                    heartbeat_time=heartbeat_time
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": f"{heartbeat_time}"}
        except Exception as e:
            return {"msg": f"失败{e}"}