# -*- coding: utf-8 -*-
# @Time    : 2026/3/16 12:00
# @Author  : lwc
# @File    : str_log_dao.py
# @Description :
from multiprocessing.spawn import set_executable

from app.core.db import async_session
from sqlmodel import select,delete,update
from sqlalchemy import func,and_
from app.models.str_operation_log import StrOperationLog
from app.models.str_deploy_log import StrDeployLog
from typing import List


class StrLogDao:

    @staticmethod
    async def record_operation_log(user_key:str, oper_type:str, oper_module:str, oper_content:str, oper_ip:str, oper_status:str):

        async with async_session() as session:
            str_o_log = StrOperationLog(
                user_key = user_key,
                oper_type=oper_type,
                oper_module=oper_module,
                oper_content=oper_content,
                oper_ip=oper_ip,
                oper_status=oper_status,
            )
            session.add(str_o_log)
            await session.commit()

    @staticmethod
    async def record_deploy_log(task_id:str, user_key: str, apps: List, progress: str, vm_name:str, app_line:str):
        try:
            async with async_session() as session:
                print(f"apps{apps}")
                task_list = []
                for item in apps:
                    deploy_task = StrDeployLog(
                        task_id=task_id,
                        user_key=user_key,
                        app_name=item.get("app_nickname"),
                        app_version=item.get("version"),
                        vm_name=vm_name,
                        app_line=app_line,
                        progress=progress,
                        content=item.get("app_content"),
                        status='ready'
                    )
                    task_list.append(deploy_task)
                session.add_all(task_list)
                await session.commit()
        except Exception as e:
            print(e)

    @staticmethod
    async def append_deploy_log(task_id: str, app_name: str, progress: str, content: str, u_type: str):
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(StrDeployLog).where(
                        and_(
                            StrDeployLog.task_id == task_id,
                            StrDeployLog.app_name == app_name
                        )
                    )
                )
                log = result.scalars().first()
                if not log:
                    return
                if u_type == '0':
                    log.progress = progress
                else:
                    log.content += "\n" + content  # 追加
                await session.commit()
        except Exception as e:
            print(f"错误:{e}")

    @staticmethod
    async def set_deploy_log_status(task_id: str, app_name: str, status:str):
        try:
            async with async_session() as session:
                u_sql = update(StrDeployLog).where(
                    and_(
                        StrDeployLog.task_id == task_id,
                        StrDeployLog.app_name == app_name,
                    )
                ).values(
                    status = status
                )
                await session.execute(u_sql)
                await session.commit()
        except Exception as e:
            print(e)

    @staticmethod
    async def get_deploy_log(task_id: str):
        async with async_session() as session:
            query = select(StrDeployLog.task_id,StrDeployLog.app_name,StrDeployLog.progress,StrDeployLog.content
                           ,StrDeployLog.status).where(
                StrDeployLog.task_id == task_id
            )
            res = await session.execute(query)
            data = res.mappings().all()
        return data