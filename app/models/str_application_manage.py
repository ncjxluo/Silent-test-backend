# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 16:23
# @Author  : lwc
# @File    : str_application_manage.py
# @Description : 应用的管理表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from sqlalchemy import SMALLINT
from datetime import datetime


class StrApplicationManage(SQLModel, table=True):

    __tablename__ = 'str_application_manage'

    id: Optional[int] = Field(default=None, primary_key=True)
    app_nickname: str = Field(max_length=40,default=None, description="应用的昵称")
    app_product_line: str = Field(max_length=40,default=None, description="应用的昵称")
    app_before_name: str = Field(max_length=100, default=None, description="应用名字的前缀")
    app_end_name: str = Field(max_length=50,default=None, description="应用名字的后缀")
    app_download_type: str = Field(max_length=20,default=None, description="应用下载的方式(ftp,http)")
    app_download_ip: str = Field(max_length=30, default=None, description="应用下载的ip地址")
    app_download_port: str = Field(max_length=20, default=None, description="应用下载的端口号")
    app_download_uname: Optional[str] = Field(max_length=64, default=None, description="下载时提供用户名")
    app_download_passwd: str = Field(max_length=30, default=None, description="下载时提供的密码")
    app_download_path: str = Field(max_length=500, default=None, description="应用下载的路径")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())