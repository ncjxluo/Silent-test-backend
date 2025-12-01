# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 17:54
# @Author  : lwc
# @File    : dependencies.py
# @Description : 依赖的模块

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    从请求头中获取 token 并校验，返回用户标识
    """
    return verify_token(token)
