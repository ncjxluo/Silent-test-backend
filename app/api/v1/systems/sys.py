# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 10:13
# @Author  : lwc
# @File    : sys.py
# @Description : 系统本身接口


from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.systems.sys_services import SysService

router = APIRouter()

@router.get("/user_heartbeat",response_model=ApiResponse)
async def user_heartbeat(current_user_key: str = Depends(get_current_user)):
    res = await SysService.user_heartbeat(current_user_key)
    return ApiResponse(data=res) # type: ignore