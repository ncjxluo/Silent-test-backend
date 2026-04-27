# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 17:26
# @Author  : lwc
# @File    : app_config.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class AppConfigRequest(BaseModel):

    app_nickname: str
    app_product_line: str
    app_before_name: str
    app_end_name: str
    app_download_type: str
    app_download_ip: str
    app_download_port: str
    app_download_uname: str
    app_download_passwd: str
    app_download_path: str

class AppLineRequest(BaseModel):

    app_product_line: str


class EditAppConfigRequest(BaseModel):

    id: int
    app_nickname: str
    app_product_line: str
    app_before_name: str
    app_end_name: str
    app_download_type: str
    app_download_ip: str
    app_download_port: str
    app_download_uname: str
    app_download_passwd: str
    app_download_path: str

class DelAppConfigRequest(BaseModel):

    id: int

class AppConfigItem(BaseResponseModel):
    id: int
    app_nickname: str
    app_product_line: str
    app_before_name: str
    app_end_name: str
    app_download_type: str
    app_download_ip: str
    app_download_port: str
    app_download_uname: str
    app_download_passwd: str
    app_download_path: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class AppConfigResponse(BaseModel):

    total_count: int
    app_configs: List[AppConfigItem]

class AppLineResponse(BaseModel):

    id: int
    app_product_line: str

class AppConfigSelectedResponse(BaseModel):
    id: int
    app_nickname: str
    field_name: str
    field_order: Optional[str]
    app_deploy_name: str
    exec_cmd: Optional[str]
    verify_cmd: Optional[str]