# -*- coding: utf-8 -*-
# @Time    : 2026/2/28 15:30
# @Author  : lwc
# @File    : str_notice.py
# @Description : 系统公告表

import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from sqlalchemy import TEXT
from datetime import datetime

class StrSysNotice(SQLModel, table=True):

    __tablename__ = 'str_sys_notice'

    notice_key: str = Field(max_length=100,default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="公告的uuid，作为唯一标识符")
    notice_title: str = Field(max_length=100, default=None, description="公告更新的标题")
    notice_content: str = Field(sa_type=TEXT, default=None, description="公告的内容")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())