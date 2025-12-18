# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 13:47
# @Author  : lwc
# @File    : agent.py
# @Description : agent 相关的路由和方法
import asyncio

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.agent.agent_service import AgentService
from app.schemas.base import ApiResponse
from app.schemas.agent.agent_schema import AgentResponse
from typing import List

router = APIRouter()


@router.get("/agent_heart_beat")
async def agent_heart_beat():

    print("我接受到了心跳")
    return {"message": "Hello agent"}



@router.get("/get_api_agents", response_model=ApiResponse[AgentResponse])
async def get_api_agents(current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    data = await AgentService.get_all_api_agent(current_page, current_count)
    return ApiResponse(data=data) # type: ignore
