# -*- coding: utf-8 -*-
# @Time    : 2025/11/19 16:44
# @Author  : lwc
# @File    : time_job.py
# @Description : 存放一些定时任务的模块

from app.services.time_job_service import TimeJobServices
import asyncio

async  def api_agent_watchdog():
    """
    这个函数用来定时监控agent是否存活，从而将其变更为失联。并且它需要跟随backend作为伴生任务启动
    :return:
    """
    check_interval = 200
    heartbeat_timeout = 15
    while True:
        await TimeJobServices.set_api_status(heartbeat_timeout)
        await asyncio.sleep(check_interval)


