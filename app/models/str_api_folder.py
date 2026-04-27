# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 10:32
# @Author  : lwc
# @File    : str_api_folder.py
# @Description : 接口文档分组表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import TEXT
import uuid
from sqlalchemy import SMALLINT


class StrApiFolder(SQLModel, table=True):

    __tablename__ = 'str_api_folder'

    id: Optional[int] = Field(default=None, primary_key=True)
    folder_key:str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="组的uuid")
    project_key: str = Field(max_length=100, index=True, description="项目的uuid")
    branch_key: str = Field(max_length=100, index=True, description="分支的uuid")
    folder_name: str = Field(max_length=50, description="组的名称")
    folder_order: Optional[int] = Field(sa_type=SMALLINT,default=1, description="文档排序")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())