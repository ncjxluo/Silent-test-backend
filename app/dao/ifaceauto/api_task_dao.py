# -*- coding: utf-8 -*-
# @Time    : 2026/4/6 17:50
# @Author  : lwc
# @File    : api_task_dao.py
# @Description :

import uuid

from sqlalchemy.sql.functions import count
from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from typing import List
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
from app.utils.my_util import is_empty


class ApiTaskDao:

    @staticmethod
    async def assign_temp_task(suite_key:str, suite_name:str, suite_agent_key:str,
                               status:str, task_type:str, plan_key:str, case_name:str,
                               case_content:str, doc_content:str, current_user_key:str) -> dict:
        try:
            async with async_session() as session:
                api_task = StrTestSuite(
                    user_key = current_user_key,
                    suite_key=suite_key,
                    suite_name=suite_name,
                    suite_agent_key=suite_agent_key,
                    status=status,
                    type=task_type
                )
                api_plan = StrTestPlan(
                    suite_key=suite_key,
                    plan_key=plan_key,
                    plan_name=case_name,
                    case_content=case_content,
                    doc_content=doc_content,
                    status=status
                )
                session.add(api_task)
                session.add(api_plan)
                await session.commit()
            return {"msg": "任务下发成功"}
        except Exception as e:
            print(e)
            return {"msg": "任务下发失败"}


    @staticmethod
    async def assign_tasks(api_suite:StrTestSuite, api_plans:List[StrTestPlan]) -> dict:
        try:
            async with async_session() as session:
                session.add(api_suite)
                session.add_all(api_plans)
                await session.commit()
            return {"msg": "任务下发成功"}
        except Exception as e:
            print(f'错误{e}')
            return {"msg": "任务下发失败"}