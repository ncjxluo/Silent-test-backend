# -*- coding: utf-8 -*-
# @Time    : 2026/3/9 17:22
# @Author  : lwc
# @File    : task_center_services.py
# @Description :
from app.dao.message_center.message_dao import MessageDao
from app.dao.test_resource.task_center_dao import TaskCenterDao
import uuid
from typing import List
from itertools import groupby

from app.utils.my_util import is_empty
from app.utils.send_message import send_mes

class TaskCenterService:

    @staticmethod
    async def add_kanban_temp(board_name:str, kanban_columns:List, board_description:str) -> dict:

        board_key = str(uuid.uuid4())
        for item in kanban_columns:
            item["column_key"] = str(uuid.uuid4())
        data = await TaskCenterDao.add_kanban_temp(board_key, board_name, kanban_columns, board_description)
        return data

    @staticmethod
    async def get_kanban_temp(k_name:str, current_page:int, current_count:int) -> dict:
        data = await TaskCenterDao.get_kanban_temp(k_name, current_page, current_count)
        grouped = groupby(data, key=lambda x: x["board_key"])
        result_list = []
        for board_key, group in grouped:
            dic1 = dict()
            dic1["board_key"] = board_key
            c_count = 0
            c_lis = list()
            for item1 in group:
                dic1["board_name"] = item1.board_name
                dic1["board_description"] = item1.board_description
                c_count = c_count + 1
                c_lis.append(item1)
            dic1["kanban_columns"] = str(c_count)
            dic1["child_item"] = c_lis
            result_list.append(dic1)
        total_count = await TaskCenterDao.get_kanban_temp_count(k_name)
        return {"total_count": total_count[0], "kanbans": result_list}

    @staticmethod
    async def edit_kanban_temp(board_key:str, board_name:str, kanban_columns:List, board_description:str) -> dict:

        data = await TaskCenterDao.edit_kanban_temp(board_key, board_name, kanban_columns, board_description)
        return data

    @staticmethod
    async def del_kanban_temp(board_key:str) -> dict:
        data = await TaskCenterDao.del_kanban_temp(board_key)
        return data

    @staticmethod
    async def del_kanban_column(column_key:str) -> dict:
        data = await TaskCenterDao.del_kanban_column(column_key)
        return data

    @staticmethod
    async def add_task(task_name: str, task_num: int, version_num: str, release_time: str,
                       is_complete:str, board_key:str, task_details: List) -> dict:
        first_place = await TaskCenterDao.get_kanban_position_column_key(board_key, '1')
        first_column_key = first_place[0]
        task_key = str(uuid.uuid4())
        for item in task_details:
            item["task_details_key"] = str(uuid.uuid4())
            item["board_key"] = board_key
            item["column_key"] = first_column_key
        data = await TaskCenterDao.add_task(
            task_key, task_name, task_num, version_num, release_time, is_complete, task_details
        )
        return data

    @staticmethod
    async def send_task_message(message_info: dict):
        if is_empty(message_info.get("message_content")):
            return
        message_channel = await MessageDao.get_message(message_info.get("message_key"))
        await send_mes(message_channel[0].mes_url, message_info.get('message_content'))

    @staticmethod
    async def edit_task(task_key: str,task_name: str, task_num: int, version_num: str, release_time: str, board_key:str, task_details: List) -> dict:
        first_place = await TaskCenterDao.get_kanban_position_column_key(board_key, '1')
        first_column_key = first_place[0]
        data = await TaskCenterDao.edit_task(task_key, task_name, task_num, version_num, release_time, board_key, first_column_key, task_details)
        return data

    @staticmethod
    async def del_task(task_key:str) -> dict:
        data = await TaskCenterDao.del_task(task_key)
        return data

    @staticmethod
    async def del_task_details(task_details_key:str) -> dict:
        data = await TaskCenterDao.del_task_details(task_details_key)
        return data


    @staticmethod
    async def get_tasks(task_label_name:str, task_condition:str, current_page: int, current_count: int) -> dict:
        data = await TaskCenterDao.get_tasks(task_label_name, task_condition, current_page, current_count)
        grouped = groupby(data, key=lambda x: x["task_key"])
        result_list = []
        for board_key, group in grouped:
            dic1 = dict()
            dic1["task_key"] = board_key
            c_lis = list()
            for item in group:
                dic1["task_name"] = item.get("task_name")
                dic1["task_num"] = item.get("task_num")
                dic1["board_key"] = item.get("board_key")
                dic1["version_num"] = item.get("version_num")
                dic1["release_time"] = item.get("release_time")
                dic1["is_complete"] = item.get("is_complete")
                c_lis.append(item)
            dic1["child_item"] = c_lis
            result_list.append(dic1)
        total_count = await TaskCenterDao.get_tasks_count(task_label_name, task_condition)
        return {"total_count": total_count[0], "tasks": result_list}


    @staticmethod
    async def get_kanban_columns_tasks(k_switch:bool, task_key:str, board_key:str, condition:str, current_user_key: str) -> dict:
        data = await TaskCenterDao.get_kanban_columns_tasks(k_switch, task_key, board_key, condition, current_user_key)
        grouped = groupby(data, key=lambda x: x["column_key"])
        result_list = []
        for column_key, group in grouped:
            dic1 = dict()
            dic1["column_key"] = column_key
            c_lis = list()
            for item in group:
                dic1["board_key"] = item.get("board_key")
                dic1["column_name"] = item.get("column_name")
                dic1["sort_order"] = item.get("sort_order")
                dic1["column_status"] = item.get("column_status")
                c_lis.append(item)
            dic1["tasks"] = c_lis
            result_list.append(dic1)
        return {"tasks": result_list}

    @staticmethod
    async def edit_kanban_tasks(task_key: str, task_details_key: str, column_key: str, column_status: str) -> dict:
        res = 0
        data = await TaskCenterDao.edit_kanban_tasks(task_key, task_details_key, column_key, column_status)
        if data == "success":
            task_status = await TaskCenterDao.get_tasks_details_status(task_key)
            if all(v.get("is_complete") == "未开始" for v in task_status):
                status = "未开始"
            elif all(v.get("is_complete") == "已完成" for v in task_status):
                status = "已完成"
            else:
                status = "进行中"
            ts_res = await TaskCenterDao.edit_tasks(task_key, status)
        else:
            res = 1
            ts_res = "unknown"
        if ts_res == "success" and res == 0:
            return {"msg": "编辑成功"}
        else:
            return {"msg": "存在失败情况"}
