# -*- coding: utf-8 -*-
# @Time    : 2026/1/21 15:52
# @Author  : lwc
# @File    : server_setting.py
# @Description : 服务器设置的api接口

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.schemas.host_management.server_setting import ServerGroupRequest, ServerGroupsResponse, DelServerGroupRequest, VirtualMachineRequest, VirtualMachineResponse, VerifyVirtualMachineRequest, VerifyVirtualMachineResponse, AllVirtualMachineResponse, DelVirtualMachineRequest,EditVirtualMachineRequest, VirtualMachineStatisticResponse,VirtualMachineStatusResponse
from app.services.host_management.server_setting_service import ServerSettingService
from typing import List

router = APIRouter()


@router.post("/add_server_group",response_model=ApiResponse)
async def add_server_group(obj:ServerGroupRequest, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.add_server_group(obj.group_key, obj.parent_key, obj.group_name, obj.group_type, obj.group_order)
    return ApiResponse(data=res) # type: ignore


@router.get("/get_server_group",response_model=ApiResponse[List[ServerGroupsResponse]])
async def get_server_group(current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.get_server_group()
    return ApiResponse(data=res) # type: ignore

@router.post("/del_server_group",response_model=ApiResponse)
async def del_server_group(obj:DelServerGroupRequest, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.del_server_group(obj.group_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/add_virtual_machine",response_model=ApiResponse)
async def add_virtual_machine(obj:VirtualMachineRequest, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.add_virtual_machine(
        obj.group_key, obj.virtual_name, obj.virtual_env, obj.virtual_ip_address, obj.virtual_ip_port,
        obj.virtual_username, obj.virtual_password, obj.description
    )
    return ApiResponse(data=res) # type: ignore

@router.get("/get_virtual_machine",response_model=ApiResponse[VirtualMachineResponse])
async def get_virtual_machine(group_key:str='8d5654a7-391f-48b9-9032-a8b4aae9b1b9', fuzzy_search:str = None, current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.get_virtual_machine(group_key, fuzzy_search, current_page, current_count)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_virtual_machine_status",response_model=ApiResponse[List[VirtualMachineStatusResponse]])
async def get_virtual_machine_status(status:str = None, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.get_virtual_machine_status(status)
    return ApiResponse(data=res) # type: ignore


@router.post("/verify_virtual_machine",response_model=ApiResponse[VerifyVirtualMachineResponse])
async def verify_virtual_machine(obj:VerifyVirtualMachineRequest, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.verify_virtual_machine(obj.virtual_keys)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_virtual_machine_all_search",response_model=ApiResponse[AllVirtualMachineResponse])
async def get_virtual_machine(fuzzy_search:str = None, current_page:int = 1, current_count:int = 10000, current_user_key: str = Depends(get_current_user)):
    if fuzzy_search is None:
        return ApiResponse(data={}) # type: ignore
    res = await ServerSettingService.get_virtual_machine_all_search(fuzzy_search, current_page, current_count)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_virtual_machine",response_model=ApiResponse)
async def del_virtual_machine(obj:DelVirtualMachineRequest, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.del_virtual_machine(obj.virtual_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/edit_virtual_machine",response_model=ApiResponse)
async def edit_virtual_machine(obj:EditVirtualMachineRequest, current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.edit_virtual_machine(
        obj.group_key,obj.virtual_key, obj.virtual_name, obj.virtual_env, obj.virtual_ip_address, obj.virtual_ip_port,
        obj.virtual_username, obj.virtual_password, obj.description
    )
    return ApiResponse(data=res) # type: ignore

@router.get("/virtual_machine_statistic",response_model=ApiResponse[VirtualMachineStatisticResponse])
async def virtual_machine_statistic(current_user_key: str = Depends(get_current_user)):
    res = await ServerSettingService.virtual_machine_statistic()
    return ApiResponse(data=res) # type: ignore