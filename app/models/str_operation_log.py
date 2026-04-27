# -*- coding: utf-8 -*-
# @Time    : 2026/3/16 10:57
# @Author  : lwc
# @File    : str_operation_log.py
# @Description : 操作日志表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy.dialects.mysql import LONGTEXT


class StrOperationLog(SQLModel, table=True):

    __tablename__ = 'str_operation_log'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="用户的uuid")
    oper_type: str = Field(max_length=50,default=None, description="操作的类型,如新增、删除等")
    oper_module: str = Field(max_length=50,default=None, description="操作的模块,如某个功能")
    oper_content:str = Field(sa_type=LONGTEXT, description="日志的内容")
    oper_ip: Optional[str] = Field(max_length=64,default=None,description="ip地址")
    oper_status: Optional[str] = Field(max_length=64,default=None,description="执行的结果")
    created_at: datetime = Field(default_factory=lambda: datetime.now(), index=True)