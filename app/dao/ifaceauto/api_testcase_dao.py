# -*- coding: utf-8 -*-
# @Time    : 2026/3/30 16:00
# @Author  : lwc
# @File    : api_testcase_dao.py
# @Description :

import uuid

from sqlalchemy.sql.functions import count
from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from typing import List
from app.models.str_api_case_project import StrApiCaseProject
from app.models.str_api_case_branch import StrApiCaseBranch
from app.models.str_api_case_folder import StrApiCaseFolder
from app.models.str_api_test_case import StrApiTestCase
from app.models.str_api_component import StrApiComponent
from app.utils.my_util import is_empty

class ApiTestCaserDao:

    @staticmethod
    async def add_api_case_project(case_project_key:str, case_project_name: str, case_project_desc: str, user_key: str) -> dict:
        try:
            async with async_session() as session:
                api_case_project = StrApiCaseProject(
                    case_project_key = case_project_key,
                    case_project_name = case_project_name,
                    case_project_desc = case_project_desc,
                    user_key = user_key
                )
                session.add(api_case_project)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def edit_api_case_project(case_project_key: str, case_project_name: str, case_project_desc: str) -> dict:
        try:
            async with async_session() as session:
                u_sql = update(StrApiCaseProject).where(
                    StrApiCaseProject.case_project_key == case_project_key
                ).values(
                    case_project_name=case_project_name,
                    case_project_desc=case_project_desc,
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_case_project(case_project_key:str) -> dict:
        try:
            async with async_session() as session:
                d_project_sql = update(StrApiCaseProject).where(
                    StrApiCaseProject.case_project_key == case_project_key
                ).values(is_delete = 1)
                d_branch_sql = update(StrApiCaseBranch).where(
                    StrApiCaseBranch.case_project_key == case_project_key
                ).values(is_delete=1)
                d_folder_sql = update(StrApiCaseFolder).where(
                    StrApiCaseFolder.case_project_key == case_project_key
                ).values(is_delete=1)
                d_doc_sql = update(StrApiTestCase).where(
                    StrApiTestCase.case_project_key == case_project_key
                ).values(is_delete=1)
                await session.execute(d_project_sql)
                await session.execute(d_branch_sql)
                await session.execute(d_folder_sql)
                await session.execute(d_doc_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def get_api_case_projects():
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiCaseProject
            ).where(StrApiCaseProject.is_delete==0)
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def add_api_case_branch(case_project_key: str, case_branch_key: str, case_branch_name: str, is_default: int) -> dict:
        try:
            async with async_session() as session:
                api_case_branch = StrApiCaseBranch(
                    case_project_key=case_project_key,
                    case_branch_key=case_branch_key,
                    case_branch_name=case_branch_name,
                    is_default=is_default
                )
                session.add(api_case_branch)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def add_api_copy_branch(case_project_key: str, case_branch_key: str, case_branch_name: str, source_key: str) -> dict:
        try:
            async with async_session() as session:
                api_case_branch = StrApiCaseBranch(
                    case_project_key=case_project_key,
                    case_branch_key=case_branch_key,
                    case_branch_name=case_branch_name,
                    is_default=0
                )
                session.add(api_case_branch)
                source_folders = await session.execute(
                    select(StrApiCaseFolder).where(
                        StrApiCaseFolder.case_project_key == case_project_key,
                        StrApiCaseFolder.case_branch_key == source_key,
                        StrApiCaseFolder.is_delete == 0
                    )
                )
                source_folder_list = source_folders.all()
                if not source_folder_list:
                    await session.commit()
                    return {"msg": "复制分支成功"}
                folder_key_map = {}
                new_folders = []
                for old_folder in source_folder_list:
                    new_folder_key = str(uuid.uuid4())
                    folder_key_map[old_folder.folder_key] = new_folder_key

                    new_folder = StrApiCaseFolder(
                        case_folder_key=new_folder_key,
                        case_project_key=case_project_key,
                        case_branch_key=case_branch_key,
                        case_folder_name=old_folder.folder_name,
                        case_folder_order=old_folder.folder_order,
                        is_delete=old_folder.is_delete
                    )
                    new_folders.append(new_folder)
                session.add_all(new_folders)
                source_apis = await session.exec(
                    select(StrApiTestCase).where(
                        StrApiTestCase.case_project_key == case_project_key,
                        StrApiTestCase.case_branch_key == case_branch_key,
                        StrApiTestCase.is_delete == 0
                    )
                )
                source_api_list = source_apis.all()
                if source_api_list:
                    new_api_docs = []
                    for old_api_doc in source_api_list:
                        new_folder_key = folder_key_map.get(old_api_doc.folder_key, "")
                        new_api_doc = StrApiTestCase(
                            case_project_key=case_project_key,
                            case_folder_key = new_folder_key,
                            case_branch_key = case_branch_key,
                            case_name = old_api_doc.doc_name,
                            case_content=old_api_doc.doc_transfer_protocol,
                            is_delete=old_api_doc.is_delete
                        )
                        new_api_docs.append(new_api_doc)
                    session.add_all(new_api_docs)
                await session.commit()
            return {"msg": "复制分支成功"}
        except Exception as e:
            return {"msg": "复制分支失败"}


    @staticmethod
    async def get_api_case_folders(case_project_key: str, case_branch_key:str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiCaseFolder.case_project_key,
                StrApiCaseFolder.case_branch_key,
                StrApiCaseFolder.case_folder_key,
                StrApiCaseFolder.case_folder_name,
                StrApiCaseFolder.case_folder_order,
                literal('group').label("type")
            ).where(and_(
                StrApiCaseFolder.is_delete == 0,
                StrApiCaseFolder.case_project_key == case_project_key,
                StrApiCaseFolder.case_branch_key == case_branch_key
            ))
            result = await session.execute(quary)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_api_testcase(case_project_key: str, case_branch_key:str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiTestCase.case_project_key,
                StrApiTestCase.case_branch_key,
                StrApiTestCase.case_folder_key,
                StrApiTestCase.case_key,
                StrApiTestCase.case_name,
                StrApiTestCase.case_content,
                StrApiTestCase.case_struct_data,
                literal('case').label("type")
            ).where(and_(
                StrApiTestCase.is_delete == 0,
                StrApiTestCase.case_project_key == case_project_key,
                StrApiTestCase.case_branch_key == case_branch_key
            ))
            result = await session.execute(quary)
            res_data = result.mappings().all()
        return res_data


    @staticmethod
    async def edit_api_case_branch(case_branch_key: str, case_branch_name: str, case_branch_order: int) -> dict:
        try:
            async with async_session() as session:
                u_sql = update(StrApiCaseBranch).where(
                    StrApiCaseBranch.case_branch_key == case_branch_key
                ).values(
                    branch_name=case_branch_name,
                    branch_order=case_branch_order,
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_case_branch(case_branch_key: str) -> dict:
        try:
            async with async_session() as session:
                d_branch_sql = update(StrApiCaseBranch).where(
                    StrApiCaseBranch.case_branch_key == case_branch_key
                ).values(is_delete=1)
                d_folder_sql = update(StrApiCaseFolder).where(
                    StrApiCaseFolder.case_branch_key == case_branch_key
                ).values(is_delete=1)
                d_doc_sql = update(StrApiTestCase).where(
                    StrApiTestCase.case_branch_key == case_branch_key
                ).values(is_delete=1)
                await session.execute(d_branch_sql)
                await session.execute(d_folder_sql)
                await session.execute(d_doc_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def get_api_case_branch(case_project_key:str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiCaseBranch
            ).where(and_(StrApiCaseBranch.is_delete == 0, StrApiCaseBranch.case_project_key == case_project_key)).order_by(desc(StrApiCaseBranch.case_branch_order))
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def get_api_case_branch_count(case_project_key: str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                count(StrApiCaseBranch.case_branch_key)
            ).where(and_(StrApiCaseBranch.is_delete == 0, StrApiCaseBranch.case_project_key == case_project_key))
            result = await session.execute(quary)
            res_data = result.one()
        return res_data

    @staticmethod
    async def add_api_case_folder(case_project_key: str, case_branch_key: str, case_folder_key: str, case_folder_name:str) -> dict:
        try:
            async with async_session() as session:
                api_case_branch = StrApiCaseFolder(
                    case_folder_key=case_folder_key,
                    case_project_key=case_project_key,
                    case_branch_key=case_branch_key,
                    case_folder_name=case_folder_name
                )
                session.add(api_case_branch)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def edit_api_case_folder(case_folder_key: str, case_folder_name: str) -> dict:
        try:
            async with async_session() as session:
                u_sql = update(StrApiCaseFolder).where(
                    StrApiCaseFolder.case_folder_key == case_folder_key
                ).values(
                    case_folder_name=case_folder_name
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_case_folder(case_folder_key: str) -> dict:
        try:
            async with async_session() as session:
                d_folder_sql = update(StrApiCaseFolder).where(
                    StrApiCaseFolder.case_folder_key == case_folder_key
                ).values(is_delete=1)
                d_doc_sql = update(StrApiTestCase).where(
                    StrApiTestCase.case_folder_key == case_folder_key
                ).values(is_delete=1)
                await session.execute(d_folder_sql)
                await session.execute(d_doc_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def get_api_case_folder(case_project_key: str, case_branch_key: str):
        async with async_session() as session:
            quary = select(
                StrApiCaseFolder.case_folder_key,
                StrApiCaseFolder.case_folder_name
            ).where(and_(
                StrApiCaseFolder.case_project_key == case_project_key,
                StrApiCaseFolder.case_branch_key == case_branch_key
            ))
            print('来了')
            print("参数：", case_project_key, case_branch_key)
            result = await session.execute(quary)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_api_components():
        async with async_session() as session:
            query = select(
                StrApiComponent
            ).where(StrApiComponent.is_delete==0).order_by(desc(StrApiComponent.component_order))
            result = await session.execute(query)
            res_data = result.scalars().all()
        return res_data


    @staticmethod
    async def manage_api_testcase(case_project_key:str, case_branch_key:str, case_folder_key:str, case_key:str, case_name:str, case_content:str, case_struct_data:str):
        try:
            async with async_session() as session:
                api_testcase = StrApiTestCase(
                    case_key=case_key,
                    case_project_key=case_project_key,
                    case_folder_key=case_folder_key,
                    case_branch_key=case_branch_key,
                    case_name=case_name,
                    case_content=case_content,
                    case_struct_data=case_struct_data
                )
                await session.merge(api_testcase)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            print(e)
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_testcase(project_key: str, branch_key: str, case_key: str):
        try:
            async with async_session() as session:
                u_sql = update(StrApiTestCase).where(
                    and_(
                        StrApiTestCase.case_project_key == project_key,
                        StrApiTestCase.case_branch_key == branch_key,
                        StrApiTestCase.case_key == case_key,
                    )
                ).values(
                    is_delete = 1
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            print(e)
            return {"msg": "删除失败"}

