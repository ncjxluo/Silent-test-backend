# -*- coding: utf-8 -*-
# @Time    : 2025/12/5 18:21
# @Author  : lwc
# @File    : roles.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime


class RoleItemResponse(BaseModel):

    role_key: Optional[str]
    role_name: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]


class RoleResponse(BaseModel):

    total_count: int
    roles: List[RoleItemResponse]


class AdditionRoleRequest(BaseModel):

    role_name: str
    role_description: str
    checkObj: List[Dict]

class DelRoleRequest(BaseModel):

    role_key: str


class EditRoleRequest(BaseModel):

    role_key: str
    role_name: str
    role_description: str
    initialCheckObj: List
    checkObj: List[Dict]