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
from app.schemas.base import ApiResponse
from typing import List


router = APIRouter()


@router.get("/dashboard")
async def dashboard(current_user_key: str = Depends(get_current_user)):
    await asyncio.sleep(1)
    print(current_user_key)
    return {"message": "Hello World"}


@router.get("/get_user_menu",response_model=ApiResponse[List[MenuResponse]])
async def get_user_menu(current_user_key: str = Depends(get_current_user)):
    menus = await MenuServices.get_user_menu(current_user_key)
    print(menus)
    return ApiResponse(data=menus) # type: ignore