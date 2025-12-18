# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 18:35
# @Author  : lwc
# @File    : depts_services.py
# @Description :

from app.dao.systems.depts_dao import DeptsDao

class DeptService:

    @staticmethod
    async def get_all_dept(current_page: int, current_count: int):
        depts = await DeptsDao.get_depts(current_page, current_count)
        total_count = await DeptsDao.get_depts_count()
        return {"total_count": total_count[0], "depts": depts}

    @staticmethod
    async def addition_dept(dept_name:str, status:int):
        res = await DeptsDao.addition_dept(dept_name, status)
        return res

    @staticmethod
    async def del_dept(dept_key:str):
        res = await DeptsDao.del_dept(dept_key)
        return res

    @staticmethod
    async def edit_dept(dept_key:str, dept_name:str, status: int):
        res = await DeptsDao.edit_dept(dept_key, dept_name, status)
        return res