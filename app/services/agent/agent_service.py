# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 17:53
# @Author  : lwc
# @File    : agent_service.py
# @Description : agent相关的service方法

from app.dao.agent.agent_dao import AgentDao
from app.dao.ifaceauto.api_reports import ApiReportsDao
from typing import List

class AgentService:

    @staticmethod
    async def get_all_api_agent(current_page:int = 1, current_count:int = 30) -> dict:
        agents = await AgentDao.get_api_agent_paging(current_page, current_count)
        total_count = await AgentDao.get_api_agent_count()
        return {"total_count": total_count[0], "agents": agents}

    @staticmethod
    async def merge_api_agent(agent_key: str, agent_name: str, status: int,
                               agent_running_tasks:str, agent_max_tasks:str, agent_cpu:str,
                               agent_memory:str, agent_io:str):

        await AgentDao.merge_api_agent(agent_key, agent_name, status,
                            agent_running_tasks, agent_max_tasks, agent_cpu, agent_memory, agent_io)

    @staticmethod
    async def get_tasks(agent_id:str) -> dict:
        tasks = await AgentDao.get_task(agent_id)
        for task in tasks:
            await ApiReportsDao.set_suite_status(task.suite_key, "running")
        return tasks