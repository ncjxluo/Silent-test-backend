# -*- coding: utf-8 -*-
# @Time    : 2026/3/9 17:21
# @Author  : lwc
# @File    : task_center_dao.py
# @Description :
import uuid

from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from typing import List
from app.models.str_kanban_boards import StrKanbanBoards
from app.models.str_kanban_columns import StrKanbanColumns
from app.models.str_testing_task import StrTestingTask
from app.models.str_testing_task_details import StrTestingTaskDetails
from app.utils.my_util import is_empty

class TaskCenterDao:

    @staticmethod
    async def add_kanban_temp(kanban_key:str, board_name:str, kanban_columns:List, board_description:str) -> dict:
        try:
            async with async_session() as session:
                kanban = StrKanbanBoards(
                    board_key = kanban_key,
                    board_name=board_name,
                    board_description=board_description
                )
                kanban_column_list = []
                for item in kanban_columns:
                    kanban_column = StrKanbanColumns(
                        board_key = kanban_key,
                        column_key = item.get("column_key"),
                        column_name=item.get("column_name"),
                        sort_order=item.get("sort_order"),
                        column_status=item.get("column_status"),
                    )
                    kanban_column_list.append(kanban_column)
                session.add(kanban)
                session.add_all(kanban_column_list)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def get_kanban_temp(k_name:str, current_page:int, current_count:int) -> dict:
        async with (async_session() as session):
            query = select(StrKanbanBoards.board_key, StrKanbanBoards.board_name, StrKanbanBoards.board_description,
                           StrKanbanColumns.column_key, StrKanbanColumns.column_name, StrKanbanColumns.sort_order, StrKanbanColumns.column_status).join(
                StrKanbanColumns, StrKanbanColumns.board_key == StrKanbanBoards.board_key, isouter=True
            ).order_by(StrKanbanColumns.board_key,StrKanbanColumns.sort_order)
            if not is_empty(k_name):
                query = query.where(
                        StrKanbanBoards.board_name.like(f"{k_name}")
                    )
            query = query.order_by(desc(StrKanbanBoards.created_at)).offset(
                (current_page - 1) * current_count).limit(
                current_count)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_kanban_temp_count(k_name:str) -> dict:
        async with (async_session() as session):
            query = select(
                func.count(StrKanbanBoards.board_key)
            )
            if not is_empty(k_name):
                query = query.where(
                    StrKanbanBoards.board_name.like(f"{k_name}")
                )
            result = await session.execute(query)
            res_data = result.one()
        return res_data

    @staticmethod
    async def edit_kanban_temp(kanban_key: str, board_name: str, kanban_columns: List, board_description: str) -> dict:
        try:
            async with async_session() as session:
                u_k_t_sql = update(StrKanbanBoards).where(StrKanbanBoards.board_key == kanban_key).values(
                    board_name = board_name,
                    board_description = board_description
                )
                await session.execute(u_k_t_sql)
                kanban_column_list = []
                for item in kanban_columns:
                    if item.get("column_key") is None:
                        kanban_column = StrKanbanColumns(
                            board_key=kanban_key,
                            column_key=str(uuid.uuid4()),
                            column_name=item.get("column_name"),
                            sort_order=item.get("sort_order"),
                            column_status=item.get("column_status"),
                        )
                        kanban_column_list.append(kanban_column)
                    else:
                        u_k_c_sql = update(StrKanbanColumns).where(
                            and_(
                                StrKanbanColumns.board_key == kanban_key,
                                StrKanbanColumns.column_key == item.get("column_key")
                            )
                        ).values(
                            column_name = item.get("column_name"),
                            sort_order= item.get("sort_order"),
                            column_status=item.get("column_status")
                        )
                        await session.execute(u_k_c_sql)
                session.add_all(kanban_column_list)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_kanban_temp(board_key:str) -> dict:
        try:
            async with async_session() as session:
                d_sql = delete(StrKanbanBoards).where(StrKanbanBoards.board_key == board_key)
                d_c_sql = delete(StrKanbanColumns).where(StrKanbanColumns.board_key == board_key)
                await session.execute(d_sql)
                await session.execute(d_c_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}


    @staticmethod
    async def del_kanban_column(column_key:str) -> dict:
        try:
            async with async_session() as session:
                d_sql = delete(StrKanbanColumns).where(StrKanbanColumns.column_key == column_key)
                await session.execute(d_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def add_task(task_key: str, task_name: str, task_num: int, version_num: str, release_time: str,
                       is_complete:str, task_details: List) -> dict:
        try:
            async with async_session() as session:
                task = StrTestingTask(
                    task_key = task_key,
                    task_name = task_name,
                    task_num = task_num,
                    version_num = version_num,
                    release_time = release_time,
                    is_complete = is_complete,
                )
                task_details_list = []
                for item in task_details:
                    task_detail = StrTestingTaskDetails(
                        task_details_key = item.get("task_details_key"),
                        task_key = task_key,
                        task_details_title = item.get("task_details_title"),
                        correlation_num = item.get("correlation_num"),
                        description = item.get("description"),
                        priority = item.get("priority"),
                        assignee_key = item.get("assignee_key"),
                        expect_day = item.get("expect_day"),
                        board_key =  item.get("board_key"),
                        column_key = item.get("column_key"),
                        is_complete = is_complete
                    )
                    task_details_list.append(task_detail)
                print(task_details_list)
                session.add(task)
                session.add_all(task_details_list)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            print(f'错误:{e}')
            return {"msg": "新增失败"}

    @staticmethod
    async def edit_task(task_key: str, task_name: str, task_num: int, version_num: str, release_time: str, board_key:str, columns_key:str, task_details: List) -> dict:
        try:
            async with async_session() as session:
                u_task_sql = update(StrTestingTask).where(StrTestingTask.task_key == task_key).values(
                    task_name=task_name,
                    task_num=task_num,
                    version_num=version_num,
                    release_time=release_time,
                )
                await session.execute(u_task_sql)
                task_details_list = []
                for item in task_details:
                    if '新增' in item.get("task_details_key"):
                        d_key = str(uuid.uuid4())
                        task_detail = StrTestingTaskDetails(
                            task_details_key=d_key,
                            task_key=task_key,
                            task_details_title=item.get("task_details_title"),
                            correlation_num=item.get("correlation_num"),
                            description=item.get("description"),
                            priority=item.get("priority"),
                            assignee_key=item.get("assignee_key"),
                            expect_day=item.get("expect_day"),
                            board_key=board_key,
                            column_key=columns_key,
                            is_complete='未开始'
                        )
                        task_details_list.append(task_detail)

                    else:
                        u_task_d_sql = update(StrTestingTaskDetails).where(
                            and_(
                                StrTestingTaskDetails.task_key == task_key,
                                StrTestingTaskDetails.task_details_key == item.get("task_details_key")
                            )
                        ).values(
                            task_details_title=item.get("task_details_title"),
                            correlation_num=item.get("correlation_num"),
                            description=item.get("description"),
                            priority=item.get("priority"),
                            assignee_key=item.get("assignee_key"),
                            expect_day=item.get("expect_day")
                        )
                        await session.execute(u_task_d_sql)
                session.add_all(task_details_list)


                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            print(f'错误:{e}')
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_task(task_key: str) -> dict:
        try:
            async with async_session() as session:
                d_sql = delete(StrTestingTask).where(StrTestingTask.task_key == task_key)
                d_c_sql = delete(StrTestingTaskDetails).where(StrTestingTaskDetails.task_key == task_key)
                await session.execute(d_sql)
                await session.execute(d_c_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def del_task_details(task_details_key: str) -> dict:
        try:
            async with async_session() as session:
                d_sql = delete(StrTestingTaskDetails).where(StrTestingTaskDetails.task_details_key == task_details_key)
                await session.execute(d_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def get_kanban_position_column_key(kanban_key:str, place:str) -> dict:
        """
        获取列最大火最小的key值
        :param kanban_key:
        :param place:
        :return:
        """
        async with (async_session() as session):
            query = select(
                StrKanbanColumns.column_key
            ).where(StrKanbanColumns.board_key == kanban_key)
            if place == '1':
                query = query.order_by(StrKanbanColumns.sort_order)
            else:
                query = query.order_by(desc(StrKanbanColumns.sort_order))
            query = query.limit(1)
            result = await session.execute(query)
            res_data = result.one()
        return res_data

    @staticmethod
    async def get_tasks(task_label_name:str, task_condition:str, current_page: int, current_count: int) -> dict:
        async with (async_session() as session):
            query = select(
                StrTestingTask.task_key,StrTestingTask.task_name,StrTestingTask.version_num,StrTestingTask.task_num,StrTestingTask.release_time,StrTestingTask.is_complete,
                StrTestingTaskDetails.task_details_key,StrTestingTaskDetails.task_details_title,StrTestingTaskDetails.assignee_key,StrTestingTaskDetails.board_key,
                StrTestingTaskDetails.correlation_num,StrTestingTaskDetails.description,StrTestingTaskDetails.priority,StrTestingTaskDetails.expect_day
            ).join(StrTestingTaskDetails, StrTestingTaskDetails.task_key == StrTestingTask.task_key, isouter=True).order_by(StrTestingTaskDetails.task_key,StrTestingTaskDetails.assignee_key)
            if task_label_name != '全部':
                query = query.where(StrTestingTask.is_complete == task_label_name)
            if not is_empty(task_condition):
                query = query.where(
                    or_(
                        StrTestingTask.task_name.like(f"{task_condition}"),
                        StrTestingTask.version_num.like(f"{task_condition}"),
                        StrTestingTaskDetails.task_details_title.like(f"{task_condition}")
                    )
                )
            query = query.order_by(desc(StrTestingTask.created_at)).offset(
                (current_page - 1) * current_count).limit(
                current_count)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_tasks_count(task_label_name:str, task_condition:str) -> dict:
        async with (async_session() as session):
            query = select(
                func.count(StrTestingTask.task_key)
            )
            if task_label_name != '全部':
                query = query.where(StrTestingTask.is_complete == task_label_name)
            if not is_empty(task_condition):
                query = query.where(
                    or_(
                        StrTestingTask.task_name.like(f"{task_condition}")
                    )
                )
            result = await session.execute(query)
            res_data = result.one()
        return res_data


    @staticmethod
    async def get_kanban_columns_tasks(k_switch:bool, task_key:str, board_key:str, condition:str, current_user_key:str) -> dict:
        async with (async_session() as session):
            join_conditions = [StrKanbanColumns.board_key == StrTestingTaskDetails.board_key,
                    StrKanbanColumns.column_key == StrTestingTaskDetails.column_key,
                    StrTestingTaskDetails.task_key == task_key,]
            if k_switch:
                join_conditions.append(
                    StrTestingTaskDetails.assignee_key == current_user_key
                )
            if not is_empty(condition):
                join_conditions.append(
                    StrTestingTaskDetails.task_details_title.like(f'%{condition}%')
                )
            query = select(StrKanbanColumns.board_key, StrKanbanColumns.column_key, StrKanbanColumns.column_name,
                            StrKanbanColumns.sort_order,StrKanbanColumns.column_status,
                            StrTestingTaskDetails.task_key,StrTestingTaskDetails.task_details_key,StrTestingTaskDetails.task_details_title,
                           StrTestingTaskDetails.correlation_num,StrTestingTaskDetails.description,StrTestingTaskDetails.priority,
                           StrTestingTaskDetails.assignee_key,StrTestingTaskDetails.expect_day
                               ).join(StrTestingTaskDetails, and_(
                    *join_conditions
                ), isouter=True).where(
                            StrKanbanColumns.board_key == board_key
                ).order_by(StrKanbanColumns.sort_order, StrTestingTaskDetails.assignee_key)

            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data


    @staticmethod
    async def edit_kanban_tasks(task_key: str, task_details_key: str, column_key: str, column_status: str) -> str:
        """
        要改变业务所处的列和任务的状态
        :param task_key:
        :param task_details_key:
        :param column_key:
        :param column_status:
        :return:
        """
        try:
            async with (async_session() as session):
                e_sql = update(StrTestingTaskDetails).where(
                    StrTestingTaskDetails.task_key == task_key,
                    StrTestingTaskDetails.task_details_key == task_details_key,
                ).values(
                    column_key = column_key,
                    is_complete = column_status,
                )
                await session.execute(e_sql)
                await session.commit()
                return "success"
        except Exception as e:
            return "fail"

    @staticmethod
    async def get_tasks_details_status(task_key: str) -> dict:
        """
        获取子任务的状态
        :param task_key: 大任务的key
        :return:
        """
        async with (async_session() as session):
            query = select(StrTestingTaskDetails.is_complete).where(StrTestingTaskDetails.task_key == task_key).group_by(StrTestingTaskDetails.is_complete)
            result = await session.execute(query)
            res_data = result.mappings().all()
        return res_data


    @staticmethod
    async def edit_tasks(task_key: str, status: str) -> str:
        """
        要改变业务所处的列和任务的状态
        :param task_key:
        :param status:
        :return:
        """
        try:
            async with (async_session() as session):
                e_sql = update(StrTestingTask).where(
                    StrTestingTask.task_key == task_key
                ).values(
                    is_complete=status
                )
                await session.execute(e_sql)
                await session.commit()
                return "success"
        except Exception as e:
            return "fail"
