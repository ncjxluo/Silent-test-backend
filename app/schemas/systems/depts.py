# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 18:37
# @Author  : lwc
# @File    : depts.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime


class DeptRequest(BaseModel):
    dept_name: str
    status: int


class DelDeptRequest(BaseModel):
    dept_key: str


class EditDeptRequest(BaseModel):
    dept_key: str
    dept_name: str
    status: int

class DeptItemResponse(BaseModel):

    dept_key: Optional[str]
    dept_name: Optional[str]
    status: Optional[int]
    created_at: Optional[datetime]


class DeptResponse(BaseModel):

    total_count: int
    depts: List[DeptItemResponse]