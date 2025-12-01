# -*- coding: utf-8 -*-
# @Time    : 2025/11/5 16:23
# @Author  : lwc
# @File    : menu_data.py
# @Description : 定义获取菜单的数据访问方法

from app.core.db import async_session
from app.models.str_sys_menu import StrSysMenu
from app.models.str_sys_user_role import StrSysUserRole
from app.models.str_sys_role_menu import StrSysRoleMenu
from sqlmodel import select, and_


class MeunDao:

    @staticmethod
    async def get_user_menu(user_key:str):
        print(user_key)
        async with async_session() as session:
            query = (
                select(StrSysMenu)
                .join(StrSysRoleMenu, StrSysMenu.menu_key == StrSysRoleMenu.menu_key) # type: ignore
                .join(StrSysUserRole, StrSysUserRole.role_key == StrSysRoleMenu.role_key)
                .where(
                    and_(
                        StrSysUserRole.user_key == user_key
                    )
                )
                .order_by(StrSysMenu.menu_order)
            )
            result = await session.execute(query)
            menus = result.scalars().all()
            unique = {m.menu_key: m for m in menus}
        return unique