# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 14:37
# @Author  : lwc
# @File    : security.py
# @Description : 安全模块，包含密码加密、token创建和认证的功能

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from jose import jwt,JWTError
import arrow
from app.utils.helper import get_config
from app.utils.custom_exception import exception_401, exception_403


SECRET_KEY=get_config().get("base").get("secret_key")
ALGORITHM=get_config().get("base").get("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES=get_config().get("base").get("access_token_expire_minutes")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(data: dict, expires_delta: timedelta):
    """
    创建一个token令牌，用于校验是否过期
    :param data: 应该是一个包含
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    to_encode.update({"exp": (arrow.now('Asia/Shanghai') + expires_delta).datetime})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    """
    这个地方是校验token是否有效
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_key = payload.get("sub")
        if user_key is None:
            raise exception_401
        return user_key
    except JWTError:
        raise exception_401


def refresh_token(token: str) -> str:
    """
    尝试刷新token的方法
    :param token: 从请求体中，拿到的token
    :return:
    """
    try:
        if not token:
            raise exception_403
        user_key = verify_token(token)
        access_token = create_token({"sub": user_key}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return access_token
    except HTTPException:
        raise exception_403