# -*- coding: utf-8 -*-
# @Time    : 2025/11/11 14:20
# @Author  : lwc
# @File    : apireports.py
# @Description : 接口自动化报告的路由

from fastapi import APIRouter, Depends
from typing import List
from app.core.dependencies import get_current_user
from app.services.ifaceauto.api_reports import ApiReportsService
from app.schemas.ifaceauto.api_report_schema import GroupedSuitesResponse, PlansResponse, CasesStatisticResponse,CasesResponse,PathSelectResponse
from app.schemas.base import ApiResponse


router = APIRouter()

@router.get("/get_api_all_reports",response_model=ApiResponse[GroupedSuitesResponse])
async def get_api_all_reports(current_user_key: str = Depends(get_current_user)):
    suites = await ApiReportsService.get_all_suites()
    return ApiResponse(data=suites) # type: ignore


@router.get("/get_api_all_plans",response_model=ApiResponse[PlansResponse])
async def get_api_all_plans(suite_key:str = 0, current_page:int = 1, current_count:int = 30, current_user_key: str = Depends(get_current_user)):
    plans = await ApiReportsService.get_all_plans(suite_key, current_page, current_count)
    return ApiResponse(data=plans) # type: ignore


@router.get("/get_api_all_cases_statistic",response_model=ApiResponse[CasesStatisticResponse])
async def get_api_all_cases_statistic(suite_key:str = "0", plan_key: str = "0", current_user_key: str = Depends(get_current_user)):
    cases = await ApiReportsService.get_cases_statistic(suite_key, plan_key)
    return ApiResponse(data=cases) # type: ignore


@router.get("/get_api_all_cases", response_model=ApiResponse[CasesResponse])
async def get_api_all_cases(suite_key:str = "0", plan_key: str = "0", current_page:int = 1, current_count:int = 30, path:str = None, status:str = None, s_time:str = None, e_time:str = None , current_user_key: str = Depends(get_current_user)):
    print(status)
    data = await ApiReportsService.get_cases(suite_key, plan_key, current_page, current_count, path, status, s_time, e_time)

    return ApiResponse(data=data) # type: ignore


@router.get("/get_api_path_select", response_model=ApiResponse[List[PathSelectResponse]])
async def get_api_path_select(suite_key:str = "0", plan_key: str = "0"):
    data = await ApiReportsService.get_path_select(suite_key,plan_key)
    print(data)
    return ApiResponse(data=data) # type: ignore