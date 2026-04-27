# -*- coding: utf-8 -*-
# @Time    : 2026/3/8 16:26
# @Author  : lwc
# @File    : str_kanban_columns.py
# @Description : 看板列的表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class StrKanbanColumns(SQLModel, table=True):

    __tablename__ = 'str_kanban_columns'


    column_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), primary_key=True,
                          description="看板列的uuid，作为唯一标识符")
    board_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), description="看板的uuid，作为唯一标识符")
    column_name: str = Field(max_length=60, default=None, description="看板列的名字")
    sort_order: str = Field(max_length=500, default=None, description="列的排序")
    column_status: str = Field(max_length=20, default=None, description="列的所代表的状态")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())