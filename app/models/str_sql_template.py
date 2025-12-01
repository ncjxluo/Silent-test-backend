# -*- coding: utf-8 -*-
# @Time    : 2025/11/24 16:59
# @Author  : lwc
# @File    : str_sql_template.py
# @Description :接口自动化 测试sql模板表

from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.mysql import LONGTEXT
from typing import Optional

class StrSqlTemplate(SQLModel, table=True):

    __tablename__ = 'str_sql_template'

    id: Optional[int] = Field(default=None, primary_key=True)
    sql_type: str = Field(max_length=20, index=True, description="sql语句的类型(给哪个数据使用的)")
    sql_lang: Optional[str] = Field(sa_type=LONGTEXT, description="sql语句")
    sql_permission: Optional[str] = Field(max_length=2000, description="执行它需要的权限")
    sql_effect: str = Field(max_length=20, description="sql语句的作用，铺底 测试 结束")
    sql_exec_timing: str = Field(max_length=20, description="sql语句执行的时机")