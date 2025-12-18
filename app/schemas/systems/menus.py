# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 16:25
# @Author  : lwc
# @File    : menus.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union

class MenusResponse(BaseModel):

    menu_key:str
    menu_parent_key:str
    menu_name:str
    menu_order:int
    is_visible:int