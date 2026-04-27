# -*- coding: utf-8 -*-
# @Time    : 2025/11/3 11:35
# @Author  : lwc
# @File    : str_test_suite.py
# @Description : 测试套件，其实应该是测试任务表

import uuid
from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime
from sqlalchemy import SMALLINT


class StrTestSuite(SQLModel, table=True):

    __tablename__ = 'str_test_suite'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_key: str = Field( max_length=100, description="执行这个任务的用户id")
    suite_key: str = Field(max_length=100, index=True, default_factory=lambda: str(uuid.uuid4()),description="测试任务的key")
    suite_name: str = Field(max_length=100, description="测试任务的名字，前端下发时的")
    suite_agent_key: str = Field(max_length=100, description="下发给agent")
    twins_flame: int = Field(sa_type=SMALLINT, default=0, description="是否开启双生焰监控")
    status: str = Field(max_length=20, description="测试任务的状态")
    type: str = Field(max_length=20, description="测试任务的类别")
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000),sa_column_kwargs={
            "onupdate": lambda: int(datetime.now().timestamp() * 1000)
        })

