# -*- coding: utf-8 -*-
# @Time    : 2025/11/11 14:20
# @Author  : lwc
# @File    : apireports.py
# @Description : 接口自动化报告的路由

from fastapi import APIRouter, Depends
from typing import List
from app.core.dependencies import get_current_user
from app.services.ifaceauto.api_reports import ApiReportsService
from app.schemas.ifaceauto.api_report_schema import GroupedSuitesResponse, PlansResponse, CasesStatisticResponse,CasesResponse,PathSelectResponse,EditCaseRequest,SubmitZentaoRequest,MonitorReportRequest
from app.schemas.base import ApiResponse
from fastapi.responses import StreamingResponse
import os
from app.utils.helper import get_realpath


router = APIRouter()

@router.get("/get_api_all_reports",response_model=ApiResponse[GroupedSuitesResponse])
async def get_api_all_reports(current_user_key: str = Depends(get_current_user)):
    suites = await ApiReportsService.get_all_suites()
    return ApiResponse(data=suites) # type: ignore


@router.get("/get_api_all_plans",response_model=ApiResponse[PlansResponse])
async def get_api_all_plans(suite_key:str = '-1111111', current_page:int = 1, current_count:int = 30, plan_name:str = None, current_user_key: str = Depends(get_current_user)):
    plans = await ApiReportsService.get_all_plans(suite_key, current_page, current_count, plan_name)
    return ApiResponse(data=plans) # type: ignore


@router.get("/get_api_all_cases_statistic",response_model=ApiResponse[CasesStatisticResponse])
async def get_api_all_cases_statistic(suite_key:str = "0", plan_key: str = "0", current_user_key: str = Depends(get_current_user)):
    cases = await ApiReportsService.get_cases_statistic(suite_key, plan_key)
    return ApiResponse(data=cases) # type: ignore


@router.get("/get_api_all_cases", response_model=ApiResponse[CasesResponse])
async def get_api_all_cases(suite_key:str = "0", plan_key: str = "0", current_page:int = 1, current_count:int = 30, path:str = None, status:str = None, s_time:str = None, e_time:str = None, fuzzy_search:str = None , current_user_key: str = Depends(get_current_user)):
    print(fuzzy_search)
    data = await ApiReportsService.get_cases(suite_key, plan_key, current_page, current_count, path, status, s_time, e_time,fuzzy_search)
    return ApiResponse(data=data) # type: ignore


@router.get("/get_api_path_select", response_model=ApiResponse[List[PathSelectResponse]])
async def get_api_path_select(suite_key:str = "0", plan_key: str = "0",current_user_key: str = Depends(get_current_user)):
    data = await ApiReportsService.get_path_select(suite_key,plan_key)
    print(data)
    return ApiResponse(data=data) # type: ignore


@router.post("/edit_api_cases", response_model=ApiResponse)
async def edit_api_cases(obj:EditCaseRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiReportsService.edit_case(
        obj.suite_key, obj.plan_key, obj.case_key, obj.remarks
    )
    return ApiResponse(data=res) # type: ignore


@router.post("/submit_zentao", response_model=ApiResponse)
async def submit_zentao(obj:SubmitZentaoRequest, current_user_key: str = Depends(get_current_user)):
    await ApiReportsService.submit_zentao(obj.suite_key, obj.plan_key)
    res = {}
    return ApiResponse(data=res) # type: ignore


@router.post("/monitor_report", response_model=ApiResponse)
async def monitor_report(obj:MonitorReportRequest, current_user_key: str = Depends(get_current_user)):

    res = await ApiReportsService.monitor_report(obj.start_time, obj.end_time)

    return ApiResponse(data=res) # type: ignore


@router.get("/download_jfr", response_model=ApiResponse)
def download_jfr(url: str):
    # client = httpx.AsyncClient()
    # 2. 流式请求（和 requests 的 stream=True 完全一样）
    # r = client.get(url)
    # 2. 强制浏览器下载（关键！）
    res = {"msg": "文件不存在"}
    all_path = get_realpath(url)
    if not os.path.exists(all_path):
        return ApiResponse(data=res) # type: ignore
    name_list = url.split("/")
    # 3. 返回流式下载
    return StreamingResponse(
        file_iterator(all_path),
        headers={
            "Content-Disposition": f'attachment; filename="{name_list[len(name_list)-1]}"'
        },
        media_type="application/octet-stream"
    )

    # return ApiResponse(data=res) # type: ignore

def file_iterator(file_path: str, chunk_size=1024 * 1024):
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk