# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:44
# @Author  : lwc
# @File    : users_dao.py
# @Description :

from app.core.db import async_session
from app.models.str_sys_user import StrSysUser
from app.models.str_sys_dept import StrSysDept
from app.models.str_sys_user_role import StrSysUserRole
from app.models.str_sys_role import StrSysRole
from sqlmodel import select,delete, and_
from sqlalchemy import func,null
from datetime import datetime


class UsersDao:

    @staticmethod
    async def get_users(use_key:str, current_page: int, current_count: int, i_type:int):
        async with async_session() as session:
            query = select(StrSysUser.user_key,StrSysUser.nickname,StrSysUser.username,StrSysUser.email,StrSysUser.phone,StrSysUser.status,StrSysUser.dept_key,StrSysDept.dept_name.label('dept'),StrSysUserRole.role_key,StrSysRole.role_name.label('role'), StrSysUser.created_at
                           ).join(StrSysDept, StrSysUser.dept_key == StrSysDept.dept_key,isouter=True
                           ).join(StrSysUserRole, StrSysUser.user_key == StrSysUserRole.user_key,isouter=True
                           ).join(StrSysRole, StrSysUserRole.role_key == StrSysRole.role_key, isouter=True)
            if i_type == 0:
                query = query.where(StrSysUser.user_key != use_key)
            query = query.order_by(StrSysUser.created_at).offset(
                    (current_page - 1) * current_count).limit(current_count)
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

    @staticmethod
    async def get_users_statistic_count(final_time: datetime):
        async with async_session() as session:
            total_query = select(func.count(StrSysUser.user_key))
            online_query = select(func.count(StrSysUser.user_key)).where(
                and_(
                    StrSysUser.heartbeat_time > final_time
                )
            )
            total_result = await session.execute(total_query)
            total_count = total_result.one()
            online_result = await session.execute(online_query)
            online_count = online_result.one()
        return total_count, online_count

    @staticmethod
    async def addition_user(user_key:str, username: str, nickname: str, email:str, phone:str, status: int, dept_key:str, role_key:str):
        try:
            async with async_session() as session:
                user = StrSysUser(
                    user_key = user_key,
                    nickname = nickname,
                    username = username,
                    passwd = 'str@123456',
                    email = email,
                    phone = phone,
                    status = status,
                    dept_key = dept_key
                )

                user_role = StrSysUserRole(
                    user_key = user_key,
                    role_key = role_key
                )
                session.add(user)
                session.add(user_role)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def del_user(user_key: str):
        try:
            async with async_session() as session:
                await session.execute(delete(StrSysUser).where(StrSysUser.user_key == user_key))
                await session.execute(delete(StrSysUserRole).where(StrSysUserRole.user_key == user_key))
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}