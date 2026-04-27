# -*- coding: utf-8 -*-
# @Time    : 2025/11/11 14:23
# @Author  : lwc
# @File    : api_reports.py
# @Description : 定义获取接口自动化测试报告的数据访问方法
from annotated_types.test_cases import cases
from app.core.es import es
from app.core.db import async_session
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
from app.models.str_test_case import StrTestCase
from app.models.str_test_case_step import StrTestCaseStep
from sqlmodel import select, and_, desc, func, text, distinct, cast, DECIMAL, case, update
from app.utils.my_util import is_empty
from datetime import datetime
from typing import List


class ApiReportsDao:
    @staticmethod
    async def set_suite_status(suite_key:str, status:str):
        async with async_session() as session:
            await session.execute(
                update(StrTestSuite).where(
                    StrTestSuite.suite_key == suite_key
                ).values(
                    status=status
                )
            )
            await session.commit()

    @staticmethod
    async def get_all_suites():
        async with async_session() as session:
            query = text(
                f"""
                    SELECT
                        a.suite_key,
                        a.suite_name,
                        a.status,
                        a.created_at,
                        a.updated_at,
                        CASE 
                            WHEN COUNT(b.plan_key) = 0 THEN 0
                            ELSE ROUND(SUM(CASE WHEN b.status = 'finish' THEN 1 ELSE 0 END) / COUNT(b.plan_key), 2)
                        END as progress,
                        CASE 
                            WHEN COUNT(b.plan_key) = 0 THEN 0
                            WHEN EXISTS (
                                SELECT 1 
                                FROM str_test_plan 
                                WHERE suite_key = a.suite_key 
                                AND status != 'ready'
                            ) THEN 1 
                            ELSE 0 
                        END as has_not_ready_plan
                    FROM
                        `str_test_suite` as a 
                    LEFT JOIN 
                        str_test_plan as b on a.suite_key = b.suite_key
                    WHERE a.type = 'api'
                    GROUP BY a.suite_key, a.suite_name, a.status, a.created_at 
                    ORDER BY a.created_at DESC
                """
            )
            result = await session.execute(query)
            suites = result.mappings().all()
            print(f"dao层{suites}")
        return suites

    @staticmethod
    async def get_all_plans(suite_key: str, current_page:int, current_count: int):
        async with async_session() as session:
            result = await session.execute(
                select(StrTestPlan).where(
                    StrTestPlan.suite_key == suite_key
                ).order_by(desc(StrTestPlan.created_at)).offset((current_page -1) * current_count).limit(current_count)
            )
            plans = result.scalars().all()
            print(f"dao层{plans}")
        return plans

    @staticmethod
    async def get_all_plans_new(suite_key: str, current_page: int, current_count: int, plan_name:str):
        async with async_session() as session:
            subquery = select(StrTestPlan.id,
                       StrTestPlan.suite_key,
                       StrTestPlan.plan_key,
                       StrTestPlan.plan_name,
                       StrTestPlan.plan_task_sum,
                       func.count(StrTestCase.case_key).label('executed_case_num'),
                       func.sum(StrTestCase.case_status).label('failed_case_num'),
                       StrTestPlan.status,
                       StrTestPlan.created_at,
                       StrTestPlan.updated_at).join(
                    StrTestCase, and_(StrTestPlan.plan_key == StrTestCase.plan_key,StrTestPlan.suite_key == StrTestCase.suite_key), isouter=True
                ).where(
                    StrTestPlan.suite_key == suite_key
                )
            if not is_empty(plan_name):
                subquery = subquery.where(
                    StrTestPlan.plan_name.ilike(f'%{plan_name}%')
                )
            subquery = subquery.group_by(StrTestPlan.plan_key).order_by(desc(StrTestPlan.created_at)).offset((current_page - 1) * current_count).limit(current_count)
            result = await session.execute(
                subquery
            )
            plans = result.mappings().all()
            print(f"dao层{plans}")
        return plans

    @staticmethod
    async def get_all_plans_counts(suite_key: str, plan_name:str):
        async with async_session() as session:
            subquery = select(func.count(StrTestPlan.id)).where(StrTestPlan.suite_key == suite_key)
            if not is_empty(plan_name):
                subquery = subquery.where(
                    StrTestPlan.plan_name.ilike(f'%{plan_name}%')
                )
            result_count = await session.execute(subquery)
            total_count = result_count.one()
            print(f"dao层{total_count}")
        return total_count

    @staticmethod
    async def get_cases_statistic_performance_indicator(suite_key: str, plan_key: str):
        body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {"term": {"suite_key": suite_key}},
                        {"term": {"plan_key": plan_key}},
                        {"exists": {"field": "response_time"}}  # 只统计有响应时间的 step
                    ]
                }
            },
            "aggs": {
                "by_url": {
                    "terms": {
                        "field": "request_url",  # keyword 类型，精确分组
                        "size": 1000,  # 最多返回 1000 个不同接口，够用
                        "order": {"request_count": "desc"}
                    },
                    "aggs": {
                        "request_count": {"value_count": {"field": "response_time"}},
                        "response_time_stats": {"stats": {"field": "response_time"}},  # avg, min, max
                        "response_time_percentiles": {
                            "percentiles": {
                                "field": "response_time",
                                "percents": [50, 90, 95, 99]  # 中位数 = P50
                            }
                        }
                    }
                }
            }
        }

        try:
            resp = await es.search(index="str_test_case_step-*", body=body)  # 推荐改成别名 "str_test_case_step"

            buckets = resp["aggregations"]["by_url"]["buckets"]
            results = []

            for bucket in buckets:
                url = bucket["key"]
                stats = bucket["response_time_stats"]
                perc = bucket["response_time_percentiles"]["values"]

                results.append([
                    url,
                    bucket["request_count"]["value"],  # request_count
                    round(stats["avg"], 2) if stats["avg"] is not None else None,  # avg_response_time
                    round(stats["min"],2),  # min_response_time
                    round(stats["max"],2),  # max_response_time
                    round(perc.get("50.0") or perc.get("50"), 2) if perc.get("50.0") or perc.get("50") else None,
                    # median (P50)
                    round(perc.get("90.0") or perc.get("90"), 2) if perc.get("90.0") or perc.get("90") else None,
                    round(perc.get("95.0") or perc.get("95"), 2) if perc.get("95.0") or perc.get("95") else None,
                    round(perc.get("99.0") or perc.get("99"), 2) if perc.get("99.0") or perc.get("99") else None
                ])

            return results

        except Exception as e:
            print(f"ES get_cases_statistic_performance_indicator error: {e}")
            return []
        # async with async_session() as session:
        #     query = text(
        #         f"""
        #         WITH step_data AS (
        #             SELECT
        #                 request_url,
        #                 CAST(response_time AS DECIMAL(10,2)) AS rt,
        #                 PERCENT_RANK() OVER (PARTITION BY request_url ORDER BY CAST(response_time AS DECIMAL(10,2))) AS pr,
        #                 ROW_NUMBER() OVER (PARTITION BY request_url ORDER BY CAST(response_time AS DECIMAL(10,2))) AS rn,
        #                 COUNT(*) OVER (PARTITION BY request_url) AS total
        #             FROM str_test_case_step
        #             WHERE case_key IN (
        #                 SELECT case_key FROM str_test_case WHERE suite_key = '{suite_key}' AND plan_key = '{plan_key}'
        #             ) AND response_time IS NOT NULL
        #             ORDER by str_test_case_step.step_id
        #         ),
        #         stats_data AS (
        #             SELECT
        #                 request_url,
        #                 COUNT(*) AS request_count,
        #                 ROUND(AVG(rt), 2) AS avg_response_time,
        #                 MIN(rt) AS min_response_time,
        #                 MAX(rt) AS max_response_time
        #             FROM step_data
        #             GROUP BY request_url
        #         ),
        #         quantile_data AS (
        #             SELECT
        #                 request_url,
        #                 MIN(CASE WHEN pr >= 0.5 THEN rt END) AS median,
        #                 MIN(CASE WHEN pr >= 0.9 THEN rt END) AS p90_response_time,
        #                 MIN(CASE WHEN pr >= 0.95 THEN rt END) AS p95_response_time,
        #                 MIN(CASE WHEN pr >= 0.99 THEN rt END) AS p99_response_time
        #             FROM step_data
        #             GROUP BY request_url
        #         )
        #         SELECT
        #             s.*,
        #             q.median,
        #             q.p90_response_time,
        #             q.p95_response_time,
        #             q.p99_response_time
        #         FROM stats_data s
        #         JOIN quantile_data q ON s.request_url = q.request_url
        #         ORDER BY s.request_count DESC;
        #         """
        #     )
        #     result = await session.execute(query)
        #     cases_performance_indicator = result.all()
        #     print(f"dao层{cases_performance_indicator}")
        # return cases_performance_indicator


    @staticmethod
    async def get_cases_statistic_basic_indicator(suite_key: str, plan_key: str):
        async with async_session() as session:
            query = select(
                func.count(StrTestCase.case_key).label('total'),
                func.sum(
                    case((StrTestCase.case_status == 1, 1), else_=0)
                ).label('failed'),
                func.sum(
                    case((StrTestCase.case_status == 0, 1),else_=0)
                ).label('success'),
                func.round(func.sum(
                    case((StrTestCase.case_status == 0, 1), else_=0)
                ) / func.count(StrTestCase.case_key),2)
            ).where(
                and_(
                    StrTestCase.suite_key == suite_key,
                    StrTestCase.plan_key == plan_key
                )
            )
            result = await session.execute(query)
            cases_basic_indicator = result.all()
            print(f"dao层{cases_basic_indicator}")
        return cases_basic_indicator


    @staticmethod
    async def get_paginated_case_keys(
            suite_key: str,
            plan_key: str,
            current_page: int,
            current_count: int,
            path: str = None,
            s_time: float = None,
            e_time: float = None,
            fuzzy_search: str = None,
            case_status: str = None,  # "1" 或 "0" 或 None
    ) -> tuple[List[str], int]:
        must = [
            {"term": {"suite_key": suite_key}},
            {"term": {"plan_key": plan_key}}
        ]
        print(type(case_status))
        print(case_status)
        print('----')
        if not is_empty(path):
            must.append({"term": {"request_url": path}})

        if not is_empty(fuzzy_search):
            must.append({"match": {"real_response": str(fuzzy_search).strip()}})

        if (s_time and str(s_time).strip()) and (e_time and str(e_time).strip()):
            try:
                gte = float(str(s_time).strip())
                lte = float(str(e_time).strip())
                must.append({"range": {"response_time": {"gte": gte, "lte": lte}}})
            except (ValueError, TypeError):
                pass

        if case_status in ("1", "0"):
            script_source = """
                    String sign = "";
                    if (doc.containsKey('assert_res_sign.keyword') && doc['assert_res_sign.keyword'].size() > 0) {
                        sign = doc['assert_res_sign.keyword'].value;
                    }
                    boolean has_failure = (sign == '整体断言:失败');

                    if (params.status == '1') {
                        return has_failure;
                    } else {
                        return !has_failure;
                    }
                """
            must.append({
                "script": {
                    "script": {
                        "source": script_source,
                        "lang": "painless",
                        "params": {"status": case_status}
                    }
                }
            })

        body = {
            "query": {"bool": {"must": must}},
            "collapse": {
                "field": "case_key"  # 按 case_key 折叠，每组只返回一个文档
            },
            "sort": [
                {"case_key": "asc"},
                {"step_id": "asc"}
            ],
            "size": current_count,
            "from": (current_page - 1) * current_count,
            "aggs": {
                "total_cases": {
                    "cardinality": {"field": "case_key"}
                }
            }
        }

        resp = await es.search(index="str_test_case_step", body=body)

        case_keys = [hit["_source"]["case_key"] for hit in resp["hits"]["hits"]]
        total_count = resp["aggregations"]["total_cases"]["value"]
        return case_keys, total_count

    @staticmethod
    async def get_case_steps(suite_key: str, plan_key: str, case_keys: List[str]):
        detail_body = {
            "query": {
                "bool": {
                    "must": [
                        {"terms": {"case_key": case_keys}},
                        {"term": {"suite_key": suite_key}},
                        {"term": {"plan_key": plan_key}}
                    ]
                }
            },
            "sort": [{"case_key": "asc"}, {"step_id": "asc"}],
            "size": 10000  # 单个 case 的 step 数量上限，根据实际情况调整
        }
        detail_resp = await es.search(index="str_test_case_step", body=detail_body)
        return detail_resp

    @staticmethod
    async def get_case_datas(case_keys: List[str]):
        async with async_session() as session:
            case_map = {}
            if case_keys:
                result = await session.execute(
                    select(StrTestCase).where(StrTestCase.case_key.in_(case_keys))
                )
                for row in result.scalars():
                    case_map[row.case_key] = {
                        "suite_key": row.suite_key,
                        "plan_key": row.plan_key,
                        "case_key": row.case_key,
                        "remarks": row.remarks,
                        "created_at": row.created_at,
                        "updated_at": row.updated_at,
                    }
        return case_map

    @staticmethod
    async def get_case_path_select(suite_key: str, plan_key: str):
        """
        找到在这个用例下，可以选择的接口名称
        :param suite_key:
        :param plan_key:
        :return:
        """
        body = {
            "size": 0,  # 不需要返回文档，只需要聚合结果
            "query": {
                "bool": {
                    "must": [
                        {"term": {"suite_key": suite_key}},
                        {"term": {"plan_key": plan_key}}
                    ]
                }
            },
            "aggs": {
                "unique_urls": {
                    "terms": {
                        "field": "request_url",  # keyword 类型，精确去重
                        "size": 100,
                        "order": {"_key": "asc"}  # 按路径字母顺序排序，体验更好
                    }
                }
            }
        }
        try:
            resp = await es.search(
                index="str_test_case_step-*",  # 注意使用通配符
                body=body
            )
            buckets = resp["aggregations"]["unique_urls"]["buckets"]
            urls = [bucket["key"] for bucket in buckets]
            return urls
        except Exception as e:
            print(f"ES get_distinct_request_urls error: {e}")
            return []


    @staticmethod
    async def edit_case(suite_key: str, plan_key: str, case_key: str, remarks: str):
        try:
            async with async_session() as session:
                await session.execute(
                    update(StrTestCase).where(and_(
                        StrTestCase.suite_key == suite_key,
                        StrTestCase.plan_key == plan_key,
                        StrTestCase.case_key == case_key
                    )).values(
                        remarks = remarks
                    )
                )
                await session.commit()
            return {"msg": "更新成功"}
        except Exception as e:
            return {"msg": "更新失败"}

    @staticmethod
    async def monitor_report(start_time: int, end_time: int):
        index_name = "str_monitor"
        query_body = {
            "size": 5000,
            "sort": [{"created_at": "asc"}],
            "query": {"bool": {"filter": [
                {
                    "range": {"created_at": {"gt": start_time}}
                },
                {
                    "range": {"created_at": {"lt": end_time}}
                }
            ]}}
        }
        resp = await es.search(
            index=index_name,  # 注意使用通配符
            body=query_body
        )
        records = [hit["_source"] for hit in resp["hits"]["hits"]]
        return records


    @staticmethod
    async def submit_zentao(suite_key: str, plan_key: str):
        return {}
        # try:
        #     async with async_session() as session:
        #         quary = select(
        #             StrTestPlan.plan_name,
        #             StrTestCase.case_key,
        #             StrTestCase.case_status,
        #             StrTestCaseStep.step_id,
        #             StrTestCaseStep.step_name,
        #             StrTestCaseStep.user_variables,
        #             StrTestCaseStep.request_url,
        #             StrTestCaseStep.request_param,
        #             StrTestCaseStep.real_response,
        #             StrTestCaseStep.assert_res_details
        #         ).join(
        #             StrTestCase, and_(
        #                 StrTestPlan.suite_key == StrTestCase.suite_key,
        #                 StrTestPlan.plan_key == StrTestCase.plan_key
        #             )
        #         ).join(
        #             StrTestCaseStep, StrTestCase.case_key == StrTestCaseStep.case_key # type: ignore
        #         ).where(
        #             and_(
        #                 StrTestPlan.suite_key == suite_key,
        #                 StrTestPlan.plan_key == plan_key,
        #                 StrTestCase.case_status == 1,
        #                 StrTestCaseStep.assert_res_sign == '整体断言:失败'
        #             )
        #         ).order_by(StrTestCase.case_key)
        #         result = await session.execute(quary)
        #         res_data = result.mappings().all()
        #     return res_data
        # except Exception as e:
        #     return {"msg": "查找失败"}

    # @staticmethod
    # async def get_endtime(suite_key: str):
    #     async with async_session() as session:
    #         query = select(StrTestSuite.updated_at).where(StrTestSuite.suite_key == suite_key)
    #         result = await session.execute(query)
    #     return result.scalars().one()
    #
    # @staticmethod
    # async def get_cases(suite_key:str ,base_time: int, first_time: int, last_time:int, mtype:str, end_time:int):
    #     async with async_session() as session:
    #         query = select(StrTestCase).where(StrTestCase.suite_key == suite_key)
    #         if mtype == "init":
    #             # base_dt = datetime.strptime(base_time, "%Y-%m-%d %H:%M:%S")
    #             query = query.where(and_(
    #                 StrTestCase.created_at > base_time,
    #                 StrTestCase.created_at < end_time
    #             ))
    #         elif mtype == "prev":
    #             # first_dt = datetime.strptime(first_time, "%Y-%m-%d %H:%M:%S")
    #             query = query.where(and_(
    #                 StrTestCase.created_at < first_time,
    #                 StrTestCase.created_at > end_time,
    #             ))
    #         else:
    #             # last_dt = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
    #             query = query.where(and_(
    #                 StrTestCase.created_at > last_time,
    #                 StrTestCase.created_at < end_time,
    #             ))
    #         # query = query.where(StrTestCase.created_at < datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    #         query = query.order_by(StrTestCase.created_at)
    #         query = query.limit(1000)
    #         result = await session.execute(query)
    #     return result.scalars().all()
    #
    #
    # @staticmethod
    # async def get_monitor_info(base_time: int, first_time: int, last_time:int, mtype:str, end_time:int):
    #     index_name = "str_monitor"
    #     query_body = {
    #         "size": 1000,
    #         "sort": [{"created_at": "asc"}],
    #         "query": {"bool": {"filter": []}}
    #     }
    #     # 1 初始加载
    #     if mtype == "init":
    #         query_body["query"]["bool"]["filter"].append({
    #             "range": {"created_at": {"gt": base_time}}
    #         })
    #         query_body["query"]["bool"]["filter"].append({
    #             "range": {"created_at": {"lt": end_time}}
    #         })
    #
    #     # 2 向上滚
    #     elif mtype == "prev":
    #         query_body["query"]["bool"]["filter"].append({
    #             "range": {"created_at": {"lt": first_time}}
    #         })
    #         query_body["query"]["bool"]["filter"].append({
    #             "range": {"created_at": {"gt": base_time}}
    #         })
    #     # 3 向下滚
    #     elif mtype == "next":
    #         query_body["query"]["bool"]["filter"].append({
    #             "range": {"created_at": {"gt": last_time}}
    #         })
    #         query_body["query"]["bool"]["filter"].append({
    #             "range": {"created_at": {"lt": end_time}}
    #         })
    #     resp = await es.search(
    #         index=index_name,
    #         body=query_body
    #     )
    #     records = [hit["_source"] for hit in resp["hits"]["hits"]]
    #     return records
