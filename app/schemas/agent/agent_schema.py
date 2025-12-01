# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 17:59
# @Author  : lwc
# @File    : agent_schema.py
# @Description : agent 返回的响应数据类型接口

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AgentItem(BaseModel):

    agent_key: str
    agent_name: str
    agent_status: Optional[int]
    agent_running_tasks: Optional[str]
    agent_max_tasks: Optional[str]
    agent_cpu: Optional[str]
    agent_memory: Optional[str]
    agent_io: Optional[str]
    created_at: datetime
    updated_at: datetime

class AgentResponse(BaseModel):
    total_count: int
    agents: List[AgentItem]