# -*- coding: utf-8 -*-
# @Time    : 2026/3/6 10:24
# @Author  : lwc
# @File    : deploy_strategy_dao.py
# @Description :

from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from app.models.str_deploy_strategy import StrDeployStrategy
from app.models.str_virtual_machine import StrVirtualMachine
from app.utils.my_util import is_empty

class DeployStrategyDao:

    @staticmethod
    async def add_deploy_strategy(strategy_name: str,process_mode: str,app_product_line: str,virtual_key: str,app_config: str,deployment_path: str,deployment_config_content: str,message_config:str) -> dict:
        try:
            async with async_session() as session:
                app_config = StrDeployStrategy(
                    strategy_name=strategy_name,
                    process_mode=process_mode,
                    app_product_line=app_product_line,
                    virtual_key=virtual_key,
                    app_config=app_config,
                    deployment_path=deployment_path,
                    deployment_config_content=deployment_config_content,
                    message_config=message_config
                )
                session.add(app_config)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def get_deploy_strategy(strategy_name: str, current_page: int, current_count: int) -> dict:
        async with async_session() as session:
            query = select(StrDeployStrategy.strategy_key,StrDeployStrategy.strategy_name,StrDeployStrategy.process_mode,StrDeployStrategy.app_product_line,
                           StrDeployStrategy.virtual_key,StrVirtualMachine.virtual_name,StrDeployStrategy.app_config,StrDeployStrategy.deployment_path,StrDeployStrategy.deployment_config_content,
                           StrDeployStrategy.message_config,StrDeployStrategy.created_at,StrDeployStrategy.updated_at
                           ).join(
                StrVirtualMachine, StrDeployStrategy.virtual_key == StrVirtualMachine.virtual_key
            ).where(and_(
                StrDeployStrategy.is_delete == 0
            ))
            if not is_empty(strategy_name):
                query = query.where(
                    StrDeployStrategy.strategy_name.like(f"{strategy_name}")
                )
            query = query.order_by(desc(StrDeployStrategy.created_at)).offset(
                (current_page - 1) * current_count).limit(
                current_count)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_deploy_strategy_count(strategy_name:str) -> dict:
        async with async_session() as session:
            query = select(
                func.count(StrDeployStrategy.strategy_key)
            ).where(and_(
                StrDeployStrategy.is_delete == 0,
            ))
            if not is_empty(strategy_name):
                query = query.where(
                    StrDeployStrategy.strategy_name.like(f"{strategy_name}")
                )
            result = await session.execute(query)
            res_data = result.one()
        return res_data

    @staticmethod
    async def edit_deploy_strategy(strategy_key: str, strategy_name: str, process_mode: str, app_product_line: str, virtual_key: str,
                                  app_config: str, deployment_path: str, deployment_config_content: str,
                                  message_config: str) -> dict:
        try:
            async with async_session() as session:
                e_sql = update(StrDeployStrategy).where(
                    StrDeployStrategy.strategy_key == strategy_key
                ).values(
                    strategy_name=strategy_name,
                    process_mode=process_mode,
                    app_product_line=app_product_line,
                    virtual_key=virtual_key,
                    app_config=app_config,
                    deployment_path=deployment_path,
                    deployment_config_content=deployment_config_content,
                    message_config=message_config
                )
                await session.execute(e_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_deploy_strategy(strategy_key:str):
        try:
            async with async_session() as session:
                d_sql = update(StrDeployStrategy).where(
                    StrDeployStrategy.strategy_key == strategy_key
                ).values(
                    is_delete = 1
                )
                await session.execute(d_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}