# -*- coding: utf-8 -*-
# @Time    : 2025/10/20 10:45
# @Author  : lwc
# @File    : main.py
# @Description :

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.utils.helper import get_config
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.time_job import api_agent_watchdog
import asyncio
from contextlib import asynccontextmanager


PROJECT_NAME=get_config().get("base").get("project_name")
VERSION=get_config().get("base").get("version")
API_STR=get_config().get("base").get("back_api_str")

app = FastAPI(title=PROJECT_NAME, version=VERSION)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix=API_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 你的前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
    # expose_headers=["set-cookie"]
)

@asynccontextmanager
async def lifespan(app:FastAPI):
    asyncio.create_task(api_agent_watchdog())
    yield

app.router.lifespan_context = lifespan

if __name__ == '__main__':
    uvicorn.run(app="main:app", host=r"0.0.0.0", port=8000, reload=True)