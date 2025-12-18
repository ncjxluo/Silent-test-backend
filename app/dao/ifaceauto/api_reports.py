# -*- coding: utf-8 -*-
# @Time    : 2025/11/11 14:23
# @Author  : lwc
# @File    : api_reports.py
# @Description : 定义获取接口自动化测试报告的数据访问方法
from annotated_types.test_cases import cases

from app.core.db import async_session
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
from app.models.str_test_case import StrTestCase
from app.models.str_test_case_step import StrTestCaseStep
from sqlmodel import select, and_, desc, func, text, distinct, cast, DECIMAL, case, update
from app.utils.my_util import is_empty


class ApiReportsDao:

    @staticmethod
    async def get_all_suites():
        async with async_session() as session:
            result = await session.execute(
                select(StrTestSuite).where(
                    StrTestSuite.type == "api"
                ).order_by(desc(StrTestSuite.created_at))
            )
            suites = result.scalars().all()
            print(f"dao层{suites}")
        return suites

    @staticmethod
    async def get_all_suites_new():
        async with async_session() as session:
            query = text(
                f"""
                SELECT
                  a.suite_key,
                  a.suite_name,
                  a.status,
                  a.created_at,
                  ROUND(sum(case when b.status = 'finish' then 1 else 0 end) / COUNT(b.plan_key),2) as progress
                FROM
                  `str_test_suite` as a 
                LEFT JOIN 
                  str_test_plan as b on a.suite_key = b.suite_key
                where a.type = 'api'
                group by a.suite_key,a.suite_name,a.status,a.created_at  ORDER BY a.created_at DESC 
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
    async def get_all_plans_new(suite_key: str, current_page: int, current_count: int):
        async with async_session() as session:
            result = await session.execute(
                select(StrTestPlan.id,
                       StrTestPlan.suite_key,
                       StrTestPlan.plan_key,
                       StrTestPlan.plan_name,
                       StrTestPlan.plan_task_sum,
                       func.sum(StrTestCase.case_status).label('failed_case_num'),
                       StrTestPlan.status,
                       StrTestPlan.created_at,
                       StrTestPlan.updated_at)
                .join(
                    StrTestCase, and_(StrTestPlan.plan_key == StrTestCase.plan_key,StrTestPlan.suite_key == StrTestCase.suite_key)
                )
                .where(
                    StrTestPlan.suite_key == suite_key
                ).group_by(StrTestPlan.plan_key).order_by(desc(StrTestPlan.created_at)).offset((current_page - 1) * current_count).limit(current_count)
            )
            plans = result.mappings().all()
            print(f"dao层{plans}")
        return plans

    @staticmethod
    async def get_all_plans_counts(suite_key: str):
        async with async_session() as session:
            result_count = await session.execute(
                select(func.count(StrTestPlan.id)).where(StrTestPlan.suite_key == suite_key))
            total_count = result_count.one()
            print(f"dao层{total_count}")
        return total_count

    @staticmethod
    async def get_cases_statistic_performance_indicator(suite_key: str, plan_key: str):
        # async with async_session() as session:
        #     query = text(
        #         f"""
        #         SELECT
        #             request_url,
        #             COUNT(*) AS request_count,
        #             ROUND(AVG(CAST(response_time as DECIMAL(10,2))),2) as avg_response_time,
        #             MIN(CAST(response_time as DECIMAL(10,2))) as min_response_time,
        #             MAX(CAST(response_time as DECIMAL(10,2))) as max_response_time,
        #             SUBSTRING_INDEX(SUBSTRING_INDEX(GROUP_CONCAT(CAST(response_time as DECIMAL(10,2)) ORDER BY CAST(response_time as DECIMAL(10,2))), ',',
        #                            FLOOR(COUNT(*) * 0.5) + 1), ',', -1) AS median,
        #             SUBSTRING_INDEX(SUBSTRING_INDEX(GROUP_CONCAT(CAST(response_time as DECIMAL(10,2)) ORDER BY CAST(response_time as DECIMAL(10,2))), ',',
        #                            FLOOR(COUNT(*) * 0.9) + 1), ',', -1) AS p90_response_time
        #         FROM str_test_case
        #         WHERE response_time IS NOT NULL and suite_key = '{suite_key}' and plan_key = '{plan_key}'
        #         GROUP BY request_url order by step_id ;
        #         """
        #     )
        #     result = await session.execute(query)
        #     cases_performance_indicator = result.all()
        #     print(f"dao层{cases_performance_indicator}")
        # return cases_performance_indicator
        async with async_session() as session:
            query = text(
                f"""
                WITH step_data AS (
                    SELECT
                        request_url,
                        CAST(response_time AS DECIMAL(10,2)) AS rt,
                        PERCENT_RANK() OVER (PARTITION BY request_url ORDER BY CAST(response_time AS DECIMAL(10,2))) AS pr,
                        ROW_NUMBER() OVER (PARTITION BY request_url ORDER BY CAST(response_time AS DECIMAL(10,2))) AS rn,
                        COUNT(*) OVER (PARTITION BY request_url) AS total
                    FROM str_test_case_step 
                    WHERE case_key IN (
                        SELECT case_key FROM str_test_case WHERE suite_key = '{suite_key}' AND plan_key = '{plan_key}'
                    ) AND response_time IS NOT NULL
                    ORDER by str_test_case_step.step_id 
                ),
                stats_data AS (
                    SELECT
                        request_url,
                        COUNT(*) AS request_count,
                        ROUND(AVG(rt), 2) AS avg_response_time,
                        MIN(rt) AS min_response_time,
                        MAX(rt) AS max_response_time
                    FROM step_data
                    GROUP BY request_url
                ),
                quantile_data AS (
                    SELECT
                        request_url,
                        MIN(CASE WHEN pr >= 0.5 THEN rt END) AS median,
                        MIN(CASE WHEN pr >= 0.9 THEN rt END) AS p90_response_time,
                        MIN(CASE WHEN pr >= 0.95 THEN rt END) AS p95_response_time,
                        MIN(CASE WHEN pr >= 0.99 THEN rt END) AS p99_response_time
                    FROM step_data
                    GROUP BY request_url
                )
                SELECT
                    s.*,
                    q.median,
                    q.p90_response_time,
                    q.p95_response_time,
                    q.p99_response_time
                FROM stats_data s
                JOIN quantile_data q ON s.request_url = q.request_url
                ORDER BY s.request_count DESC;
                """
            )
            result = await session.execute(query)
            cases_performance_indicator = result.all()
            print(f"dao层{cases_performance_indicator}")
        return cases_performance_indicator


    @staticmethod
    async def get_cases_statistic_basic_indicator(suite_key: str, plan_key: str):
        async with async_session() as session:
            # query = text(
            #     f"""
            #         SELECT
            #             COUNT(DISTINCT case_key) as total_cases,
            #             COUNT(DISTINCT CASE WHEN LOCATE('失败', assert_res_sign) > 0 THEN case_key END) as fail_cases,
            #             COUNT(DISTINCT case_key) - COUNT(DISTINCT CASE WHEN LOCATE('失败', assert_res_sign) > 0 THEN case_key END) as success_cases,
            #             ROUND(
            #                 (COUNT(DISTINCT case_key) - COUNT(DISTINCT CASE WHEN LOCATE('失败', assert_res_sign) > 0 THEN case_key END)) * 100.0 /
            #                 COUNT(DISTINCT case_key),
            #                 2
            #             ) as pass_rate_percent
            #         FROM str_test_case where suite_key = '{suite_key}' and plan_key = '{plan_key}'
            #         """
            # )
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
    async def get_case_datas(suite_key: str, plan_key: str, current_page:int, current_count: int, path:str = None, status:str = None, s_time:str = None, e_time:str = None):
        async with async_session() as session:
            # case_group = StrTestCase.__table__.alias(name="case_group")
            # case_child = StrTestCase.__table__.alias(name="case_child")
            # subquery = select(distinct(case_group.c.case_key).label('case_key')).where(
            #     and_(
            #         case_group.c.suite_key == suite_key,
            #         case_group.c.plan_key == plan_key
            #     )
            # )
            # if not is_empty(status):
            #     subquery = subquery.where(
            #         func.LOCATE(status, case_group.c.assert_res_sign) > 0
            #     )
            #
            # if not is_empty(s_time) and not is_empty(e_time) and not is_empty(path):
            #     time_child_query = select(distinct(case_group.c.case_key)).where(and_(
            #         cast(case_group.c.response_time, DECIMAL(10, 2)).between(s_time, e_time),
            #         case_group.c.suite_key == suite_key,
            #         case_group.c.plan_key == plan_key
            #     ))
            #     time_child_query = time_child_query.where(
            #         case_group.c.request_url == path
            #     )
            #     subquery = subquery.where(case_group.c.case_key.in_(time_child_query))
            # elif not is_empty(s_time) and not is_empty(e_time):
            #     time_child_query = select(distinct(case_group.c.case_key)).where(and_(
            #         cast(case_group.c.response_time, DECIMAL(10, 2)).between(s_time, e_time),
            #         case_group.c.suite_key == suite_key,
            #         case_group.c.plan_key == plan_key
            #     ))
            #     subquery = subquery.where(case_group.c.case_key.in_(time_child_query))
            # # LOCATE
            # subquery = subquery.offset((current_page -1) * current_count).limit(current_count).alias("t1")
            # query = (
            #     select(case_child)
            #     .join(subquery, subquery.c.case_key == case_child.c.case_key)# type: ignore
            #     .order_by(case_child.c.case_key,case_child.c.step_id,case_child.c.id)
            # )

            case_main = StrTestCase.__table__.alias(name="case_main")
            case_step = StrTestCaseStep.__table__.alias(name="case_step")

            subquery = select(distinct(case_main.c.case_key).label('case_key')).where(
                and_(
                    case_main.c.suite_key == suite_key,
                    case_main.c.plan_key == plan_key
                )
            )
            if not is_empty(status):
                subquery = subquery.where(
                    case_main.c.case_status == int(status)
                )

            if not is_empty(s_time) and not is_empty(e_time):
                time_child_query = select(distinct(case_step.c.case_key)).where(and_(
                    cast(case_step.c.response_time, DECIMAL(10, 2)).between(s_time, e_time)
                ))
                if not is_empty(path):
                    time_child_query = time_child_query.where(
                        case_step.c.request_url == path
                    )
                subquery = subquery.where(case_main.c.case_key.in_(time_child_query))
            # LOCATE
            subquery = subquery.offset((current_page -1) * current_count).limit(current_count).alias("t1")
            query = (
                select(case_main.c.suite_key,case_main.c.plan_key,case_main.c.case_key,case_main.c.case_status, # type: ignore
                       case_step.c.step_id,case_step.c.step_name,case_step.c.user_variables,case_step.c.request_url,
                       case_step.c.request_param,case_step.c.real_response,case_step.c.response_time,case_step.c.assert_res_sign,
                       case_step.c.assert_res_details,case_step.c.assert_ver_sign,case_step.c.assert_time_sign,
                       case_main.c.remarks,case_main.c.created_at,case_main.c.updated_at)
                .join(subquery, subquery.c.case_key == case_main.c.case_key) # type: ignore
                .join(case_step, case_step.c.case_key == subquery.c.case_key)  # type: ignore
                .order_by(case_main.c.case_key,case_step.c.step_id)
            )

            result = await session.execute(query)
            case_datas = result.mappings().all()
            print("case_datas")
            print(case_datas)
        return case_datas


    @staticmethod
    async def get_case_key_count(suite_key: str, plan_key: str, path:str = None, status:str = None, s_time:str = None, e_time:str = None):
        async with async_session() as session:
            query = select(func.count(distinct(StrTestCase.case_key))).join(
                StrTestCaseStep, StrTestCase.case_key == StrTestCaseStep.case_key
            ).where(
                and_(
                    StrTestCase.suite_key == suite_key,
                    StrTestCase.plan_key == plan_key
                )
            )
            if not is_empty(status):
                query = query.where(
                    StrTestCase.case_status == int(status)
                )
            if not is_empty(s_time) and not is_empty(e_time):
                query = query.where(
                    cast(StrTestCaseStep.response_time, DECIMAL(10, 2)).between(s_time, e_time)
                )
            if not is_empty(path):
                query = query.where(
                    StrTestCaseStep.request_url == path
                )
            result_count = await session.execute(query)
            cases_group_count =  result_count.one()
        return cases_group_count

    @staticmethod
    async def get_case_path_select(suite_key: str, plan_key: str):
        """
        找到在这个用例下，可以选择的接口名称
        :param suite_key:
        :param plan_key:
        :return:
        """
        async with async_session() as session:
            subquery = select(StrTestCase.case_key).where(
                        and_(
                            StrTestCase.suite_key == suite_key,
                            StrTestCase.plan_key == plan_key
                        )
                ).limit(1).alias("t1")

            query = select(distinct(StrTestCaseStep.request_url)).join(
                subquery, StrTestCaseStep.case_key == subquery.c.case_key
            )
            result = await session.execute(query)
            path_select = result.scalars().all()
        return path_select


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
