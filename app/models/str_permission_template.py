# -*- coding: utf-8 -*-
# @Time    : 2025/11/24 16:59
# @Author  : lwc
# @File    : str_permission_template.py
# @Description : 接口自动化 测试数据中的权限模板表

from sqlmodel import SQLModel, Field
from typing import Optional

class StrPermissionTemplate(SQLModel, table=True):

    __tablename__ = 'str_permission_template'

    id: Optional[int] = Field(default=None, primary_key=True)
    t_permission_name: str = Field(max_length=100, index=True, description="权限的名字")
    t_permission_type: str = Field(max_length=100, description="权限的类型")