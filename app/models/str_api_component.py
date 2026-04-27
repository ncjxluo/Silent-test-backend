# -*- coding: utf-8 -*-
# @Time    : 2026/3/28 17:09
# @Author  : lwc
# @File    : str_api_component.py
# @Description :

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
import uuid
from sqlalchemy import SMALLINT


class StrApiComponent(SQLModel, table=True):

    __tablename__ = 'str_api_component'

    component_key:str = Field(max_length=100, primary_key=True, default_factory=lambda: str(uuid.uuid4()), description="组件的uuid")
    component_name: str = Field(max_length=50, description="组件的名字,比如http取样器")
    component_type: str = Field(max_length=200, description="组件的类型,比如根或者容器")
    component_category: str = Field(max_length=200, description="组件的分类,比如测试计划、取样器")
    component_xml_tag: str = Field(max_length=200, description="组件的xml标签,用于开始和结尾")
    is_container :int = Field(sa_type=SMALLINT,  description="是否可以放子节点")
    parent_keys: str = Field(max_length=200, description="允许放在哪些大类下")
    allow_child_categories: str = Field(max_length=200, description="允许哪些类放进来")
    props: Optional[str] = Field(max_length=2000, description="允许添加什么属性")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    component_order: Optional[int] = Field(sa_type=SMALLINT,  description="排序")
    component_desc: Optional[str] = Field(max_length=2000, description="组件的作用")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())