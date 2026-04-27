# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 17:26
# @Author  : lwc
# @File    : app_config_dao.py
# @Description :

from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from typing import List
from app.models.str_application_manage import StrApplicationManage
from app.models.str_application_product_line import StrApplicationProductLine
from app.utils.my_util import is_empty

class AppconfigDao:

    @staticmethod
    async def add_app_config(app_nickname:str,app_product_line:str,
                             app_before_name:str,app_end_name:str,app_download_type:str,
                             app_download_ip:str,app_download_port:str,
                             app_download_uname:str,app_download_passwd:str,app_download_path:str) -> dict:
        try:
            async with async_session() as session:
                app_config = StrApplicationManage(
                    app_nickname= app_nickname,
                    app_product_line = app_product_line,
                    app_before_name = app_before_name,
                    app_end_name = app_end_name,
                    app_download_type = app_download_type,
                    app_download_ip = app_download_ip,
                    app_download_port = app_download_port,
                    app_download_uname = app_download_uname,
                    app_download_passwd = app_download_passwd,
                    app_download_path = app_download_path
                )
                session.add(app_config)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def get_app_config(app_nickname:str, app_product_line, current_page: int, current_count: int) -> dict:
        async with async_session() as session:
            query = select(StrApplicationManage.id,StrApplicationManage.app_nickname,StrApplicationManage.app_product_line,
                           StrApplicationManage.app_before_name,StrApplicationManage.app_end_name,
                           StrApplicationManage.app_download_type,StrApplicationManage.app_download_ip,
                           StrApplicationManage.app_download_port,StrApplicationManage.app_download_uname,
                           StrApplicationManage.app_download_passwd,StrApplicationManage.app_download_path,
                           StrApplicationManage.created_at,StrApplicationManage.updated_at
            ).where(and_(
                StrApplicationManage.is_delete == 0
            ))
            if not is_empty(app_nickname):
                query = query.where(
                    StrApplicationManage.app_nickname.like(f"{app_nickname}")
                )
            if not is_empty(app_product_line):
                query = query.where(
                    StrApplicationManage.app_product_line.like(f"{app_product_line}")
                )
            query = query.order_by(desc(StrApplicationManage.created_at)).offset((current_page - 1) * current_count).limit(
                current_count)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_app_config_count(app_nickname:str, app_product_line) -> dict:
        async with async_session() as session:
            query = select(
                func.count(StrApplicationManage.id)
            ).where(and_(
                StrApplicationManage.is_delete == 0,
            ))
            if not is_empty(app_nickname):
                query = query.where(
                    StrApplicationManage.app_nickname.like(f"{app_nickname}")
                )
            if not is_empty(app_product_line):
                query = query.where(
                    StrApplicationManage.app_product_line.like(f"{app_product_line}")
                )
            result = await session.execute(query)
            res_data = result.one()
        return res_data


    @staticmethod
    async def del_app_config(id:int):
        try:
            async with async_session() as session:
                d_sql = update(StrApplicationManage).where(
                    StrApplicationManage.id == id
                ).values(
                    is_delete = 1
                )
                await session.execute(d_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def edit_app_config(id:int ,app_nickname:str,app_product_line:str,
                             app_before_name:str,app_end_name:str,app_download_type:str,
                             app_download_ip:str,app_download_port:str,
                             app_download_uname:str,app_download_passwd:str,app_download_path:str) -> dict:
        try:
            async with async_session() as session:
                edit_ac = update(StrApplicationManage).where(and_(
                    StrApplicationManage.id == id
                )).values(
                    app_nickname=app_nickname,
                    app_product_line=app_product_line,
                    app_before_name=app_before_name,
                    app_end_name=app_end_name,
                    app_download_type=app_download_type,
                    app_download_ip=app_download_ip,
                    app_download_port=app_download_port,
                    app_download_uname=app_download_uname,
                    app_download_passwd=app_download_passwd,
                    app_download_path=app_download_path,
                )
                await session.execute(edit_ac)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def add_app_line(app_product_line: str) -> dict:
        try:
            async with async_session() as session:
                app_config = StrApplicationProductLine(
                    app_product_line=app_product_line,
                )
                session.add(app_config)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def get_app_line() -> dict:
        async with async_session() as session:
            query = select(StrApplicationProductLine.id,StrApplicationProductLine.app_product_line
                           ).where(and_(
                StrApplicationProductLine.is_delete == 0
            ))
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_app_config_selected(app_product_line:str) -> dict:
        async with async_session() as session:
            query = select(StrApplicationManage.id, StrApplicationManage.app_nickname,
                           StrApplicationManage.app_nickname.label('field_name'),literal('').label('field_order'),
                           StrApplicationManage.app_nickname.label('app_deploy_name'),
                            literal('').label('exec_cmd'),literal('').label('verify_cmd'),
                           ).where(and_(
                StrApplicationManage.is_delete == 0,
                StrApplicationManage.app_product_line == app_product_line
            ))
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_deploy_app(ids: List) -> dict:
        async with async_session() as session:
            query = select(StrApplicationManage).where(StrApplicationManage.id.in_(ids))
            result = await session.execute(query)
            res_data = result.scalars().all()
        return res_data