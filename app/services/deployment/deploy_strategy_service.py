# -*- coding: utf-8 -*-
# @Time    : 2026/3/6 10:24
# @Author  : lwc
# @File    : deploy_strategy_service.py
# @Description :
from app.dao.deployment.deploy_strategy_dao import DeployStrategyDao

class DeployStrategyService:

    @staticmethod
    async def add_deploy_strategy(strategy_name: str,process_mode: str,app_product_line: str,virtual_key: str,app_config: str,deployment_path: str,deployment_config_content: str,message_config:str) -> dict:

        data = await DeployStrategyDao.add_deploy_strategy(
            strategy_name, process_mode, app_product_line, virtual_key, app_config, deployment_path,
            deployment_config_content, message_config
        )
        return data

    @staticmethod
    async def get_deploy_strategy(strategy_name:str, current_page:int, current_count:int) -> dict:

        data = await DeployStrategyDao.get_deploy_strategy(strategy_name, current_page, current_count)
        count = await DeployStrategyDao.get_deploy_strategy_count(strategy_name)
        return {"total_count": count[0], "deploy_strategys": data}

    @staticmethod
    async def edit_deploy_strategy(strategy_key: str, strategy_name: str,process_mode: str,app_product_line: str,virtual_key: str,app_config: str,deployment_path: str,deployment_config_content: str,message_config:str) -> dict:

        data = await DeployStrategyDao.edit_deploy_strategy(strategy_key,
            strategy_name, process_mode, app_product_line, virtual_key, app_config, deployment_path,
            deployment_config_content, message_config
        )
        return data

    @staticmethod
    async def del_deploy_strategy(strategy_key: str) -> dict:

        data = await DeployStrategyDao.del_deploy_strategy(strategy_key)
        return data