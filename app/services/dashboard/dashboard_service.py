# -*- coding: utf-8 -*-
# @Time    : 2026/2/28 16:15
# @Author  : lwc
# @File    : dashboard_service.py
# @Description : 仪表盘中的业务逻辑

from app.dao.systems.manage_dao import ManageDao

class DashboardService:

    @staticmethod
    async def get_notice() -> dict:
        data = await ManageDao.get_notice()
        return data

    @staticmethod
    async def get_memos(user_key:str, current_page:int, current_count:int) -> dict:
        memos = await ManageDao.get_memos(user_key, current_page, current_count)
        total_count = await ManageDao.get_memos_count(user_key)
        return {"total_count": total_count[0], "memos": memos}

    @staticmethod
    async def add_memo(user_key:str, memo_title:str, memo_content:str, memo_level:str, memo_complete:str) -> dict:
        data = await ManageDao.add_memo(user_key, memo_title, memo_content, memo_level, memo_complete)
        return data

    @staticmethod
    async def del_memo(memo_key:str) -> dict:
        data = await ManageDao.del_memo(memo_key)
        return data

    @staticmethod
    async def edit_memo(memo_key:str, memo_complete:str) -> dict:
        data = await ManageDao.edit_memo(memo_key, memo_complete)
        return data