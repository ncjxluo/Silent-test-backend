# -*- coding: utf-8 -*-
# @Time    : 2025/12/22 15:39
# @Author  : lwc
# @File    : base_res_model.py
# @Description :

from pydantic import BaseModel, field_serializer
from datetime import datetime


class BaseResponseModel(BaseModel):

    # 全局字段序列化器：处理所有datetime类型字段
    @field_serializer("*", when_used="always")  # "*" 匹配所有字段
    def serialize_datetime(self, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value