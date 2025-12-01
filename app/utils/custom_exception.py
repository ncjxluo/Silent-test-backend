# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 15:20
# @Author  : lwc
# @File    : custom_exception.py
# @Description : 自定义异常类

from jose import jwt,JWTError
from fastapi import HTTPException, status


exception_401 = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token or expired",headers={"WWW-Authenticate": "Bearer"})

exception_403 = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Refresh token is expired",headers={"WWW-Authenticate": "Bearer"})