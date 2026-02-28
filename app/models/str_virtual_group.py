# -*- coding: utf-8 -*-
# @Time    : 2026/1/27 10:45
# @Author  : lwc
# @File    : str_virtual_group.py
# @Description : 虚拟机和分组的关联表

from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime


class StrVirtualGropy(SQLModel, table=True):

    __tablename__ = 'str_virtual_group'

    virtual_key: str = Field(max_length=100, primary_key=True, description="虚拟机的key")
    group_key: str = Field(max_length=100, primary_key=True, description="虚拟机分组的key")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())