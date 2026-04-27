# -*- coding: utf-8 -*-
# @Time    : 2026/3/16 11:47
# @Author  : lwc
# @File    : str_operation_decorator.py
# @Description : 记录操作日志的装饰器

import functools
import asyncio
from typing import Optional, Callable
from app.dao.systems.str_log_dao import StrLogDao


def log_operation(module: str = "", operation: str = "", content: str = ""):
    """
    统一记录接口操作日志的装饰器
    :param module: 模块
    :param operation: 操作类型
    :param content: 内容
    :return:
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        # wraps 可以保留入口函数的信息
        async def wrapper(*args, **kwargs):
            current_user_key = kwargs.get("current_user_key", '未知')
            request_body = {}
            for key, value in kwargs.items():
                if hasattr(value, "dict"):
                    request_body = value.dict()
                    break
            if current_user_key == '未知':
                current_user_key = request_body.get("username")
            try:
                result = await func(*args, **kwargs)
                msg = "操作成功"
            except Exception as e:
                result = {"code": 500, "msg": str(e)}
                msg = f"操作失败：{str(e)}"
            asyncio.create_task(StrLogDao.record_operation_log(
                current_user_key, operation, module, content, "", msg
            ))
            return result
        return wrapper
    return decorator