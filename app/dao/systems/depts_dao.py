# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 18:33
# @Author  : lwc
# @File    : depts_dao.py
# @Description :

from app.core.db import async_session
from app.models.str_sys_dept import StrSysDept
from sqlmodel import select,delete,update
from sqlalchemy import func


class DeptsDao:

    @staticmethod
    async def get_depts(current_page: int, current_count: int):
        async with async_session() as session:
            query = select(StrSysDept).order_by(StrSysDept.created_at).offset(
                (current_page - 1) * current_count).limit(current_count)
            result = await session.execute(query)
            depts = result.scalars().all()
        return depts

    @staticmethod
    async def get_depts_count():
        async with async_session() as session:
            query = select(func.count(StrSysDept.dept_key))
            result = await session.execute(query)
            dept_count = result.one()
        return dept_count

    @staticmethod
    async def addition_dept(dept_name:str, status:int):
        try:
            async with async_session() as session:
                dept = StrSysDept(
                    dept_name=dept_name,
                    status=status
                )
                session.add(dept)
                await session.commit()
            return {"msg":"新增成功"}
        except Exception as e:
            return {"msg":"新增失败"}

    @staticmethod
    async def del_dept(dept_key: str):
        try:
            async with async_session() as session:
                await session.execute(delete(StrSysDept).where(StrSysDept.dept_key == dept_key))
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def edit_dept(dept_key: str, dept_name: str, status: int):
        try:
            async with async_session() as session:
                await session.execute(
                    update(StrSysDept).where(StrSysDept.dept_key == dept_key).values(
                        dept_name = dept_name, status = status
                    )
                )
                await session.commit()
            return {"msg": "更新成功"}
        except Exception as e:
            return {"msg": "更新失败"}