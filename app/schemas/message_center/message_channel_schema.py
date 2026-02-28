# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 18:21
# @Author  : lwc
# @File    : message_channel_schema.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from pydantic import RootModel
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class TestSendMessageRequest(BaseModel):
    mes_url: str
    mes_info: str


class SaveMessageRequest(BaseModel):
    mes_name: str
    mes_url: str
    mes_info: Optional[str]
    is_enable: int

class MessageResponse(BaseModel):
    mes_key: str
    mes_name: str
    mes_url: str
    mes_info: Optional[str] = None
    is_enable: int

class MessagesResponse(BaseModel):
    messages: List[MessageResponse]


class SettingMessageRequest(BaseModel):
    mes_key: str
    is_enable: bool

class DelMessageRequest(BaseModel):
    mes_key: str