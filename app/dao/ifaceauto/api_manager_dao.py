# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 14:26
# @Author  : lwc
# @File    : api_manager_dao.py
# @Description :
import uuid

from sqlalchemy.sql.functions import count
from app.core.db import async_session
from sqlmodel import select,delete,update,and_,desc,func,or_,literal
from typing import List
from app.models.str_api_project import StrApiProject
from app.models.str_api_branch import StrApiBranch
from app.models.str_api_folder import StrApiFolder
from app.models.str_api_document import StrApiDocument
from app.models.str_api_env import StrApiEnv
from app.utils.my_util import is_empty

class ApiManagerDao:

    @staticmethod
    async def add_api_project(project_key:str, project_name: str, project_desc: str, user_key: str) -> dict:
        try:
            async with async_session() as session:
                api_project = StrApiProject(
                    project_key = project_key,
                    project_name = project_name,
                    project_desc = project_desc,
                    user_key = user_key
                )
                session.add(api_project)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def edit_api_project(project_key: str, project_name: str, project_desc: str) -> dict:
        try:
            async with async_session() as session:
                u_sql = update(StrApiProject).where(
                    StrApiProject.project_key == project_key
                ).values(
                    project_name=project_name,
                    project_desc=project_desc,
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_project(project_key:str) -> dict:
        try:
            async with async_session() as session:
                d_project_sql = update(StrApiProject).where(
                    StrApiProject.project_key == project_key
                ).values(is_delete = 1)
                d_branch_sql = update(StrApiBranch).where(
                    StrApiBranch.project_key == project_key
                ).values(is_delete=1)
                d_folder_sql = update(StrApiFolder).where(
                    StrApiFolder.project_key == project_key
                ).values(is_delete=1)
                d_doc_sql = update(StrApiDocument).where(
                    StrApiDocument.project_key == project_key
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
    async def get_api_projects():
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiProject
            ).where(StrApiProject.is_delete==0)
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def add_api_branch(project_key: str, branch_key: str, branch_name: str, is_default: int) -> dict:
        """
        添加空分支
        :param project_key:
        :param branch_key:
        :param branch_name:
        :param is_default:
        :return:
        """
        try:
            async with async_session() as session:
                api_branch = StrApiBranch(
                    project_key=project_key,
                    branch_key=branch_key,
                    branch_name=branch_name,
                    is_default=is_default
                )
                session.add(api_branch)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def add_api_copy_branch(project_key: str, branch_key: str, branch_name: str, source_key: str) -> dict:
        """
        添加复制分支
        :param project_key:
        :param branch_key:
        :param branch_name:
        :param source_key:
        :return:
        """
        try:
            async with async_session() as session:
                api_branch = StrApiBranch(
                    project_key=project_key,
                    branch_key=branch_key,
                    branch_name=branch_name,
                    is_default=0
                )
                session.add(api_branch)
                source_folders = await session.execute(
                    select(StrApiFolder).where(
                        StrApiFolder.project_key == project_key,
                        StrApiFolder.branch_key == source_key,
                        StrApiFolder.is_delete == 0
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

                    new_folder = StrApiFolder(
                        folder_key=new_folder_key,
                        project_key=project_key,
                        branch_key=branch_key,
                        folder_name=old_folder.folder_name,
                        folder_order=old_folder.folder_order,
                        is_delete=old_folder.is_delete
                    )
                    new_folders.append(new_folder)
                session.add_all(new_folders)
                source_apis = await session.exec(
                    select(StrApiDocument).where(
                        StrApiDocument.project_key == project_key,
                        StrApiDocument.branch_key == source_key,
                        StrApiDocument.is_delete == 0
                    )
                )
                source_api_list = source_apis.all()
                if source_api_list:
                    new_api_docs = []
                    for old_api_doc in source_api_list:
                        new_folder_key = folder_key_map.get(old_api_doc.folder_key, "")
                        new_api_doc = StrApiDocument(
                            project_key=project_key,
                            folder_key = new_folder_key,
                            branch_key = branch_key,
                            doc_name = old_api_doc.doc_name,
                            doc_transfer_protocol=old_api_doc.doc_transfer_protocol,
                            doc_ip=old_api_doc.doc_ip,
                            doc_port=old_api_doc.doc_port,
                            doc_path=old_api_doc.doc_path,
                            doc_method=old_api_doc.doc_method,
                            doc_operationId=old_api_doc.doc_operationId,
                            doc_req_content_type=old_api_doc.doc_req_content_type,
                            doc_req_params=old_api_doc.doc_req_params,
                            doc_req_required=old_api_doc.doc_req_required,
                            doc_res_status=old_api_doc.doc_res_status,
                            doc_res_content_type=old_api_doc.doc_res_content_type,
                            doc_res_params=old_api_doc.doc_res_params,
                            doc_res_required=old_api_doc.doc_res_required,
                            doc_order=old_api_doc.doc_order,
                            doc_desc=old_api_doc.doc_desc,
                            doc_content=old_api_doc.doc_content,
                            is_delete=old_api_doc.is_delete
                        )
                        new_api_docs.append(new_api_doc)
                    session.add_all(new_api_docs)
                await session.commit()
            return {"msg": "复制分支成功"}
        except Exception as e:
            return {"msg": "复制分支失败"}


    @staticmethod
    async def get_api_folders(project_key: str, branch_key:str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiFolder.project_key,StrApiFolder.branch_key, StrApiFolder.folder_key,
                StrApiFolder.folder_name, StrApiFolder.folder_order, literal('group').label("type")
            ).where(and_(
                StrApiFolder.is_delete == 0,
                StrApiFolder.project_key == project_key,
                StrApiFolder.branch_key == branch_key
            ))
            result = await session.execute(quary)
            res_data = result.mappings().all()
        return res_data

    @staticmethod
    async def get_api_docs(project_key: str, branch_key:str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiDocument.project_key,StrApiDocument.branch_key,StrApiDocument.folder_key,
                StrApiDocument.doc_key,StrApiDocument.doc_name,StrApiDocument.doc_transfer_protocol,StrApiDocument.doc_ip,
                StrApiDocument.doc_port,StrApiDocument.doc_path,StrApiDocument.doc_method,
                StrApiDocument.doc_operationId,StrApiDocument.doc_req_content_type,StrApiDocument.doc_req_params,
                StrApiDocument.doc_req_required,StrApiDocument.doc_res_status,StrApiDocument.doc_res_content_type,
                StrApiDocument.doc_res_params,StrApiDocument.doc_res_required,
                StrApiDocument.doc_order,StrApiDocument.doc_desc,literal('api').label("type")
            ).where(and_(
                StrApiDocument.is_delete == 0,
                StrApiDocument.project_key == project_key,
                StrApiDocument.branch_key == branch_key
            ))
            result = await session.execute(quary)
            res_data = result.mappings().all()
        return res_data


    @staticmethod
    async def edit_api_branch(branch_key: str, branch_name: str, branch_order: int) -> dict:
        try:
            async with async_session() as session:
                u_sql = update(StrApiBranch).where(
                    StrApiBranch.branch_key == branch_key
                ).values(
                    branch_name=branch_name,
                    branch_order=branch_order,
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_branch(branch_key: str) -> dict:
        try:
            async with async_session() as session:
                d_branch_sql = update(StrApiBranch).where(
                    StrApiBranch.branch_key == branch_key
                ).values(is_delete=1)
                d_folder_sql = update(StrApiFolder).where(
                    StrApiFolder.branch_key == branch_key
                ).values(is_delete=1)
                d_doc_sql = update(StrApiDocument).where(
                    StrApiDocument.branch_key == branch_key
                ).values(is_delete=1)
                await session.execute(d_branch_sql)
                await session.execute(d_folder_sql)
                await session.execute(d_doc_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def get_api_branch(project_key:str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiBranch
            ).where(and_(StrApiBranch.is_delete == 0, StrApiBranch.project_key == project_key)).order_by(desc(StrApiBranch.branch_order))
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def get_api_branch_count(project_key: str):
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                count(StrApiBranch.branch_key)
            ).where(and_(StrApiBranch.is_delete == 0, StrApiBranch.project_key == project_key))
            result = await session.execute(quary)
            res_data = result.one()
        return res_data

    @staticmethod
    async def add_api_folder(project_key: str, branch_key: str, folder_key: str, folder_name:str) -> dict:
        """
        添加目录
        :param project_key:
        :param branch_key:
        :param folder_key:
        :param folder_name:
        :return:
        """
        try:
            async with async_session() as session:
                api_branch = StrApiFolder(
                    folder_key=folder_key,
                    project_key=project_key,
                    branch_key=branch_key,
                    folder_name=folder_name
                )
                session.add(api_branch)
                await session.commit()
            return {"msg": "新增成功"}
        except Exception as e:
            return {"msg": "新增失败"}

    @staticmethod
    async def edit_api_folder(folder_key: str, folder_name: str) -> dict:
        try:
            async with async_session() as session:
                u_sql = update(StrApiFolder).where(
                    StrApiFolder.folder_key == folder_key
                ).values(
                    folder_name=folder_name
                )
                await session.execute(u_sql)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api_folder(folder_key: str) -> dict:
        try:
            async with async_session() as session:
                d_folder_sql = update(StrApiFolder).where(
                    StrApiFolder.folder_key == folder_key
                ).values(is_delete=1)
                d_doc_sql = update(StrApiDocument).where(
                    StrApiDocument.folder_key == folder_key
                ).values(is_delete=1)
                await session.execute(d_folder_sql)
                await session.execute(d_doc_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def manage_api_env(env_key: str, env_name: str, env_icon: str, env_url: str, env_color: str) -> dict:
        """
        添加目录
        :param env_key:
        :param env_name:
        :param env_icon:
        :param env_url:
        :param env_color
        :return:
        """
        try:
            async with async_session() as session:
                api_env = StrApiEnv(
                    env_key=env_key,
                    env_name=env_name,
                    env_icon=env_icon,
                    env_url=env_url,
                    env_color=env_color,
                )
                await session.merge(api_env)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            print(e)
            return {"msg": "编辑失败"}


    @staticmethod
    async def get_api_env():
        """
        :return:
        """
        async with async_session() as session:
            quary = select(
                StrApiEnv
            ).where(StrApiEnv.is_delete == 0)
            result = await session.execute(quary)
            res_data = result.scalars().all()
        return res_data

    @staticmethod
    async def del_api_env(env_key: str) -> dict:
        try:
            async with async_session() as session:
                d_env_sql = update(StrApiEnv).where(
                    StrApiEnv.env_key == env_key
                ).values(is_delete=1)
                await session.execute(d_env_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def manage_api(project_key:str, folder_key:str, branch_key:str, doc_key:str, doc_name:str,
                         doc_path:str, doc_method:str, doc_req_content_type:str,
                         doc_req_params:str, doc_res_content_type:str,
                         doc_res_params:str, doc_desc:str, doc_content:str, doc_debug_json:str) -> dict:
        """
        编辑api接口描述文档
        :param doc_key:
        :param project_key:
        :param folder_key:
        :param branch_key:
        :param doc_name:
        :param doc_transfer_protocol:
        :param doc_method:
        :param doc_operationId:
        :param doc_req_content_type:
        :param doc_req_params:
        :param doc_req_required:
        :param doc_res_status:
        :param doc_res_content_type:
        :param doc_res_params:
        :param doc_res_required:
        :param doc_desc:
        :param doc_content:
        :param doc_debug_json:
        :return:
        """
        try:
            async with async_session() as session:
                api = StrApiDocument(
                    project_key=project_key,
                    folder_key=folder_key,
                    branch_key=branch_key,
                    doc_key=doc_key,
                    doc_name=doc_name,
                    doc_path=doc_path,
                    doc_method=doc_method,
                    doc_operationId=doc_name,
                    doc_req_content_type=doc_req_content_type,
                    doc_req_params=doc_req_params,
                    doc_req_required='',
                    doc_res_status="200",
                    doc_res_content_type=doc_res_content_type,
                    doc_res_params=doc_res_params,
                    doc_res_required='',
                    doc_desc=doc_desc,
                    doc_content=doc_content,
                    doc_debug_json=doc_debug_json
                )
                await session.merge(api)
                await session.commit()
            return {"msg": "编辑成功"}
        except Exception as e:
            print(e)
            return {"msg": "编辑失败"}

    @staticmethod
    async def del_api(doc_key: str) -> dict:
        try:
            async with async_session() as session:
                d_sql = update(StrApiDocument).where(
                    StrApiDocument.doc_key == doc_key
                ).values(is_delete=1)
                await session.execute(d_sql)
                await session.commit()
            return {"msg": "删除成功"}
        except Exception as e:
            return {"msg": "删除失败"}

    @staticmethod
    async def get_api_yml(p_key:str, b_key:str, o_id:str):

        async with async_session() as session:
            quary = select(
                StrApiDocument.doc_content
            ).where(
                and_(
                    StrApiDocument.project_key == p_key,
                    StrApiDocument.branch_key == b_key,
                    StrApiDocument.doc_operationId == o_id
                )
            )
            result = await session.execute(quary)
            res_data = result.mappings().all()
        return res_data