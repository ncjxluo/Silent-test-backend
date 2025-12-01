# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 16:47
# @Author  : lwc
# @File    : time_job_dao.py
# @Description : 相关定时任务的dao


from app.core.db import async_session
from app.models.str_api_node import StrApiAgent
from sqlmodel import select,func

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
                select(func.count(StrApiAgent.id))
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