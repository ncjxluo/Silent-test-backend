# -*- coding: utf-8 -*-
# @Time    : 2026/1/21 16:52
# @Author  : lwc
# @File    : server_setting_dao.py
# @Description :
from sqlalchemy.sql.functions import count
from app.core.db import async_session
from app.models.str_server_group import StrServerGroup
from sqlmodel import select,delete,update,and_,desc,func,or_
from app.models.str_virtual_machine import StrVirtualMachine
from app.models.str_virtual_group import StrVirtualGropy
from app.utils.my_util import is_empty
from typing import List


class ServerSettingDao:

    @staticmethod
    async def get_server_group() -> dict:
        async with async_session() as session:
            query = select(
                StrServerGroup
            ).where(StrServerGroup.is_delete == 0)
            result = await session.execute(query)
            res_data = result.scalars().all()
        return res_data


    @staticmethod
    async def add_server_group(group_key:str, parent_key:str, group_name:str, group_type:str, group_order:str) -> dict:
        try:
            async with async_session() as session:
                server_group = StrServerGroup(
                    group_key = group_key,
                    parent_key = parent_key,
                    group_name = group_name,
                    group_type = group_type,
                    group_order = group_order
                )
                session.add(server_group)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def update_server_group_name(group_key:str, group_name:str):
        try:
            async with async_session() as session:
                query = update(StrServerGroup).where(and_(
                    StrServerGroup.group_key == group_key
                )).values(
                    group_name=group_name
                )
                await session.execute(query)
                await session.commit()
            return {"msg": "更新成功"}
        except Exception as e:
            return {"msg": "更新失败"}

    @staticmethod
    async def del_server_group(group_key:str):
        try:
            async with async_session() as session:
                query = delete(StrServerGroup).where(and_(
                    StrServerGroup.group_key == group_key
                ))
                await session.execute(query)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def add_virtual_machine(group_key: str, virtual_key:str, virtual_name:str, virtual_env:str, virtual_ip_address:str,
                                  virtual_ip_port:str, virtual_username:str,
                                  virtual_password:str, description:str) -> dict:
        """
        添加虚拟机到指定的分组中
        :param group_key: 分组的key(
        :param virtual_key: 虚机的key
        :param virtual_name: 虚机的名字
        :param virtual_env: 虚机的环境标识
        :param virtual_ip_address: 虚机的ip地址
        :param virtual_ip_port: 虚机的端口号
        :param virtual_username: 虚机的用户名
        :param virtual_password: 虚机的密码
        :param description: 虚机的备注
        :return:
        """
        try:
            async with async_session() as session:
                vm = StrVirtualMachine(
                    virtual_key = virtual_key,
                    virtual_name = virtual_name,
                    virtual_env = virtual_env,
                    virtual_ip_address = virtual_ip_address,
                    virtual_ip_port = virtual_ip_port,
                    virtual_username=virtual_username,
                    virtual_password = virtual_password,
                    description = description
                )
                vm_group = StrVirtualGropy(
                    group_key = group_key,
                    virtual_key = virtual_key
                )

                session.add(vm)
                session.add(vm_group)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def edit_virtual_machine(group_key: str, virtual_key: str, virtual_name: str, virtual_env: str,
                                  virtual_ip_address: str,
                                  virtual_ip_port: str, virtual_username: str,
                                  virtual_password: str, description: str) -> dict:
        """
        编辑虚拟机的信息
        :param group_key: 分组的key
        :param virtual_key: 虚机的key
        :param virtual_name: 虚机的名字
        :param virtual_env: 虚机的环境标识
        :param virtual_ip_address: 虚机的ip地址
        :param virtual_ip_port: 虚机的端口号
        :param virtual_username: 虚机的用户名
        :param virtual_password: 虚机的密码
        :param description: 虚机的备注
        :return:
        """
        try:
            async with async_session() as session:
                edit_vm = update(StrVirtualMachine).where(and_(
                    StrVirtualMachine.virtual_key == virtual_key
                )).values(
                    virtual_name=virtual_name,
                    virtual_env=virtual_env,
                    virtual_ip_address=virtual_ip_address,
                    virtual_ip_port=virtual_ip_port,
                    virtual_username=virtual_username,
                    virtual_password=virtual_password,
                    description=description,
                )
                edit_group = update(StrVirtualGropy).where(and_(
                    StrVirtualGropy.virtual_key == virtual_key
                )).values(
                    group_key=group_key
                )
                await session.execute(edit_vm)
                await session.execute(edit_group)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def get_virtual_machine(group_key:str, fuzzy_search:str, current_page:int, current_count:int) -> dict:
        async with async_session() as session:
            query = select(
                StrServerGroup.group_name,
                StrVirtualGropy.group_key,
                StrVirtualMachine.virtual_key,
                StrVirtualMachine.virtual_name,
                StrVirtualMachine.virtual_env,
                StrVirtualMachine.virtual_ip_address,
                StrVirtualMachine.virtual_ip_port,
                StrVirtualMachine.virtual_username,
                StrVirtualMachine.virtual_password,
                StrVirtualMachine.status,
                StrVirtualMachine.virtual_config_info,
                StrVirtualMachine.description,
                StrVirtualMachine.created_at,
                StrVirtualMachine.updated_at
            ).join(
                StrVirtualGropy, StrServerGroup.group_key == StrVirtualGropy.group_key, isouter=True
            ).join(
                StrVirtualMachine, StrVirtualGropy.virtual_key == StrVirtualMachine.virtual_key, isouter=True
            ).where(and_(
                StrServerGroup.is_delete == 0,
            StrVirtualMachine.is_delete == 0,
                StrServerGroup.group_key == group_key
            ))
            if not is_empty(fuzzy_search):
                query = query.where(or_(StrVirtualMachine.virtual_ip_address.like(f"%{fuzzy_search}%"),
                                        StrVirtualMachine.virtual_name.like(f"%{fuzzy_search}%")))
            query = query.order_by(desc(StrVirtualMachine.created_at)).offset((current_page - 1) * current_count).limit(current_count)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_virtual_machine_count(group_key:str, fuzzy_search:str) -> dict:
        async with async_session() as session:
            query = select(
                func.count(StrVirtualGropy.virtual_key)
            ).join(
                StrVirtualMachine, StrVirtualGropy.virtual_key == StrVirtualMachine.virtual_key, isouter=True
            ).where(and_(
                StrVirtualMachine.is_delete == 0,
                StrVirtualGropy.group_key == group_key
            ))
            if not is_empty(fuzzy_search):
                query = query.where(or_(StrVirtualMachine.virtual_ip_address.like(f"%{fuzzy_search}%"),
                                        StrVirtualMachine.virtual_name.like(f"%{fuzzy_search}%")))
            result = await session.execute(query)
            res_data = result.one()
        return res_data


    @staticmethod
    async def get_virtual_machine_info(virtual_key: List[str]) -> dict:
        async with async_session() as session:
            query = select(
                StrVirtualMachine
            ).where(StrVirtualMachine.virtual_key.in_(virtual_key))
            result = await session.execute(query)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def verify_virtual_machine_info(virtual_key:str, status:str, virtual_config_info:str) -> dict:
        async with async_session() as session:
            query = update(
                StrVirtualMachine
            ).where(
                StrVirtualMachine.virtual_key == virtual_key
            ).values(
                status=status,
                virtual_config_info=virtual_config_info
            )
            await session.execute(query)
            await session.commit()
        return {}

    @staticmethod
    async def get_virtual_machine_all_search(fuzzy_search:str, current_page:int, current_count:int) -> dict:
        async with async_session() as session:
            query = select(
                StrServerGroup.group_name,
                StrVirtualGropy.group_key,
                StrVirtualMachine.virtual_key,
                StrVirtualMachine.virtual_name,
                StrVirtualMachine.virtual_env,
                StrVirtualMachine.virtual_ip_address,
                StrVirtualMachine.virtual_ip_port,
                StrVirtualMachine.virtual_username,
                StrVirtualMachine.virtual_password,
                StrVirtualMachine.status,
                StrVirtualMachine.virtual_config_info,
                StrVirtualMachine.description,
                StrVirtualMachine.created_at,
                StrVirtualMachine.updated_at
            ).join(
                StrVirtualGropy, StrServerGroup.group_key == StrVirtualGropy.group_key, isouter=True
            ).join(
                StrVirtualMachine, StrVirtualGropy.virtual_key == StrVirtualMachine.virtual_key, isouter=True
            ).where(and_(
                StrServerGroup.is_delete == 0,
            StrVirtualMachine.is_delete == 0
            ))
            if not is_empty(fuzzy_search):
                query = query.where(or_(StrVirtualMachine.virtual_ip_address.like(f"%{fuzzy_search}%"),
                                        StrVirtualMachine.virtual_name.like(f"%{fuzzy_search}%"),
                                        StrVirtualMachine.description.like(f"%{fuzzy_search}%")
                                        )
                                    )
            query = query.order_by(desc(StrVirtualMachine.created_at)).offset((current_page - 1) * current_count).limit(current_count)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def del_virtual_machine(virtual_key:str):
        try:
            async with async_session() as session:
                await session.execute(delete(StrVirtualMachine).where(and_(
                    StrVirtualMachine.virtual_key == virtual_key
                )))
                await session.execute( delete(StrVirtualGropy).where(and_(
                    StrVirtualGropy.virtual_key == virtual_key
                )))
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def virtual_machine_statistic():
        """
        获取虚机不同状态的个数
        :return:
        """
        async with async_session() as session:
            s_sql = select(count(StrVirtualMachine.virtual_key)).where(StrVirtualMachine.status == '可连接')
            f_sql = select(count(StrVirtualMachine.virtual_key)).where(StrVirtualMachine.status == '无法连接')
            u_sql = select(count(StrVirtualMachine.virtual_key)).where(StrVirtualMachine.status == '未连接')
            success_result = await session.execute(s_sql)
            success_count = success_result.one()
            fail_result = await session.execute(f_sql)
            fail_count = fail_result.one()
            unknown_result = await session.execute(u_sql)
            unknown_count = unknown_result.one()
            return success_count, fail_count, unknown_count

    @staticmethod
    async def get_virtual_machine_status(status:str) -> dict:
        async with async_session() as session:
            query = select(
                StrVirtualMachine.virtual_key,
                StrVirtualMachine.virtual_name,
            ).where(and_(
                StrVirtualMachine.status == status
            ))
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data