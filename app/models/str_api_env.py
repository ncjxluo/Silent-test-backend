# -*- coding: utf-8 -*-
# @Time    : 2026/3/23 14:50
# @Author  : lwc
# @File    : str_api_env.py
# @Description :
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import TEXT
import uuid
from sqlalchemy import SMALLINT

class StrApiEnv(SQLModel, table=True):

    __tablename__ = 'str_api_env'

    env_key:str = Field(max_length=100, primary_key=True, default_factory=lambda: str(uuid.uuid4()), description="接口环境的uuid")
    env_name: str = Field(max_length=100, index=True, description="接口环境的名字")
    env_icon: str = Field(max_length=100, index=True, description="环境的icon")
    env_url: Optional[str] = Field(max_length=200, default='', description="前置url")
    env_color: Optional[str] = Field(max_length=200, default='', description="环境的背景颜色")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())