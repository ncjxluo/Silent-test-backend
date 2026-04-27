# -*- coding: utf-8 -*-
# @Time    : 2026/3/8 16:26
# @Author  : lwc
# @File    : str_kanban_boards.py
# @Description : 看板的模板表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class StrKanbanBoards(SQLModel, table=True):

    __tablename__ = 'str_kanban_boards'

    board_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), primary_key=True,
                          description="看板的uuid，作为唯一标识符")
    board_name: str = Field(max_length=60, default=None, description="看板的名字")
    board_description: str = Field(max_length=500, default=None, description="看板的描述")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())