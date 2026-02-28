# -*- coding: utf-8 -*-
# @Time    : 2026/2/28 15:12
# @Author  : lwc
# @File    : str_memo.py
# @Description : 备忘录表

import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from sqlalchemy import TEXT
from datetime import datetime

class StrSysMemo(SQLModel, table=True):

    __tablename__ = 'str_sys_memo'

    memo_key: str = Field(max_length=100,default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="待办事项的uuid，作为唯一标识符")
    user_key: str = Field(max_length=100, index=True, description="用户的uuid，作为唯一标识符")
    memo_title: str = Field(max_length=100, default=None, description="备忘录的标题")
    memo_content: str = Field(sa_type=TEXT, default=None, description="备忘录的内容")
    memo_level: str = Field(max_length=10, default=None, description="备忘录的优先级")
    memo_complete: str = Field(max_length=10, default=None, description="是否完成")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())