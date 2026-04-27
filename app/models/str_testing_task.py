# -*- coding: utf-8 -*-
# @Time    : 2026/3/8 16:26
# @Author  : lwc
# @File    : str_testing_task.py
# @Description : 测试的任务表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class StrTestingTask(SQLModel, table=True):

    __tablename__ = 'str_testing_task'

    task_key: str = Field(max_length=100, default_factory=lambda: str(uuid.uuid4()), primary_key=True,
                          description="大任务的uuid，作为唯一标识符")
    task_name: str = Field(max_length=200, default=None, description="大任务的名字")
    task_num: str = Field(max_length=200, default=None, description="细则任务的数量")
    version_num: str = Field(max_length=20, default=None, description="要发的版本号")
    release_time: str = Field(max_length=50, default=None, description="发版的时间")
    is_complete: str = Field(max_length=50, default=None, description="是否完成")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())