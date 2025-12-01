# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 17:53
# @Author  : lwc
# @File    : agent_service.py
# @Description : agent相关的service方法

from app.dao.agent.agent_dao import AgentDao

class AgentService:

    @staticmethod
    async def get_all_api_agent(current_page:int = 1, current_count:int = 30) -> dict:
        agents = await AgentDao.get_api_agent_paging(current_page, current_count)
        total_count = await AgentDao.get_api_agent_count()
        return {"total_count": total_count[0], "agents": agents}
