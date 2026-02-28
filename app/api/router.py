# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 15:44
# @Author  : lwc
# @File    : router.py
# @Description : 汇总所有路由

from fastapi import APIRouter
from app.api.v1 import auth
from app.api.v1.dashboard import dashboard
from app.api.v1.ifaceauto import api_reports
from app.api.v1.agent import agent
from app.api.v1.systems import users,depts,roles,menus
from app.api.v1.message_center import message_channel
from app.api.v1.host_management import server_setting, web_sockets

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(api_reports.router, prefix="/apireport", tags=["apireport"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(users.router, prefix="/systems", tags=["systems"])
api_router.include_router(depts.router, prefix="/systems", tags=["systems"])
api_router.include_router(roles.router, prefix="/systems", tags=["systems"])
api_router.include_router(menus.router, prefix="/systems", tags=["systems"])
api_router.include_router(message_channel.router, prefix="/message_center", tags=["message_center"])
api_router.include_router(server_setting.router, prefix="/server_setting", tags=["server_setting"])
api_router.include_router(web_sockets.router, prefix="/ws", tags=["ws"])

