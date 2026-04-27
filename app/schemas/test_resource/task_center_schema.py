# -*- coding: utf-8 -*-
# @Time    : 2026/3/9 17:21
# @Author  : lwc
# @File    : task_center_schema.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class KanbanColumn(BaseModel):
    column_name: str
    sort_order: str
    column_status: str

class AddKanbanRequest(BaseModel):

    board_name: str
    kanban_columns: List
    board_description: str

class KanbanItem(BaseModel):

    column_key: Optional[str]
    column_name: Optional[str]
    sort_order: Optional[str]
    column_status: Optional[str]


class KanbanResponse(BaseModel):
    board_key: Optional[str]
    board_name: Optional[str]
    board_description: Optional[str]
    kanban_columns: Optional[str]
    child_item: Optional[List[KanbanItem]] = []


class KanbansResponse(BaseModel):
    total_count: int
    kanbans: List[KanbanResponse]

class EditKanbanRequest(BaseModel):

    board_key: str
    board_name: str
    kanban_columns: List
    board_description: str

class DelKanbanRequest(BaseModel):

    board_key: str

class DelKanbanColumnRequest(BaseModel):

    column_key: str

class AddTaskRequest(BaseResponseModel):

    task_name: str
    board_key: str
    task_num: int
    version_num: str
    release_time: str
    task_details: List
    message_info: dict

class EditTaskRequest(BaseResponseModel):
    task_key: str
    task_name: str
    board_key: str
    task_num: int
    version_num: str
    release_time: str
    task_details: List

class DelTaskRequest(BaseModel):

    task_key: str

class DelTaskDetailsRequest(BaseModel):

    task_details_key: str

class TaskItem(BaseModel):

    task_details_key: Optional[str]
    task_details_title: Optional[str]
    correlation_num: Optional[str]
    description: Optional[str]
    priority: Optional[str]
    assignee_key: Optional[str]
    expect_day: Optional[str]


class TaskResponse(BaseModel):
    task_key: Optional[str]
    task_name: Optional[str]
    task_num: Optional[str]
    version_num: Optional[str]
    release_time: Optional[str]
    is_complete: Optional[str]
    board_key: Optional[str]
    child_item: Optional[List[TaskItem]] = []


class TasksResponse(BaseModel):
    total_count: int
    tasks: List[TaskResponse]


class ColumnsTaskItem(BaseModel):

    task_key: Optional[str]
    task_details_key: Optional[str]
    task_details_title: Optional[str]
    correlation_num: Optional[str]
    description: Optional[str]
    priority: Optional[str]
    assignee_key: Optional[str]
    expect_day: Optional[str]

class ColumnsTask(BaseModel):

    board_key: Optional[str]
    column_key: Optional[str]
    column_name: Optional[str]
    sort_order: Optional[str]
    column_status: Optional[str]
    tasks: Optional[List[ColumnsTaskItem]] = []

class ColumnsTasksResponse(BaseModel):
    tasks: List[ColumnsTask]

class EditKanbanTasksRequest(BaseModel):

    assignee_key: str
    task_key: str
    task_details_key: str
    column_key: str
    column_status:str