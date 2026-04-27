# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 18:16
# @Author  : lwc
# @File    : message_channel.py
# @Description : 消息中心的api接口

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.message_center.message_services import MessageService
from app.schemas.message_center.message_channel_schema import TestSendMessageRequest,SaveMessageRequest,MessagesResponse,SettingMessageRequest,DelMessageRequest,MessageStatusResponse
import httpx
from typing import List

router = APIRouter()

@router.post("/test_send_message",response_model=ApiResponse)
async def test_send_message(obj:TestSendMessageRequest, current_user_key: str = Depends(get_current_user)):
    res = {}
    headers = {"Content-Type": "application/json"}
    message_info = {
        "msgtype": "text",
        "text": {
            "content": f"{obj.mes_info}",
            "mentioned_mobile_list": ["@all"]
        }
    }
    async with httpx.AsyncClient() as client:
        mes_response = await client.post(
            url=obj.mes_url,
            json=message_info,
            headers=headers
        )
    return ApiResponse(data={"msg": "发送成功"}) # type: ignore

@router.post("/save_message_channel",response_model=ApiResponse)
async def save_message_channel(obj:SaveMessageRequest, current_user_key: str = Depends(get_current_user)):
    res = await MessageService.save_message_channel(obj.mes_name, obj.mes_url, obj.mes_info, obj.is_enable)
    return ApiResponse(data=res)  # type: ignore


@router.get("/get_message_channel",response_model=ApiResponse[MessagesResponse])
async def get_message_channel(current_user_key: str = Depends(get_current_user)):
    res = await MessageService.get_message_channel()
    return ApiResponse(data=res)  # type: ignore

@router.get("/get_message_channel_status",response_model=ApiResponse[List[MessageStatusResponse]])
async def get_message_channel_status(status:int, current_user_key: str = Depends(get_current_user)):
    res = await MessageService.get_message_channel_status(status)
    return ApiResponse(data=res)  # type: ignore


@router.post("/setting_message_status",response_model=ApiResponse)
async def setting_message_status(obj:SettingMessageRequest, current_user_key: str = Depends(get_current_user)):
    res = await MessageService.setting_message_status(obj.mes_key, obj.is_enable)
    return ApiResponse(data=res)  # type: ignore

@router.post("/del_message_channel",response_model=ApiResponse)
async def del_message_channel(obj:DelMessageRequest, current_user_key: str = Depends(get_current_user)):
    res = await MessageService.delete_message_cchannel(obj.mes_key)
    return ApiResponse(data=res)  # type: ignore