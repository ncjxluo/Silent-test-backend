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

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(api_reports.router, prefix="/apireport", tags=["apireport"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

