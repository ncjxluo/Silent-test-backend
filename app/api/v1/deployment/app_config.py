# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 17:25
# @Author  : lwc
# @File    : app_config.py
# @Description : 应用配置

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.schemas.deployment.app_config_schema import AppConfigRequest,AppConfigResponse,EditAppConfigRequest,DelAppConfigRequest,AppLineRequest,AppLineResponse,AppConfigSelectedResponse
from app.services.deployment.app_config_service import AppConfigService
from typing import List

router = APIRouter()


@router.post("/add_app_config",response_model=ApiResponse)
async def add_app_config(obj:AppConfigRequest, current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.add_app_config(obj.app_nickname,obj.app_product_line,obj.app_before_name,
                obj.app_end_name,obj.app_download_type,obj.app_download_ip,
                obj.app_download_port,obj.app_download_uname,obj.app_download_passwd,obj.app_download_path
    )
    return ApiResponse(data=res) # type: ignore


@router.get("/get_app_config",response_model=ApiResponse[AppConfigResponse])
async def get_app_config(app_nickname:str=None, app_product_line:str=None, current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.get_app_config(app_nickname, app_product_line, current_page, current_count)
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_app_config",response_model=ApiResponse)
async def edit_app_config(obj:EditAppConfigRequest, current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.edit_app_config(obj.id,obj.app_nickname,obj.app_product_line,obj.app_before_name,
                obj.app_end_name,obj.app_download_type,obj.app_download_ip,
                obj.app_download_port,obj.app_download_uname,obj.app_download_passwd,obj.app_download_path
    )
    return ApiResponse(data=res) # type: ignore

@router.post("/del_app_config",response_model=ApiResponse)
async def del_app_config(obj:DelAppConfigRequest, current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.del_app_config(obj.id)
    return ApiResponse(data=res) # type: ignore


@router.post("/add_app_line",response_model=ApiResponse)
async def add_app_line(obj:AppLineRequest, current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.add_app_line(obj.app_product_line)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_app_line",response_model=ApiResponse[List[AppLineResponse]])
async def get_app_line(current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.get_app_line()
    return ApiResponse(data=res) # type: ignore

@router.get("/get_app_config_selected",response_model=ApiResponse[List[AppConfigSelectedResponse]])
async def get_app_config_selected(app_product_line:str=None, current_user_key: str = Depends(get_current_user)):
    res = await AppConfigService.get_app_config_selected(app_product_line)
    return ApiResponse(data=res) # type: ignore