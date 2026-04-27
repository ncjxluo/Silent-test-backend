# -*- coding: utf-8 -*-
# @Time    : 2026/1/21 15:57
# @Author  : lwc
# @File    : server_setting.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class ServerGroupRequest(BaseModel):
    parent_key: str
    group_key: str
    group_name: str
    group_type: str
    group_order: int


class ServerGroupsResponse(BaseModel):
    group_key: str
    parent_key: str
    group_name: str
    group_type: str
    group_order: int
    children: Optional[list] = []

class DelServerGroupRequest(BaseModel):
    group_key: str

class DelVirtualMachineRequest(BaseModel):
    virtual_key: str

class VirtualMachineRequest(BaseModel):
    group_key: str
    virtual_name: str
    virtual_env: str
    virtual_ip_address: str
    virtual_ip_port: str
    virtual_username: str
    virtual_password: str
    description: str

class EditVirtualMachineRequest(BaseModel):
    group_key: str
    virtual_key: str
    virtual_name: str
    virtual_env: str
    virtual_ip_address: str
    virtual_ip_port: str
    virtual_username: str
    virtual_password: str
    description: str

class VerifyVirtualMachineRequest(BaseModel):
    virtual_keys: List[str]


class VirtualMachineItem(BaseResponseModel):
    group_key: str
    group_name: str
    virtual_key: str
    virtual_name: str
    virtual_env: str
    virtual_ip_address: str
    virtual_ip_port: str
    virtual_username: str
    virtual_password: str
    status: str
    virtual_config_info: Optional[str] = ""
    description: Optional[str] = ""
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class VirtualMachineResponse(BaseModel):
    total_count: int
    virtual_machines: List[VirtualMachineItem]

class VirtualMachineStatusResponse(BaseModel):
    virtual_key: str
    virtual_name: str

class AllVirtualMachineResponse(BaseModel):
    virtual_machines: Optional[List[VirtualMachineItem]] = []


class VerifyVirtualMachineResponse(BaseModel):
    result: List


class VirtualMachineStatisticResponse(BaseModel):
    connection_success: int
    connection_fail: int
    connection_unknown: int