# -*- coding: utf-8 -*-
# @Time    : 2025/12/5 18:21
# @Author  : lwc
# @File    : roles_dao.py
# @Description :

from app.core.db import async_session
from app.models.str_sys_role import StrSysRole
from app.models.str_sys_role_menu import StrSysRoleMenu
from sqlmodel import select,delete,update
from sqlalchemy import func
from typing import List
import uuid


class RolesDao:

    @staticmethod
    async def get_roles(current_page: int, current_count: int):
        async with async_session() as session:
            query = select(StrSysRole).where(StrSysRole.is_delete != 1).order_by(StrSysRole.created_at).offset(
                (current_page - 1) * current_count).limit(current_count)
            result = await session.execute(query)
            roles = result.scalars().all()
        return roles

    @staticmethod
    async def get_roles_count():
        async with async_session() as session:
            query = select(func.count(StrSysRole.role_key))
            result = await session.execute(query)
            role_count = result.one()
        return role_count

    @staticmethod
    async def get_active_role(role_key: str):
        async with async_session() as session:
            query = select(StrSysRoleMenu.menu_key).where(StrSysRoleMenu.role_key == role_key)
            result = await session.execute(query)
            active_role = result.mappings().all()
        return active_role


    @staticmethod
    async def addition_role(role_name:str, role_desc:str, menu_key_list:List):
        try:
            async with async_session() as session:
                role_key = uuid.uuid4()
                role = StrSysRole(
                    role_key=role_key,
                    role_name=role_name,
                    description=role_desc
                )
                cases = list()
                for menu_key in menu_key_list:
                    role_menu = StrSysRoleMenu(
                        menu_key=menu_key,
                        role_key=role_key
                    )
                    cases.append(role_menu)
                session.add(role)
                session.add_all(cases)
                await session.commit()
            return {"msg":"新增成功"}
        except Exception as e:
            return {"msg":"新增失败"}

    @staticmethod
    async def del_role(role_key: str):
        try:
            async with async_session() as session:
                await session.execute(delete(StrSysRole).where(
                    StrSysRole.role_key == role_key # type: ignore
                ))
                await session.execute(delete(StrSysRoleMenu).where(StrSysRoleMenu.role_key == role_key)) # type: ignore
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}