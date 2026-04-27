# -*- coding: utf-8 -*-
# @Time    : 2026/3/16 14:39
# @Author  : lwc
# @File    : deploy_task_dao.py
# @Description :

from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from app.utils.my_util import is_empty

class DeployTaskDao:

    @staticmethod
    async def test() -> dict:

        return {"msg": "新增失败"}