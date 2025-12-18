# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:41
# @Author  : lwc
# @File    : users.py
# @Description :

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.systems.users_services import UserService
from app.schemas.systems.users import UsersResponse


router = APIRouter()

@router.get("/get_users",response_model=ApiResponse[UsersResponse])
async def get_users(current_user_key: str = Depends(get_current_user), current_page:int = 1, current_count:int = 30,):
    users_res = await UserService.get_all_users(current_user_key, current_page, current_count)
    return ApiResponse(data=users_res) # type: ignore