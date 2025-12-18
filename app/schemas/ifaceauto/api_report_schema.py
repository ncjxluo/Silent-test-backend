# -*- coding: utf-8 -*-
# @Time    : 2025/11/11 14:54
# @Author  : lwc
# @File    : api_report_schema.py
# @Description : 定义接口自动化报告树的返回体

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from pydantic import RootModel
from datetime import datetime


class ApiSuiteResponse(BaseModel):

    suite_key: Optional[str]
    suite_name: Optional[str]
    status: Optional[str]
    created_at: Optional[datetime]
    progress: Optional[str]


class GroupedSuitesResponse(RootModel[Dict[str, List[ApiSuiteResponse]]]):
    pass


class ApiPlansResponse(BaseModel):

    id: Optional[int]
    suite_key: Optional[str]
    plan_key: Optional[str]
    plan_name: Optional[str]
    plan_task_sum: Optional[int]
    failed_case_num: Optional[int]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PlansResponse(BaseModel):
    total_count: int
    plans: List[ApiPlansResponse]


class CaseStatisticInterFace(BaseModel):
    case_path: Optional[str]
    request_count: Optional[str]
    avg_response_time: Optional[str]
    min_response_time: Optional[str]
    max_response_time: Optional[str]
    median: Optional[str]
    p90_response_time: Optional[str]
    p95_response_time: Optional[str]
    p99_response_time: Optional[str]


class CasesStatisticResponse(BaseModel):
    total_cases: Optional[str] = "暂无数据"
    fail_cases: Optional[str] = "暂无数据"
    success_cases: Optional[str] = "暂无数据"
    pass_rate_percent: Optional[str] = "暂无数据"
    case_statistic: Optional[List[CaseStatisticInterFace]] = []


class CasesItem(BaseModel):
    step_id: Optional[str]
    step_name: Optional[str]
    user_variables: Optional[str]
    request_url: Optional[str]
    request_param: Optional[str]
    real_response: Optional[str]
    response_time: Optional[str]
    assert_res_sign: Optional[str]
    assert_res_details: Optional[str]
    assert_ver_sign: Optional[str]
    assert_time_sign: Optional[str]



class CaseResponse(BaseModel):
    case_key: Optional[str]
    case_status: Optional[str]
    sql: Optional[str] = None
    remarks: Optional[str]
    child_item: Optional[List[CasesItem]] = []


class CasesResponse(BaseModel):
    total_count: int
    cases: List[CaseResponse]


class PathSelectResponse(BaseModel):
    path: Optional[str]


class EditCaseRequest(BaseModel):
    suite_key: str
    plan_key: str
    case_key: str
    remarks: Optional[str]