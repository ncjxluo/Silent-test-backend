# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 13:47
# @Author  : lwc
# @File    : agent.py
# @Description : agent 相关的路由和方法
import asyncio
import json
import os
from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.util.preloaded import orm_util
from typing import List
from app.core.dependencies import get_current_user
from app.services.agent.agent_service import AgentService
from app.schemas.base import ApiResponse
from app.schemas.agent.agent_schema import AgentResponse, MergeAgentHeart,AgentTaskResponse
from app.utils.helper import get_storage_profiler_path
import subprocess

router = APIRouter()


@router.post("/agent_heart_beat")
async def agent_heart_beat(obj:MergeAgentHeart):
    # print(agent_key, agent_name, status, agent_running_tasks, agent_cpu, agent_memory, agent_io)
    await AgentService.merge_api_agent(
        obj.agent_key, obj.agent_name, obj.status, obj.agent_running_tasks, obj.agent_max_tasks, obj.agent_cpu, obj.agent_memory, obj.agent_io
    )
    print(obj)


@router.get("/get_api_agents", response_model=ApiResponse[AgentResponse])
async def get_api_agents(current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    data = await AgentService.get_all_api_agent(current_page, current_count)
    return ApiResponse(data=data) # type: ignore


@router.get("/get_task", response_model=ApiResponse[List[AgentTaskResponse]])
async def get_task(agent_id:str):
    data = await AgentService.get_tasks(agent_id)
    print(f"任务{data}")
    return ApiResponse(data=data) # type: ignore


@router.post("/api_agent_upload_profile")
async def api_agent_upload_profile(
    file_name: str = Form(...),
    event_type: str = Form(...),
    file: UploadFile = File(...)
):

    # jfr_filename = f"{file_name}"
    jfr_path = os.path.join(get_storage_profiler_path(), file_name)

    with open(jfr_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            print(f"保存进度: {file.content_type}")
            f.write(chunk)

    # for item in event_type.split(','):
    #     html_filename = file_name.replace(".jfr", f"-{item}.html")
    #     html_path = os.path.join(get_storage_profiler_path(), html_filename)
    #     try:
    #         cmd = ["/opt/async-profiler/bin/jfrconv", f'--{item}', jfr_path, html_path]
    #         # with open(html_path, "w") as f:
    #         # subprocess.run(cmd)
    #         await asyncio.create_subprocess_exec(*cmd)
    #     except Exception as e:
    #         html_path = ""
    #         print(f"❌ 转换失败: {e}")

    return {
        "msg": "ok",
        "jfr_path": jfr_path
    }