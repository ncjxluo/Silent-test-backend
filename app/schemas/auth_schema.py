# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 15:49
# @Author  : lwc
# @File    : auth_schema.py
# @Description : 定义 auth 的请求体与响应体

from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    username: Optional[str]
    user_url: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True