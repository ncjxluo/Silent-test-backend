# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 17:32
# @Author  : lwc
# @File    : dashboard.py
# @Description : 工作台相关的路由

import asyncio

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.menu.menu_services import MenuServices
from app.schemas.workbench.menu_schema import MenuResponse
from app.services.dashboard.dashboard_service import DashboardService
from app.schemas.systems.manage import NoticeResponse,MemoRequest,MemosResponse,EditMemoRequest,DelMemoRequest
from app.schemas.base import ApiResponse
from typing import List


router = APIRouter()


@router.get("/dashboard")
async def dashboard(current_user_key: str = Depends(get_current_user)):
    await asyncio.sleep(1)
    return {"message": "Hello World"}


@router.get("/get_notice",response_model=ApiResponse[List[NoticeResponse]])
async def get_notice(current_user_key: str = Depends(get_current_user)):
    notices = await DashboardService.get_notice()
    return ApiResponse(data=notices) # type: ignore


@router.get("/get_memo",response_model=ApiResponse[MemosResponse])
async def get_memo(current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    memos = await DashboardService.get_memos(current_user_key, current_page, current_count)
    return ApiResponse(data=memos) # type: ignore


@router.post("/add_memo",response_model=ApiResponse)
async def add_memo(obj:MemoRequest, current_user_key: str = Depends(get_current_user)):
    res = await DashboardService.add_memo(current_user_key, obj.memo_title, obj.memo_content, obj.memo_level, obj.memo_complete)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_memo",response_model=ApiResponse)
async def del_memo(obj:DelMemoRequest, current_user_key: str = Depends(get_current_user)):
    res = await DashboardService.del_memo(obj.memo_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/edit_memo",response_model=ApiResponse)
async def edit_memo(obj:EditMemoRequest, current_user_key: str = Depends(get_current_user)):
    res = await DashboardService.edit_memo(obj.memo_key, obj.memo_complete)
    return ApiResponse(data=res) # type: ignore


@router.get("/get_user_menu",response_model=ApiResponse[List[MenuResponse]])
async def get_user_menu(current_user_key: str = Depends(get_current_user)):
    menus = await MenuServices.get_user_menu(current_user_key)
    return ApiResponse(data=menus) # type: ignore