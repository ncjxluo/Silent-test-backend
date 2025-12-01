# -*- coding: utf-8 -*-
# @Time    : 2025/11/24 17:00
# @Author  : lwc
# @File    : str_user_template.py
# @Description : 接口自动化 测试用户的连接模板表

from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.mysql import LONGTEXT
from typing import Optional

class StrUserTemplate(SQLModel, table=True):

    __tablename__ = 'str_user_template'

    id: Optional[int] = Field(default=None, primary_key=True)
    t_user_name: str = Field(max_length=100, index=True, description="测试过程中用户的名字")
    t_user_passwd: Optional[str] = Field(max_length=100, description="测试过程中用户的密码")
    t_user_permission: str = Field(max_length=100, description="用户的权限")
    t_user_permission_type: str = Field(max_length=100, description="用户权限的类型")
    t_user_db_name: str = Field(sa_type=LONGTEXT, description="用户对哪个数据库有权限")
    t_user_db_type: str = Field(max_length=200, description="数据库的类型列表")