# -*- coding: utf-8 -*-
# @Time    : 2026/3/28 15:24
# @Author  : lwc
# @File    : str_api_case_folder.py
# @Description : 用例分组的目录

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import TEXT
import uuid
from sqlalchemy import SMALLINT


class StrApiCaseFolder(SQLModel, table=True):

    __tablename__ = 'str_api_case_folder'

    id: Optional[int] = Field(default=None, primary_key=True)
    case_folder_key:str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="组的uuid")
    case_project_key: str = Field(max_length=100, index=True, description="项目的uuid")
    case_branch_key: str = Field(max_length=100, index=True, description="分支的uuid")
    case_folder_name: str = Field(max_length=50, description="组的名称")
    case_folder_order: Optional[int] = Field(sa_type=SMALLINT,default=1, description="文档排序")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())