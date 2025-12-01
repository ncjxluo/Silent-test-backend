# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 16:09
# @Author  : lwc
# @File    : base.py
# @Description : 基础返回响应的模板

from typing import TypeVar, Generic
from pydantic.generics import GenericModel


T = TypeVar("T")

class ApiResponse(GenericModel, Generic[T]):

    status: int = 200
    message: str = "操作成功"  # 默认值
    data: T