# -*- coding: utf-8 -*-
# @Time    : 2026/3/9 17:21
# @Author  : lwc
# @File    : taskcenter.py
# @Description :

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from typing import List
from app.schemas.test_resource.task_center_schema import AddKanbanRequest,KanbansResponse,EditKanbanRequest,DelKanbanRequest,DelKanbanColumnRequest,AddTaskRequest,TasksResponse,ColumnsTasksResponse,EditKanbanTasksRequest,EditTaskRequest,DelTaskRequest,DelTaskDetailsRequest
from app.services.test_resource.task_center_services import TaskCenterService

router = APIRouter()


@router.post("/add_kanban_temp",response_model=ApiResponse)
async def add_kanban_temp(obj:AddKanbanRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.add_kanban_temp(obj.board_name,obj.kanban_columns,obj.board_description)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_kanban_temp",response_model=ApiResponse[KanbansResponse])
async def get_kanban_temp(k_name:str=None, current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.get_kanban_temp(k_name, current_page, current_count)
    return ApiResponse(data=res) # type: ignore

@router.post("/edit_kanban_temp",response_model=ApiResponse)
async def edit_kanban_temp(obj:EditKanbanRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.edit_kanban_temp(obj.board_key, obj.board_name, obj.kanban_columns, obj.board_description)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_kanban_temp",response_model=ApiResponse)
async def del_kanban_temp(obj:DelKanbanRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.del_kanban_temp(obj.board_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_kanban_column",response_model=ApiResponse)
async def del_kanban_column(obj:DelKanbanColumnRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.del_kanban_column(obj.column_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/add_task",response_model=ApiResponse)
async def add_task(obj:AddTaskRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.add_task(
        obj.task_name, obj.task_num, obj.version_num, obj.release_time, '未开始', obj.board_key, obj.task_details
    )
    if res.get("msg") == "新增成功":
        await TaskCenterService.send_task_message(obj.message_info)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_tasks",response_model=ApiResponse[TasksResponse])
async def get_tasks(task_label_name:str, task_condition:str, current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    print(task_condition)
    print(task_label_name)
    res = await TaskCenterService.get_tasks(task_label_name, task_condition, current_page, current_count)
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_task",response_model=ApiResponse)
async def edit_task(obj:EditTaskRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.edit_task(obj.task_key, obj.task_name, obj.task_num, obj.version_num, obj.release_time, obj.board_key, obj.task_details)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_task",response_model=ApiResponse)
async def del_task(obj:DelTaskRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.del_task(obj.task_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_task_details",response_model=ApiResponse)
async def del_task_details(obj:DelTaskDetailsRequest, current_user_key: str = Depends(get_current_user)):
    res = await TaskCenterService.del_task_details(obj.task_details_key)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_kanban_columns_tasks",response_model=ApiResponse[ColumnsTasksResponse])
async def get_kanban_columns_tasks(k_switch:bool=True, task_key:str=None, board_key:str=None, condition:str=None, current_user_key: str = Depends(get_current_user)):
    print('进来了')
    res = await TaskCenterService.get_kanban_columns_tasks(k_switch,task_key, board_key, condition, current_user_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_kanban_tasks",response_model=ApiResponse)
async def edit_kanban_tasks(obj:EditKanbanTasksRequest, current_user_key: str = Depends(get_current_user)):
    if obj.assignee_key != current_user_key:
        return ApiResponse(data={"msg": "暂时不支持移动他人的任务"}) # type: ignore
    res = await TaskCenterService.edit_kanban_tasks(obj.task_key, obj.task_details_key, obj.column_key, obj.column_status)
    return ApiResponse(data=res) # type: ignore