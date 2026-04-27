# -*- coding: utf-8 -*-
# @Time    : 2026/3/8 16:26
# @Author  : lwc
# @File    : str_testing_task_details.py
# @Description :

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class StrTestingTaskDetails(SQLModel, table=True):

    __tablename__ = 'str_testing_task_details'

    task_details_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), primary_key=True, description="任务的uuid,唯一标识符")
    task_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), description="所属于大任务的uuid，作为唯一标识符")
    task_details_title: str = Field(max_length=200, default=None, description="任务的名字")
    correlation_num: str = Field(max_length=20, default=None, description="管理的需求号(禅道或者jira)")
    description: str = Field(max_length=200, default=None, description="任务的描述")
    priority: str = Field(max_length=10, default=None, description="优先级[高、中、低]")
    assignee_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), description="关联负责人的key")
    expect_day: str = Field(max_length=5, default=None, description="预估的时间天数")
    board_key: str = Field(max_length=100, default=None, description="处于看板模板的key")
    column_key: str = Field(max_length=100, default=None, description="出于看板模板列的key")
    is_complete: str = Field(max_length=50, default=None, description="是否完成")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())