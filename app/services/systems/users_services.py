# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:42
# @Author  : lwc
# @File    : users.py
# @Description :

from app.dao.systems.users_dao import UsersDao
from datetime import datetime, timedelta
import uuid

class UserService:

    @staticmethod
    async def get_all_users(user_key: str, current_page: int, current_count: int, i_type:int):
        users = await UsersDao.get_users(user_key, current_page, current_count, i_type)
        total_count = await UsersDao.get_users_count(user_key)
        return {"total_count": total_count[0], "users": users}

    @staticmethod
    async def addition_user(username: str, nickname: str, email:str, phone:str, status: int, dept_key:str, role_key:str):
        user_key = str(uuid.uuid4())
        res = await UsersDao.addition_user(user_key, username, nickname, email, phone, status, dept_key, role_key)
        return res

    @staticmethod
    async def del_user(user_key: str):
        res = await UsersDao.del_user(user_key)
        return res

    @staticmethod
    async def get_user_statistic(online_time_difference: int = 30):
        threshold_time = datetime.now() - timedelta(seconds=online_time_difference)
        print(f"时间差{threshold_time}")
        total_count, online_count = await UsersDao.get_users_statistic_count(threshold_time)
        return {"total_count": total_count[0], "online_count": online_count[0]}