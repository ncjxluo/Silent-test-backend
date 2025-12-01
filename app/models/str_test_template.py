# -*- coding: utf-8 -*-
# @Time    : 2025/11/24 16:59
# @Author  : lwc
# @File    : str_test_template.py
# @Description : 接口自动化 测试sql和权限绑定模板表

from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.mysql import LONGTEXT
from typing import Optional

class StrTestTemplate(SQLModel, table=True):

    __tablename__ = 'str_test_template'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, index=True, description="测试过程中,使用的用户")
    dbname: str = Field(max_length=100, description="数据库实例的名字")
    schemaname: str = Field(max_length=100, description="数据库schema的名字")
    dbtype: str = Field(max_length=100, description="数据库的类型")
    sql: str = Field(sa_type=LONGTEXT, description="执行的sql语句")
    expect: str = Field(max_length=200, description="执行之后的期望")