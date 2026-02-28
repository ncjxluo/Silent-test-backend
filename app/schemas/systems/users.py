# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:55
# @Author  : lwc
# @File    : users.py
# @Description :

from pydantic import BaseModel
from app.schemas.base_res_model import BaseResponseModel
from typing import Optional,Dict,List,Union
from datetime import datetime

class UsersItemResponse(BaseResponseModel):

    user_key: Optional[str]
    nickname: Optional[str]
    username: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    status: Optional[int]
    dept_key: Optional[str]
    dept: Optional[str]
    role_key: Optional[str]
    role: Optional[str]
    created_at: Optional[datetime]


class UsersResponse(BaseModel):

    total_count: int
    users: List[UsersItemResponse]


class UserRequest(BaseModel):
    username: str
    nickname: str
    email: Optional[str]
    phone: Optional[str]
    status: int
    dept_key: str
    role_key: str

class DelUserRequest(BaseModel):
    user_key: str