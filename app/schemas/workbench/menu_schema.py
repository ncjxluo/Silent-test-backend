# -*- coding: utf-8 -*-
# @Time    : 2025/11/5 16:17
# @Author  : lwc
# @File    : menu_schema.py
# @Description : 定义获取左侧菜单的schema

from pydantic import BaseModel
from typing import Optional


class MenuResponse(BaseModel):

    menu_key: Optional[str]
    menu_parent_key: Optional[str]
    menu_name: Optional[str]
    menu_path: Optional[str]
    menu_router_name: Optional[str]
    menu_component: Optional[str]
    menu_icon: Optional[str]
    menu_type: Optional[str]
    menu_order: Optional[int]
    is_visible: Optional[int]
    permission_code: Optional[str]

    class Config:
        orm_mode = True