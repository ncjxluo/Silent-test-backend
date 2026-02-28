# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:41
# @Author  : lwc
# @File    : users.py
# @Description :

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.systems.users_services import UserService
from app.schemas.systems.users import UsersResponse,UserRequest,DelUserRequest


router = APIRouter()

@router.get("/get_users",response_model=ApiResponse[UsersResponse])
async def get_users(current_user_key: str = Depends(get_current_user), current_page:int = 1, current_count:int = 30,):
    users_res = await UserService.get_all_users(current_user_key, current_page, current_count)
    return ApiResponse(data=users_res) # type: ignore


@router.post("/addition_user",response_model=ApiResponse)
async def addition_dept(user:UserRequest, current_user_key: str = Depends(get_current_user)):
    res = await UserService.addition_user(user.username, user.nickname, user.email, user.phone, user.status, user.dept_key, user.role_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_user",response_model=ApiResponse)
async def del_dept(user:DelUserRequest, current_user_key: str = Depends(get_current_user)):
    print(user.user_key)
    res = await UserService.del_user(user.user_key)
    return ApiResponse(data=res) # type: ignore