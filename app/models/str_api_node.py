# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 16:03
# @Author  : lwc
# @File    : str_api_node.py
# @Description :  接口自动化节点(agent)

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import SMALLINT


class StrApiAgent(SQLModel, table=True):

    __tablename__ = 'str_api_agent'

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()), description="agent的uuid")
    agent_name: str = Field(max_length=50, description="agent的名字")
    agent_status: Optional[int] = Field(sa_type=SMALLINT,default=1,description="agent的状态,1=存活 0=失联")
    agent_running_tasks: Optional[str] = Field(max_length=500,default=None, description="agent正在执行的任务")
    agent_max_tasks: Optional[str] = Field(max_length=10, default=None, description="agent最大执行任务的能力")
    agent_cpu: Optional[str] = Field(max_length=10, default=None, description="agent机器上cpu负载")
    agent_memory: Optional[str] = Field(max_length=10, default=None, description="agent机器上内存负载")
    agent_io: Optional[str] = Field(max_length=10, default=None, description="agent机器上io的情况")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
