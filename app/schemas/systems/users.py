# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:55
# @Author  : lwc
# @File    : users.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime

class UsersItemResponse(BaseModel):

    user_key: Optional[str]
    nickname: Optional[str]
    username: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    status: Optional[int]
    dept: Optional[str]
    created_at: Optional[datetime]


class UsersResponse(BaseModel):

    total_count: int
    users: List[UsersItemResponse]