# -*- coding: utf-8 -*-
# @Time    : 2025/11/11 14:43
# @Author  : lwc
# @File    : api_reports.py
# @Description : 定义获取接口自动化测试报告的业务方法

from app.dao.ifaceauto.api_reports import ApiReportsDao
from app.models.str_test_case import StrTestCase
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
from app.schemas.ifaceauto.api_report_schema import CasesStatisticResponse,CaseStatisticInterFace,CasesResponse,CasesItem
from typing import List
from collections import defaultdict
from itertools import groupby
from app.utils.my_util import is_empty
import json


class ApiReportsService:

    # @staticmethod
    # async def get_all_suites():
    #     suites: List[StrTestSuite] = await ApiReportsDao.get_all_suites()
    #     grouped = defaultdict(list)
    #     for suite in suites:
    #         date = suite.created_at.strftime("%Y-%m-%d")
    #         grouped[date].append({"suite_key": suite.suite_key,"suite_name": suite.suite_name,"status": suite.status,"created_at": suite.created_at})
    #     print(f"services 层 的{dict(grouped)}")
    #     return dict(grouped)

    @staticmethod
    async def get_all_suites():
        suites = await ApiReportsDao.get_all_suites_new()
        grouped = defaultdict(list)
        for suite in suites:
            date = suite.created_at.strftime("%Y-%m-%d")
            grouped[date].append({"suite_key": suite.suite_key, "suite_name": suite.suite_name, "status": suite.status,
                                  "created_at": suite.created_at, "progress": str(int(suite.progress * 100))})
        print(f"services 层 的{dict(grouped)}")
        return dict(grouped)

    @staticmethod
    async def get_all_plans(suite_key: str, current_page:int = 1, current_count:int = 30):
        if suite_key == '-1111111':
            plans: List[StrTestPlan] = []
            total_count = [0]
        else:
            plans: List[StrTestPlan] = await ApiReportsDao.get_all_plans_new(suite_key, current_page, current_count)
            total_count = await ApiReportsDao.get_all_plans_counts(suite_key)
        print(plans)
        print(f"services 层 的{plans}")
        return {"total_count": total_count[0], "plans": plans}

    @staticmethod
    async def get_cases_statistic(suite_key: str, plan_key: str):
        cases_basic = await ApiReportsDao.get_cases_statistic_basic_indicator(suite_key, plan_key)
        cases_performance_indicator = await ApiReportsDao.get_cases_statistic_performance_indicator(suite_key, plan_key)
        basic_fields = ["total_cases", "fail_cases", "success_cases", "pass_rate_percent"]
        basic_data = {}
        if cases_basic and cases_basic[0]:
            for i, field in enumerate(basic_fields):
                value = cases_basic[0][i]
                basic_data[field] = str(value) if value is not None else "暂无数据"
        else:
            basic_data = {field: "暂无数据" for field in basic_fields}
        performance_fields = [
            "case_path", "request_count", "avg_response_time",
            "min_response_time", "max_response_time", "median", "p90_response_time", "p95_response_time", "p99_response_time"
        ]
        case_statistics = []
        if cases_performance_indicator:
            for index in range(0, len(cases_performance_indicator)):
                case_data = {}
                for i, field in enumerate(performance_fields):
                    value = cases_performance_indicator[index][i]
                    case_data[field] = str(value) if value is not None else None
                case_statistics.append(CaseStatisticInterFace(**case_data))
        return CasesStatisticResponse(**basic_data, case_statistic=case_statistics)

    @staticmethod
    async def get_cases(suite_key: str, plan_key: str, current_page:int = 1, current_count:int = 30, path:str = None, status:str = None, s_time:str = None, e_time:str = None):
        if not is_empty(path) and all(is_empty(param) for param in [status,s_time,e_time]):
            case_data = await ApiReportsDao.get_case_datas(suite_key, plan_key, current_page, current_count)
            case_count = await ApiReportsDao.get_case_key_count(suite_key, plan_key)
        elif not is_empty(path) and not is_empty(status) and all(is_empty(param) for param in [s_time,e_time]):
            case_data = await ApiReportsDao.get_case_datas(suite_key, plan_key, current_page, current_count,status=status)
            case_count = await ApiReportsDao.get_case_key_count(suite_key, plan_key, status=status)
        else:
            case_data = await ApiReportsDao.get_case_datas(suite_key, plan_key, current_page, current_count, status=status, s_time=s_time, e_time=e_time, path=path)
            case_count = await ApiReportsDao.get_case_key_count(suite_key, plan_key, status=status, s_time=s_time, e_time=e_time, path=path)
        result_list = []
        grouped = groupby(case_data, key=lambda x: x["case_key"])
        for case_key, group in grouped:
            dic1 = dict()
            dic1["case_key"] = case_key
            dic1["case_status"] = "success"
            dic1["remarks"] = None
            c_lis = list()
            for item1 in group:
                if dic1["remarks"] is None:
                    dic1["remarks"] = item1.remarks
                if "precheck" in item1.request_url:
                    dic1["sql"] = json.loads(item1.request_param).get("sql")
                if item1.case_status == 1 and dic1["case_status"] == "success":
                    dic1["case_status"] = "fail"
                if is_empty(path):
                    c_lis.append(item1)
                else:
                    if item1.request_url == path:
                        c_lis.append(item1)
            dic1["child_item"] = c_lis
            result_list.append(dic1)
        return {"total_count": case_count[0], "cases": result_list}


    @staticmethod
    async def get_path_select(suite_key: str, plan_key: str):
        res = await ApiReportsDao.get_case_path_select(suite_key, plan_key)
        data = [ {"path": item} for item in res]
        return data

    @staticmethod
    async def edit_case(suite_key: str, plan_key: str, case_key:str, remarks:str):
        res = await ApiReportsDao.edit_case(suite_key, plan_key, case_key, remarks)
        return res