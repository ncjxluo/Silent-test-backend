# -*- coding: utf-8 -*-
# @Time    : 2026/3/4 16:23
# @Author  : lwc
# @File    : str_application_product_line.py
# @Description : 应用的产品线表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime


class StrApplicationProductLine(SQLModel, table=True):

    __tablename__ = 'str_application_product_line'

    id: Optional[int] = Field(default=None, primary_key=True)
    app_product_line: str = Field(max_length=40,default=None, description="应用的产品线")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())