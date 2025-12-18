# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 16:20
# @Author  : lwc
# @File    : menus.py
# @Description :

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.systems.menus_services import MenusService
from app.schemas.systems.menus import MenusResponse
from typing import List

router = APIRouter()

@router.get("/get_menus",response_model=ApiResponse[List[MenusResponse]])
async def get_roles(current_user_key: str = Depends(get_current_user)):
    res = await MenusService.get_all_menu()
    return ApiResponse(data=res) # type: ignore