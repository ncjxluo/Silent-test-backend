# -*- coding: utf-8 -*-
# @Time    : 2026/3/16 10:57
# @Author  : lwc
# @File    : str_deploy_log.py
# @Description : 部署日志表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy.dialects.mysql import LONGTEXT


class StrDeployLog(SQLModel, table=True):

    __tablename__ = 'str_deploy_log'

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: str = Field(max_length=100, index=True, description="任务的uuid")
    user_key: str = Field(max_length=100, index=True, description="用户的uuid")
    app_name: str = Field(max_length=50,default=None, description="部署应用的名字")
    app_version: str = Field(max_length=50, default=None, description="部署应用的版本")
    vm_name: str = Field(max_length=60, default=None, description="虚机的名字")
    app_line: str = Field(max_length=40, default=None, description="产品线")
    progress:str = Field(max_length=5, description="部署的进度")
    content: Optional[str] = Field(sa_type=LONGTEXT, description="部署的日志")
    status: Optional[str] = Field(max_length=10,default="ready",description="部署的状态")
    created_at: datetime = Field(default_factory=lambda: datetime.now(), index=True)
