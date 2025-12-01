# -*- coding: utf-8 -*-
# @Time    : 2025/11/5 17:30
# @Author  : lwc
# @File    : menu_services.py
# @Description : 定义菜单的services

from app.dao.menu.menu_dao import MeunDao

class MenuServices:

    @staticmethod
    async def get_user_menu(user_key:str):
        res = await MeunDao.get_user_menu(user_key)
        menus = [ v for v in res.values()]
        print(f"services 层 的{menus}")
        return menus