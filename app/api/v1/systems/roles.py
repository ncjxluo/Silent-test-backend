# -*- coding: utf-8 -*-
# @Time    : 2025/12/5 18:17
# @Author  : lwc
# @File    : roles.py
# @Description :

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.systems.roles_services import RolesService
from app.schemas.systems.roles import RoleResponse,AdditionRoleRequest,DelRoleRequest,EditRoleRequest
from typing import List


router = APIRouter()

@router.get("/get_roles",response_model=ApiResponse[RoleResponse])
async def get_roles(current_user_key: str = Depends(get_current_user), current_page:int = 1, current_count:int = 30):
    res = await RolesService.get_all_role(current_page, current_count)
    return ApiResponse(data=res) # type: ignore


@router.get("/get_active_roles",response_model=ApiResponse[List])
async def get_active_roles(current_user_key: str = Depends(get_current_user), role_key:str = ''):
    res = await RolesService.get_active_role(role_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/addition_role",response_model=ApiResponse)
async def addition_role(objs:AdditionRoleRequest, current_user_key: str = Depends(get_current_user)):
    res = await RolesService.addition_role(objs.role_name, objs.role_description, objs.checkObj)
    return ApiResponse(data=res) # type: ignore


@router.post("/del_role",response_model=ApiResponse)
async def del_role(objs:DelRoleRequest, current_user_key: str = Depends(get_current_user)):
    res = await RolesService.del_role(objs.role_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/edit_role",response_model=ApiResponse)
async def del_role(objs:EditRoleRequest, current_user_key: str = Depends(get_current_user)):
    res = {}
    await RolesService.edit_role(objs.role_key,objs.role_name,objs.role_description,objs.initialCheckObj,objs.checkObj)
    return ApiResponse(data=res) # type: ignore