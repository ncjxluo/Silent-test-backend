# -*- coding: utf-8 -*-
# @Time    : 2026/3/14 17:38
# @Author  : lwc
# @File    : deploy_task.py
# @Description :  部署执行的api
from pyexpat.errors import messages

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.schemas.deployment.deploy_task_schema import DeployStrategyRequest, DeployLogResponse
import asyncio
from app.services.deployment.deploy_task_service import DeployTaskService
from app.utils.str_operation_decorator import log_operation
import json


router = APIRouter()

@router.post("/exec_deploy_task",response_model=ApiResponse)
@log_operation(module="部署任务",operation="执行",content="执行了部署任务")
async def exec_deploy_task(obj:DeployStrategyRequest, current_user_key: str = Depends(get_current_user)):
    deploy_tool_internal_path = 'operations/middlewares/'
    task_res = await DeployTaskService.create_deploy_task(obj.strategy_key, obj.strategy_name, obj.process_mode, obj.app_product_line,
                                                obj.virtual_key, obj.virtual_name, obj.app_config, obj.deployment_path,
                                                json.loads(obj.deployment_config_content), json.loads(obj.message_config), deploy_tool_internal_path,current_user_key, obj.deploy_cmd)
    return ApiResponse(data=task_res) # type: ignore


@router.get("/get_deploy_result",response_model=ApiResponse[DeployLogResponse])
async def get_deploy_result(task_id:str, current_user_key: str = Depends(get_current_user)):
    deploy_log = await DeployTaskService.get_deploy_result(task_id)
    return ApiResponse(data=deploy_log) # type: ignore