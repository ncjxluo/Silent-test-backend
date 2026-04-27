# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 10:16
# @Author  : lwc
# @File    : sys_services.py
# @Description : 系统的业务操作

from app.dao.systems.sys_dao import SysDao
import uuid
from datetime import datetime

class SysService:

    @staticmethod
    async def user_heartbeat(user_key: str):
        res = await SysDao.update_hearbeat_time(user_key, datetime.now())
        return res