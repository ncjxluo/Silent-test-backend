# -*- coding: utf-8 -*-
# @Time    : 2026/1/21 15:28
# @Author  : lwc
# @File    : str_server_group.py
# @Description : 服务器分组表

import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime

class StrServerGroup(SQLModel, table=True):

    __tablename__ = 'str_server_group'

    group_key: str = Field(max_length=100,default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="服务器分组的uuid，作为唯一标识符")
    parent_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), primary_key=True,
                           description="服务器分组父级分组的key")
    group_name: str = Field(max_length=60, default=None, description="分组的名字")
    group_type: str = Field(max_length=20, default=None, description="分组的类型")
    group_order: str = Field(max_length=10, default=None, description="分组的排序")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
