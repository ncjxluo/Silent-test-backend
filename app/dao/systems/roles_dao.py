# -*- coding: utf-8 -*-
# @Time    : 2025/12/5 18:21
# @Author  : lwc
# @File    : roles_dao.py
# @Description :

from app.core.db import async_session
from app.models.str_sys_role import StrSysRole
from app.models.str_sys_role_menu import StrSysRoleMenu
from sqlmodel import select,delete,update,insert
from sqlalchemy import func
from typing import List,Set
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


    @staticmethod
    async def edit_role(role_key: str, role_name:str, role_desc:str, i_set:Set[str], d_set:Set[str]):
        """
        编辑角色的方法
        :param role_key: 角色的key
        :param role_name: 角色的名字
        :param role_desc: 角色的描述
        :param i_set: 需要添加到角色中的菜单集合
        :param d_set: 需要删除到角色中的菜单集合
        :param d_set: 需要删除到角色中的菜单集合
        :return:
        """
        try:
            async with async_session() as session:
                usql = update(StrSysRole).where(
                    StrSysRole.role_key == role_key # type: ignore
                ).values(
                    role_name = role_name, description = role_desc
                )
                await session.execute(usql)
                if i_set is not None and len(i_set) > 0:
                    r_m_data = [{"menu_key": item ,"role_key": role_key} for item in i_set]
                    isql = insert(StrSysRoleMenu).values(
                        r_m_data
                    )
                    await session.execute(isql)
                if d_set is not None and len(d_set) > 0:
                    dsql = delete(StrSysRoleMenu).where(
                        StrSysRoleMenu.role_key == role_key # type: ignore
                    ).where(
                        StrSysRoleMenu.menu_key.in_(d_set) # type: ignore
                    )
                    await session.execute(dsql)
                await session.commit()
            return {"msg": "更新成功"}
        except Exception as e:
            return {"msg": "更新失败"}