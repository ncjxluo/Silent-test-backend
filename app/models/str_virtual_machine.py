# -*- coding: utf-8 -*-
# @Time    : 2026/1/27 10:44
# @Author  : lwc
# @File    : str_virtual_machine.py
# @Description : 虚拟机存储表

import uuid
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime


class StrVirtualMachine(SQLModel, table=True):

    __tablename__ = 'str_virtual_machine'

    id: Optional[int] = Field(default=None, primary_key=True)
    virtual_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="虚拟机的key")
    virtual_name: str = Field(max_length=60,default=None, description="虚拟机的名字")
    virtual_env: str = Field(max_length=60, default=None, description="虚拟机环境标识")
    virtual_ip_address:str = Field(max_length=60,default=None, description="虚拟机的ip地址")
    virtual_ip_port: str = Field(max_length=10, default=None, description="虚拟机的端口")
    virtual_username: str = Field(max_length=60, default=None, description="虚拟机登录的用户名")
    virtual_password: str = Field(max_length=60, default=None, description="虚拟机登录的密码")
    virtual_config_info: Optional[str] = Field(max_length=200, default=None, description="虚拟机的配置信息")
    status: str = Field(max_length=30, default_factory=lambda: "未连接",description="虚拟机是否可连接")
    description: Optional[str] = Field(max_length=300,default=None,description="虚拟机备注信息")
    is_delete: Optional[int] = Field(sa_type=SMALLINT,default=0, description="虚拟机的删除状态,1=删除 0=未删除")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
