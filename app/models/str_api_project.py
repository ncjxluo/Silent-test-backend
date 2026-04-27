# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 10:31
# @Author  : lwc
# @File    : str_api_project.py
# @Description : 接口的项目管理表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import TEXT
import uuid
from sqlalchemy import SMALLINT


class StrApiProject(SQLModel, table=True):

    __tablename__ = 'str_api_project'

    id: Optional[int] = Field(default=None, primary_key=True)
    project_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="项目的uuid")
    project_name: str = Field(max_length=50, description="项目名称")
    project_desc: Optional[str] = Field(sa_type=TEXT, description="项目描述")
    user_key:str = Field(max_length=100, index=True, description="用户的uuid")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
