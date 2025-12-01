# -*- coding: utf-8 -*-
# @Time    : 2025/11/4 18:14
# @Author  : lwc
# @File    : auth_service.py
# @Description : 认证功能相关的服务层代码


from app.dao.user_dao import UserDao

class UserServices:

    @staticmethod
    async def check_auth(username:str, password:str):
        return await UserDao.login(username, password)



