# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 16:26
# @Author  : lwc
# @File    : menus_services.py
# @Description :

from app.dao.systems.menus_dao import MenusDao

class MenusService:

    @staticmethod
    async def get_all_menu():
        menus = await MenusDao.get_menus()
        return menus