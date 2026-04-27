# -*- coding: utf-8 -*-
# @Time    : 2026/3/6 10:23
# @Author  : lwc
# @File    : deploy_strategy.py
# @Description : 部署策略的相关接口

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.schemas.deployment.deploy_strategy_schema import DeployStrategyRequest,DeployStrategyResponse,DelDeployStrategyRequest,EditDeployStrategyRequest
from app.services.deployment.deploy_strategy_service import DeployStrategyService

router = APIRouter()


@router.post("/add_deploy_strategy",response_model=ApiResponse)
async def add_deploy_strategy(obj:DeployStrategyRequest, current_user_key: str = Depends(get_current_user)):
    res = await DeployStrategyService.add_deploy_strategy(obj.strategy_name, obj.process_mode, obj.app_product_line,
                obj.virtual_key,obj.app_config,obj.deployment_path,obj.deployment_config_content,obj.message_config
    )
    return ApiResponse(data=res) # type: ignore

@router.get("/get_deploy_strategy",response_model=ApiResponse[DeployStrategyResponse])
async def get_app_config(app_nickname:str=None, current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    res = await DeployStrategyService.get_deploy_strategy(app_nickname, current_page, current_count)
    return ApiResponse(data=res) # type: ignore

@router.post("/edit_deploy_strategy",response_model=ApiResponse)
async def edit_deploy_strategy(obj:EditDeployStrategyRequest, current_user_key: str = Depends(get_current_user)):
    res = await DeployStrategyService.edit_deploy_strategy(obj.strategy_key, obj.strategy_name, obj.process_mode, obj.app_product_line,
                obj.virtual_key,obj.app_config,obj.deployment_path,obj.deployment_config_content,obj.message_config
    )
    return ApiResponse(data=res) # type: ignore

@router.post("/del_deploy_strategy",response_model=ApiResponse)
async def del_deploy_strategy(obj:DelDeployStrategyRequest, current_user_key: str = Depends(get_current_user)):
    print(obj.strategy_key)
    res = await DeployStrategyService.del_deploy_strategy(obj.strategy_key)
    return ApiResponse(data=res) # type: ignore