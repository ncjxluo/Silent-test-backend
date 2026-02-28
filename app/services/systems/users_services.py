# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 14:42
# @Author  : lwc
# @File    : users.py
# @Description :

from app.dao.systems.users_dao import UsersDao
import uuid

class UserService:

    @staticmethod
    async def get_all_users(user_key: str, current_page: int, current_count: int):
        users = await UsersDao.get_users(user_key, current_page, current_count)
        print(f"用户是{users}")
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