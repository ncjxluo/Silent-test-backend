# -*- coding: utf-8 -*-
# @Time    : 2025/12/5 18:21
# @Author  : lwc
# @File    : roles_services.py
# @Description :

from app.dao.systems.roles_dao import RolesDao
from typing import List

class RolesService:

    @staticmethod
    async def get_all_role(current_page: int, current_count: int):
        roles = await RolesDao.get_roles(current_page, current_count)
        total_count = await RolesDao.get_roles_count()
        return {"total_count": total_count[0], "roles": roles}

    @staticmethod
    async def get_active_role(role_key: str):
        roles = await RolesDao.get_active_role(role_key)
        print(roles)
        res_roles = [ item.get("menu_key") for item in roles]
        print(res_roles)
        return res_roles

    @staticmethod
    async def addition_role(role_name:str, role_desc:str, menu_obj:List[dict]):
        menu_key_list = [ item.get("menu_key") for item in menu_obj]
        res = await RolesDao.addition_role(role_name, role_desc, menu_key_list)
        return res

    @staticmethod
    async def del_role(role_key: str):
        res = await RolesDao.del_role(role_key)
        return res


    @staticmethod
    async def edit_role(role_key: str, role_name:str, role_desc:str, initial_list:List, menu_obj:List[dict]):
        check_list = [ item.get("menu_key") for item in menu_obj]
        print(role_key)
        print(role_name)
        print(role_desc)
        print(initial_list)
        print(check_list)

        i_list = set(check_list) - set(initial_list)
        d_list = set(initial_list) - set(check_list)
        print(i_list)
        print(d_list)
        return {}
