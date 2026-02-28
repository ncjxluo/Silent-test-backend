# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 15:13
# @Author  : lwc
# @File    : str_sys_message.py
# @Description :
import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime

class StrSysMessage(SQLModel, table=True):

    __tablename__ = 'str_sys_message'

    mes_key: str = Field(max_length=100,default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="消息通道的uuid，作为唯一标识符")
    mes_name: str = Field(max_length=60, default=None, description="消息的名字")
    mes_url: str = Field(max_length=1000, default=None, description="消息的发送地址")
    mes_info: str = Field(max_length=2000, default=None, description="前端路由名字")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    is_enable: int = Field(sa_type=SMALLINT, default=1, description="是否启用,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())