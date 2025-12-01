# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 15:45
# @Author  : lwc
# @File    : auth.py
# @Description : 与授权相关的路由，比如用户登录，刷新token等

from pyexpat.errors import messages
from fastapi import APIRouter,Response,Request,HTTPException
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.schemas.base import ApiResponse
from app.core.security import create_token
from app.utils.helper import get_config
from datetime import timedelta
from app.utils.custom_exception import exception_403
from app.core.security import refresh_token as ref_token
from app.services.user_service import UserServices


router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES=get_config().get("base").get("access_token_expire_minutes")
REFRESH_TOKEN_EXPIRE_MINUTES=get_config().get("base").get("refresh_token_expire_minutes")

@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(login_data: LoginRequest, response: Response):
    user = await UserServices.check_auth(login_data.username, login_data.password)
    if user is None:
        return ApiResponse[LoginResponse](data=LoginResponse(username=None, user_url=None, token=None), message="登录失败,账号或密码错误", status=200) # type: ignore

    access_token = create_token({"sub": user.user_key}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": user.user_key}, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # 生产环境开启 HTTPS 时必须
        samesite="lax",  # CSRF 防护
        max_age=3600
    )
    return ApiResponse[LoginResponse](data=LoginResponse(username=user.username, user_url=user.avatar, token=access_token), message="登录成功", status=200) # type: ignore


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
            key="refresh_token",
            path="/",
            domain=None,
            secure=False,
            samesite="lax"
        )
    return {"status":200, "message": "已退出登录","data": {}}



@router.post("/refresh")
async def refresh(request: Request):
    try:
        print("Headers:", request.headers)
        print("Cookies:", request.cookies)
        refresh_token = request.cookies.get("refresh_token")
        print(refresh_token)
        print("wo  zhixingle ya ")
        if not refresh_token:
            raise exception_403
        access_token = ref_token(refresh_token)
        return {"message": "操作成功", "data": {"access_token": access_token}}
    except HTTPException:
        raise exception_403
