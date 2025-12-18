# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 16:25
# @Author  : lwc
# @File    : menus_dao.py
# @Description :

from app.core.db import async_session
from app.models.str_sys_menu import StrSysMenu
from sqlmodel import select
from sqlalchemy import func


class MenusDao:

    @staticmethod
    async def get_menus():
        async with async_session() as session:
            query = select(StrSysMenu).order_by(StrSysMenu.menu_order)
            result = await session.execute(query)
            menus = result.scalars().all()
        return menus