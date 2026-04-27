# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 16:47
# @Author  : lwc
# @File    : time_job_service.py
# @Description : 相关定时任务的service

from datetime import datetime
from app.dao.agent.agent_dao import AgentDao

class TimeJobServices:

    @staticmethod
    async def set_api_status(heartbeat_timeout:int) -> None:
        agents = await AgentDao.get_api_agent()
        print(f"agents参数{agents}")
        now = datetime.now()
        for agent in agents:
            print(f"agent参数{agent}")
            if agent.updated_at and (now - agent.updated_at).total_seconds() > heartbeat_timeout:
                print(f"agent_key:{agent.agent_key}已经超过{heartbeat_timeout}秒没有更新了")
                if agent.agent_status != 0:
                    await AgentDao.set_api_agent_status(agent.agent_key, 0)