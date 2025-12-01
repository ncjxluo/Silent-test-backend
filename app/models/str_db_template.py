# -*- coding: utf-8 -*-
# @Time    : 2025/11/24 16:58
# @Author  : lwc
# @File    : str_db_template.py
# @Description : 接口自动化 测试数据中的数据库连接模板表

from sqlmodel import SQLModel, Field
from typing import Optional

class StrDbTemplate(SQLModel, table=True):

    __tablename__ = 'str_db_template'

    id: Optional[int] = Field(default=None, primary_key=True)
    db_name: str = Field(max_length=100, index=True, description="数据库实例的名字")
    db_type: str = Field(max_length=100, description="数据库实例的类型")
    db_ip: str = Field(max_length=100, description="数据库实例的IP地址")
    db_port: str = Field(max_length=100, description="数据库实例的端口号")
    db_service_name: str = Field(max_length=100, description="数据库实例的服务名")
    db_uname: str = Field(max_length=100, description="数据库实例的用户名")
    db_passwd: str = Field(max_length=100, description="数据库实例的密码")
    db_schema_name: str = Field(max_length=100, description="数据库实例的需要填写的schema名字")
    db_safety_rules: str = Field(max_length=100, description="数据库实例使用的安全规则")
