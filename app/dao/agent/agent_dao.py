# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 16:47
# @Author  : lwc
# @File    : time_job_dao.py
# @Description : 相关定时任务的dao


from app.core.db import async_session
from app.models.str_api_node import StrApiAgent
from sqlmodel import select,func,and_
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
from typing import List

class AgentDao:

    @staticmethod
    async def get_api_agent():
        async with async_session() as session:
            result = await session.execute(select(StrApiAgent))
            agents = result.scalars().all()
        return agents

    @staticmethod
    async def get_api_agent_paging(current_page, current_count):
        async with async_session() as session:
            query = (
                select(StrApiAgent).offset((current_page -1) * current_count).limit(current_count)
            )
            result = await session.execute(query)
            agents = result.scalars().all()
        return agents

    @staticmethod
    async def get_api_agent_count():
        async with async_session() as session:
            query = (
                select(func.count(StrApiAgent.agent_key))
            )
            result = await session.execute(query)
            result_count = result.one()
        return result_count

    @staticmethod
    async def set_api_agent_status(agent_key: str, status: int) -> None:
        async with async_session() as session:
            result = await session.execute(select(StrApiAgent).where(StrApiAgent.agent_key == agent_key))
            agent: StrApiAgent = result.scalars().one()
            agent.agent_status = status
            session.add(agent)
            await session.commit()

    @staticmethod
    async def merge_api_agent(agent_key: str, agent_name: str, status: int,
                               agent_running_tasks:str, agent_max_tasks:str, agent_cpu:str,
                               agent_memory:str, agent_io:str):
        async with async_session() as session:
            api_env = StrApiAgent(
                agent_key=agent_key,
                agent_name=agent_name,
                agent_status=status,
                agent_running_tasks=agent_running_tasks,
                agent_max_tasks=agent_max_tasks,
                agent_cpu=agent_cpu,
                agent_memory=agent_memory,
                agent_io=agent_io,
            )
            await session.merge(api_env)
            await session.commit()


    @staticmethod
    async def get_task(agent_id:str):
        async with async_session() as session:
            query = (
                select(StrTestSuite.suite_key,StrTestPlan.plan_key,
                       StrTestPlan.plan_name,
                       StrTestPlan.case_content,StrTestPlan.doc_content)
                .join(StrTestPlan, StrTestSuite.suite_key == StrTestPlan.suite_key).where(
                    and_(
                        StrTestSuite.suite_agent_key == agent_id,
                        StrTestSuite.status == 'ready'
                    )
                )
            )
            result = await session.execute(query)
            tasks = result.mappings().all()
        return tasks