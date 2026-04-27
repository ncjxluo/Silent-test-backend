# -*- coding: utf-8 -*-
# @Time    : 2026/3/26 10:43
# @Author  : lwc
# @File    : http_content_type_enum.py
# @Description :
from enum import Enum

class HttpContentTypeEnum(Enum):

    form_data=("data","multipart/form-data")
    json=("json","application/json")
    text=("content", "text/plain")
    binary=("files", "application/octet-stream")

    @property
    def req_method(self):
        return self.value[0]

    @property
    def swagger(self):
        return self.value[1]