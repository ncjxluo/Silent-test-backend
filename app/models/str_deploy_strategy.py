# -*- coding: utf-8 -*-
# @Time    : 2026/3/5 18:10
# @Author  : lwc
# @File    : str_deploy_strategy.py
# @Description : 部署策略表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from sqlalchemy import SMALLINT,JSON
from datetime import datetime


class StrDeployStrategy(SQLModel, table=True):

    __tablename__ = 'str_deploy_strategy'

    strategy_key:str = Field(max_length=100,default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="部署策略的uuid，作为唯一标识符")
    strategy_name: str = Field(max_length=40,default=None, description="部署策略的名称")
    process_mode: str = Field(max_length=40,default=None, description="执行部署的模式，串行或并行")
    app_product_line: str = Field(max_length=40,default=None, description="应用产品线")
    virtual_key: str = Field(max_length=40,default=None, description="目标虚机的key")
    app_config: str = Field(sa_type=JSON, default=None, description="应用的配置信息")
    deployment_path: str = Field(max_length=200, default=None, description="部署工具所在虚机上的位置")
    deployment_config_content: str = Field(sa_type=JSON, default=None, description="部署工具的配置文件")
    message_config:str = Field(sa_type=JSON, default=None, description="消息通道的配置")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())