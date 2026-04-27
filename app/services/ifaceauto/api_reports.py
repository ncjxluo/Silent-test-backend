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
from datetime import datetime
import json
import httpx


class ApiReportsService:

    @staticmethod
    async def get_all_suites():
        suites = await ApiReportsDao.get_all_suites()
        grouped = defaultdict(list)
        for suite in suites:
            # date = suite.created_at.strftime("%Y-%m-%d")
            date = datetime.fromtimestamp(suite.created_at / 1000).strftime("%Y-%m-%d")
            if suite.has_not_ready_plan > 0 and int(suite.progress) < 1:
                suite_status = "running"
            elif int(suite.progress) == 1 and suite.status != 'finish':
                suite_status = "finish"
            else:
                suite_status = ""
            if suite_status != "":
                await ApiReportsDao.set_suite_status(suite.suite_key, suite_status)
            grouped[date].append({"suite_key": suite.suite_key, "suite_name": suite.suite_name, "status": suite.status,
                                  "created_at": suite.created_at, "updated_at": suite.updated_at, "progress": str(int(suite.progress * 100))})
        return dict(grouped)

    @staticmethod
    async def get_all_plans(suite_key: str, current_page:int = 1, current_count:int = 30, plan_name:str = None):
        if suite_key == '-1111111':
            plans: List[StrTestPlan] = []
            total_count = [0]
        else:
            plans: List[StrTestPlan] = await ApiReportsDao.get_all_plans_new(suite_key, current_page, current_count,plan_name)
            total_count = await ApiReportsDao.get_all_plans_counts(suite_key,plan_name)
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

    # @staticmethod
    # async def get_cases(suite_key: str, plan_key: str, current_page:int = 1, current_count:int = 30, path:str = None, status:str = None, s_time:str = None, e_time:str = None, fuzzy_search:str = None):
    #     if not is_empty(path) and all(is_empty(param) for param in [status,s_time,e_time,fuzzy_search]):
    #         case_data = await ApiReportsDao.get_case_datas(suite_key, plan_key, current_page, current_count)
    #         case_count = await ApiReportsDao.get_case_key_count(suite_key, plan_key)
    #     elif not is_empty(path) and not is_empty(status) and not is_empty(fuzzy_search) and all(is_empty(param) for param in [s_time,e_time]):
    #         case_data = await ApiReportsDao.get_case_datas(suite_key, plan_key, current_page, current_count,status=status,fuzzy_search=fuzzy_search)
    #         case_count = await ApiReportsDao.get_case_key_count(suite_key, plan_key, status=status,fuzzy_search=fuzzy_search)
    #     else:
    #         case_data = await ApiReportsDao.get_case_datas(suite_key, plan_key, current_page, current_count, status=status, s_time=s_time, e_time=e_time, path=path,fuzzy_search=fuzzy_search)
    #         case_count = await ApiReportsDao.get_case_key_count(suite_key, plan_key, status=status, s_time=s_time, e_time=e_time, path=path,fuzzy_search=fuzzy_search)
    #     result_list = []
    #     grouped = groupby(case_data, key=lambda x: x["case_key"])
    #
    #     for case_key, group in grouped:
    #         dic1 = dict()
    #         dic1["case_key"] = case_key
    #         dic1["case_status"] = "success"
    #         dic1["remarks"] = None
    #         c_lis = list()
    #         for item1 in group:
    #             if dic1["remarks"] is None:
    #                 dic1["remarks"] = item1.remarks
    #             if "precheck" in item1.request_url:
    #                 dic1["sql"] = json.loads(item1.request_param).get("sql")
    #             if item1.case_status == 1 and dic1["case_status"] == "success":
    #                 dic1["case_status"] = "fail"
    #             if is_empty(path):
    #                 c_lis.append(item1)
    #             else:
    #                 if item1.request_url == path:
    #                     c_lis.append(item1)
    #         dic1["child_item"] = c_lis
    #         result_list.append(dic1)
    #     return {"total_count": case_count[0], "cases": result_list}

    @staticmethod
    async def get_cases(suite_key: str, plan_key: str, current_page: int = 1, current_count: int = 30, path: str = None,
                        status: str = None, s_time: str = None, e_time: str = None, fuzzy_search: str = None):
        case_keys, total_count = await ApiReportsDao.get_paginated_case_keys(
            suite_key, plan_key, current_page, current_count, path, s_time, e_time, fuzzy_search, status
        )
        print(f"case_keys{case_keys}")
        if not case_keys:
            return {"total_count": total_count, "cases": []}
        detail_resp = await ApiReportsDao.get_case_steps(suite_key, plan_key, case_keys)
        all_steps = [hit["_source"] for hit in detail_resp["hits"]["hits"]]
        grouped_steps = defaultdict(list)
        case_status_map = {}  # case_key -> status
        for step in all_steps:
            ck = step["case_key"]
            grouped_steps[ck].append(step)
            if ck not in case_status_map:
                case_status_map[ck] = 0
            if step.get("assert_res_sign") == "整体断言:失败":
                case_status_map[ck] = 1
        case_map = await ApiReportsDao.get_case_datas(case_keys)
        result_list = []
        for ck in case_keys:  # 用第一步返回的顺序，保证分页稳定
            case_info = case_map.get(ck, {
                "suite_key": suite_key,
                "plan_key": plan_key,
                "case_key": ck,
                "remarks": None,
                "created_at": None,
                "updated_at": None,
            })
            case_info["case_status"] = "success" if case_status_map.get(ck, 0) == 0 else "fail"
            steps = grouped_steps.get(ck, [])
            for step in steps:
                if "step_id" in step and isinstance(step["step_id"], (int, float)):
                    step["step_id"] = str(step["step_id"])  # 转成字符串
                if "user_variables" in step and isinstance(step["user_variables"], dict):
                    step["user_variables"] = json.dumps(step["user_variables"], ensure_ascii=False)
                request_url = step.get("request_url", "")
                if "precheck" in request_url and request_url:
                    req_param = step.get("request_param")
                    if isinstance(req_param, str):
                        param_dict = json.loads(req_param)
                    elif isinstance(req_param, dict):
                        param_dict = req_param
                    else:
                        param_dict = {}
                    sql_value = param_dict.get("sql") if isinstance(param_dict, dict) else None
                    if sql_value is not None:
                        case_info["sql"] = sql_value  # 直接在 step 上新增 sql 字段
            case_info["child_item"] = grouped_steps.get(ck, [])
            result_list.append(case_info)
        return {"total_count": total_count, "cases": result_list}


    @staticmethod
    async def get_path_select(suite_key: str, plan_key: str):
        res = await ApiReportsDao.get_case_path_select(suite_key, plan_key)
        data = [ {"path": item} for item in res]
        return data

    @staticmethod
    async def edit_case(suite_key: str, plan_key: str, case_key:str, remarks:str):
        res = await ApiReportsDao.edit_case(suite_key, plan_key, case_key, remarks)
        return res

    @staticmethod
    async def submit_zentao(suite_key: str, plan_key: str):
        res_data = await ApiReportsDao.submit_zentao(suite_key, plan_key)
        result_list = []
        grouped = groupby(res_data, key=lambda x: x["case_key"])
        for case_key, group in grouped:
            dic1 = dict()
            dic1["case_key"] = case_key
            dic1["case_status"] = "失败"
            dic1["case_step_name"] = ''
            dic1["step_details"] = ''
            for item1 in group:
                if "plan_name" not in dic1:
                    dic1["plan_name"] = item1.plan_name
                dic1["case_step_name"] = dic1.get("case_step_name") + item1.step_name
                dic1["case_env"] = item1.user_variables
                dic1["step_details"] = f"""
                {dic1.get("step_details")}<p></p><p>步骤:<p>{item1.step_id}</p><p>请求接口:</p>
                <p>{item1.request_url}</p><p>请求参数:</p><p>{item1.request_param}</p><p>真实返回:</p><p>{item1.real_response}</p><p>该步骤的期望:</p><p>{item1.assert_res_details}</p>
                """
            result_list.append(dic1)
        async with httpx.AsyncClient() as client:
            interface_prefix = "http://192.168.1.212/zentao/api.php/v1"
            response = await client.post(
                url= f"{interface_prefix}/tokens",
                json={"account": "wcheng.luo", "password": "luowencheng"},
                timeout=10  # 超时时间（可选）
            )
            token = response.json().get("token")
            for index in range(0,1):
                p_data = {
                    "branch": 0,
                    "title": f'【接口自动化】[{result_list[index].get("plan_name")}][{result_list[index].get("case_key")}][{result_list[index].get("case_step_name")}][{result_list[index].get("case_status")}]',
                    "severity": 3,
                    "pri": 3,
                    "steps": f'<p>前置条件: {result_list[index].get("case_env")}</p><p></p><p>详情:</p>{result_list[index].get("step_details")}</p>',
                    "type": "codeerror",
                    "openedBuild": [
                        "trunk"
                    ]
                }
                response = await client.post(
                    url=f"{interface_prefix}/products/20/bugs",
                    json=p_data,
                    headers = {
                        "Content-Type": "application/json",  # 可加（但 json 参数会自动加，冗余）
                        "token": token
                    }
                )
        return {}

    @staticmethod
    async def monitor_report(start_time:int, end_time:int):
        res = await ApiReportsDao.monitor_report(start_time, end_time)
        print(f"监控数据{res}")
        # grouped = defaultdict(list)
        monitor_data = {}
        metrics = []
        alerts = []
        count = 0
        for item in res:
            metrics.append(
                {
                    "timestamp": item.get("created_at"),
                    "container": item.get("container_name"),
                    "cpu": item.get("cpu_usage"),
                    "mem": item.get("mem_percent"),
                    "io": item.get("blkio_bytes"),
                    "lock": item.get("lock_wait"),
                    "alert": {
                      "has": 'false' if item.get("trigger_time",'无') == '无' else 'true',
                      "flameGraphUrl": item.get("file_path")
                    }
                }
            )
            if item.get("trigger_time",'无') != '无':
                alerts.append({
                    "id": f'id-{count}',
                    "timestamp": item.get("trigger_time"),
                    "container": item.get("container_name"),
                    "cpu": item.get("cpu_usage"),
                    "mem": item.get("mem_percent"),
                    "io": item.get("blkio_bytes"),
                    "lock": item.get("lock_wait"),
                    "type": item.get("event_type"),
                    "flameGraphUrl": item.get("file_path"),
                })
                count = count + 1
        monitor_data["metrics"] = metrics
        monitor_data["alerts"] = alerts
        return monitor_data