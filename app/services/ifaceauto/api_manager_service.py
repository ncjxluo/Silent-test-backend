# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 14:25
# @Author  : lwc
# @File    : api_manager_service.py
# @Description :

import json
from http.client import responses
from app.utils.my_util import normalize_example
from app.dao.ifaceauto.api_manager_dao import ApiManagerDao
import uuid
from app.utils.my_util import is_empty
from collections import defaultdict
from typing import List,Optional,Union,Dict,Any
from app.utils.http_request import api_request
from app.utils.http_content_type_enum import HttpContentTypeEnum
import yaml
import re

class ApiManagerService:

    @staticmethod
    async def add_api_project(project_name: str, project_desc: str, user_key:str):
        project_key = str(uuid.uuid4())
        data = await ApiManagerDao.add_api_project(project_key, project_name, project_desc, user_key)
        return data

    @staticmethod
    async def get_api_projects():
        api_projects = await ApiManagerDao.get_api_projects()
        return api_projects

    @staticmethod
    async def edit_api_project(project_key: str, project_name: str, project_desc: str):
        data = await ApiManagerDao.edit_api_project(project_key, project_name, project_desc)
        return data

    @staticmethod
    async def del_api_project(project_key: str):
        data = await ApiManagerDao.del_api_project(project_key)
        return data

    @staticmethod
    async def add_api_branch(project_key:str, branch_name: str, branch_source: str):
        b_count = await ApiManagerDao.get_api_branch_count(project_key)
        is_default = 0
        if b_count[0] == 0:
            is_default = 1
        branch_key = str(uuid.uuid4())
        if is_empty(branch_source):
            data = await ApiManagerDao.add_api_branch(project_key, branch_key, branch_name, is_default)
        else:
            data = await ApiManagerDao.add_api_copy_branch(project_key, branch_key, branch_name, branch_source)
        return data

    @staticmethod
    async def get_api_branchs(project_key:str):
        api_projects = await ApiManagerDao.get_api_branch(project_key)
        return api_projects

    @staticmethod
    async def edit_api_branch(branch_key: str, branch_name: str, branch_order: int):
        data = await ApiManagerDao.edit_api_branch(branch_key, branch_name, branch_order)
        return data

    @staticmethod
    async def del_api_branch(branch_key: str):
        data = await ApiManagerDao.del_api_branch(branch_key)
        return data

    @staticmethod
    async def get_apis(project_key: str, branch_key:str):
        folder_data = await ApiManagerDao.get_api_folders(project_key, branch_key)
        api_doc_data = await ApiManagerDao.get_api_docs(project_key, branch_key)
        api_map = defaultdict(list)
        no_folder_api_list = []
        for api_doc in api_doc_data:
            if is_empty(api_doc.folder_key):
                no_folder_api_list.append({**api_doc, 'label': api_doc.doc_name})
            else:
                api_map[api_doc.folder_key].append({**api_doc, 'label': api_doc.doc_name})
        api_docs = []
        for folder in folder_data:
            api_docs.append(
                {
                    "project_key": folder.project_key,
                    "branch_key": folder.branch_key,
                    "folder_key": folder.folder_key,
                    "folder_name": folder.folder_name,
                    "folder_order": folder.folder_order,
                    "type": folder.type,
                    "label": folder.folder_name,
                    "children": api_map.get(folder.folder_key, [])
                }
            )
        api_docs.extend(no_folder_api_list)
        return {"apis": api_docs}


    @staticmethod
    async def add_api_folder(project_key: str, branch_key: str, folder_key: str, folder_name: str):
        data = await ApiManagerDao.add_api_folder(project_key, branch_key, folder_key, folder_name)
        return data

    @staticmethod
    async def edit_api_folder(folder_key: str, folder_name: str):
        data = await ApiManagerDao.edit_api_folder(folder_key, folder_name)
        return data

    @staticmethod
    async def del_api_folder(folder_key: str):
        data = await ApiManagerDao.del_api_folder(folder_key)
        return data

    @staticmethod
    async def manage_api_env(env_key: str, env_name: str, env_icon: str, env_url: str, env_color: str):
        data = await ApiManagerDao.manage_api_env(env_key, env_name, env_icon, env_url, env_color)
        return data

    @staticmethod
    async def get_api_env():
        env_data = await ApiManagerDao.get_api_env()
        return {"envs": env_data}

    @staticmethod
    async def del_api_env(env_key: str):
        data = await ApiManagerDao.del_api_env(env_key)
        return data

    @staticmethod
    async def api_debug(env_url: str, doc_method: str, doc_path: str, req_content_type: str, api_header_params: dict, req_params: Optional[Union[dict,str]]) -> dict:
        pattern = r"/^https?:\/\/[^\s/$.?#].[^\s]*$/i"
        if re.search(pattern, doc_path):
            url = doc_method
        else:
            url = f"{env_url}{doc_path}"
        api_response = await api_request(
            headers=api_header_params,
            method=doc_method,
            url=url,
            req_content_type=req_content_type,
            params=req_params
        )
        return {"res": api_response}

    @staticmethod
    async def manage_api(project_key: str, branch_key: str, folder_key: str, doc_key: str, doc_name:str,
                         doc_method: str, doc_path: str, doc_desc: str,
                         apiParams: List, apiParamsFdata:List, apiParamsJson: List,
                         debug_json_params: str, req_content_type: str, res_content_type: str,
                         apiResResult:List, version:str, author:str):

        if doc_method == "GET":
            params = apiParams
        else:
            if req_content_type == 'json':
                params = apiParamsJson
            elif req_content_type == 'form_data':
                params = apiParamsFdata
            else:
                params = None
        swagger_yml = ApiManagerService.build_swagger_yaml(
            doc_name,doc_method,doc_path,doc_desc,params,req_content_type,res_content_type,apiResResult,
            version, author
        )
        print(f"最后一步生成值:{swagger_yml}")
        res = await ApiManagerDao.manage_api(
            project_key, folder_key, branch_key, doc_key, doc_name, doc_path, doc_method,
            req_content_type, json.dumps(params,ensure_ascii=False), res_content_type, json.dumps(apiResResult,ensure_ascii=False),
            doc_desc, swagger_yml, debug_json_params
        )
        return res


    @staticmethod
    def build_swagger_yaml(doc_name:str, doc_method:str, doc_path:str, doc_desc:str, req_params:List,
                           req_content_type:str, res_content_type:str, res_result_params:List,
                           version:str, author:str):
        """
        这个要生成swagger格式的yml文档，以便于后续用例执行的时候使用
        :param doc_name:
        :param doc_method:
        :param doc_path:
        :param doc_desc:
        :param req_params:
        :param req_content_type:
        :param res_content_type:
        :param res_result_params:
        :param version:
        :param author:
        :return:
        """
        parameters = []
        doc_method = doc_method.lower()
        if doc_method == 'get':
            for param in req_params:
                if param.get('type') == "":
                    schema_type = {}
                else:
                    schema_type = {"type": param.get('type')}
                parameters.append({
                    "in": "query",
                    "name": param.get('name'),
                    "schema": schema_type,
                    "description": param.get('desc', ''),
                    "example": normalize_example(param.get('example'), param.get('type'))
                    # "example": param.get('example')
                })
        request_body = None
        if doc_method == 'post' and req_params is not None:
            properties = {}
            required = []
            for param in req_params:
                prop_name = param.get('name')
                if param.get('type') == "":
                    prop_type = {}
                else:
                    prop_type = param.get('type')
                properties[prop_name] = {
                    "type": prop_type,
                    "description": param.get('desc', ''),
                    "example": normalize_example(param.get('example'), param.get('type'))
                    # "example": param.get('example')
                }
                if param.get('status') is True:  # 你数据中用 status 表示必填
                    required.append(prop_name)
            request_body = {
                "content": {
                    HttpContentTypeEnum[req_content_type].swagger: {
                        "schema": {
                            "type": "object",
                            "properties": properties,
                            "required": required if required else []
                        }
                    }
                }
            }
        res_properties = {}
        res_required = []
        for res in res_result_params:
            name = res.get('name')
            res_type = res.get('type', 'string')
            res_properties[name] = {
                "type": res_type,
                "description": res.get('desc', '')
            }
            if res.get('status') is True:
                res_required.append(name)
            if res_type == 'array':
                res_properties[name]["items"] = {"type": "object"}

        openapi_spec: Dict[str, Any] = {
            "openapi": "3.0.0",
            "info": {
                "title": doc_name,
                "description": doc_desc,
                "version": version,
                "contact": {"name": f"{author}"}
            },
            "servers": [
                {"url": "${scheme}://${host}:${scheme_port}", "description": "接口测试服务器"}
            ],
            "paths": {
                doc_path: {
                    doc_method: {
                        "operationId": doc_name,
                        "summary": doc_desc,
                        "description": doc_desc,
                    }
                }
            }
        }
        if doc_method in ['get', 'delete', 'head']:
            if parameters:
                print('wolaile ')
                print(openapi_spec)
                openapi_spec["paths"][doc_path][doc_method]["parameters"] = parameters
        else:
            if request_body:
                openapi_spec["paths"][doc_path][doc_method]["requestBody"] = request_body
            elif parameters: # 这里应该是根据req_content_type来的
                openapi_spec["paths"][doc_path][doc_method]["parameters"] = parameters

        openapi_spec["paths"][doc_path][doc_method]["responses"] = {
            "200": {
                "description": "操作成功",
                "content": {
                    HttpContentTypeEnum[res_content_type].swagger: {
                        "schema": {
                            "type": "object",
                            "properties": res_properties,
                            "required": res_required if res_required else []
                        }
                    }
                }
            }
        }
        print(f"最后一步{openapi_spec}")

        # yaml_str = yaml.dump(openapi_spec, allow_unicode=True, sort_keys=False, width=10000, indent=2)
        return json.dumps(openapi_spec, ensure_ascii=False)

    @staticmethod
    async def del_api(doc_key: str):
        data = await ApiManagerDao.del_api(doc_key)
        return data



