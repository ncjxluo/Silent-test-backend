# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 11:20
# @Author  : lwc
# @File    : str_api_branch.py
# @Description : 接口文档的分支表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import TEXT
import uuid
from sqlalchemy import SMALLINT


class StrApiBranch(SQLModel, table=True):

    __tablename__ = 'str_api_branch'

    id: Optional[int] = Field(default=None, primary_key=True)
    branch_key:str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="分支的uuid")
    project_key: str = Field(max_length=100, index=True, description="项目的uuid")
    branch_name: str = Field(max_length=50, description="文档的名称,也是标题")
    branch_order: Optional[int] = Field(sa_type=SMALLINT,default=1, description="文档排序")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    is_default: int = Field(sa_type=SMALLINT, default=0, description="是否是默认, 1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())