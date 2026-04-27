# -*- coding: utf-8 -*-
# @Time    : 2026/3/30 15:59
# @Author  : lwc
# @File    : api_testcase_service.py
# @Description :

import json
from http.client import responses
from exceptiongroup import catch
from sqlalchemy import false
from app.dao.ifaceauto.api_testcase_dao import ApiTestCaserDao
import uuid
from app.utils.my_util import is_empty
from collections import defaultdict
from typing import List,Optional,Union,Dict,Any
from app.utils.http_request import api_request
from app.utils.http_content_type_enum import HttpContentTypeEnum
from app.utils.parser_xml import parse_test_plan_xml
from app.dao.ifaceauto.api_task_dao import ApiTaskDao
from app.dao.ifaceauto.api_manager_dao import ApiManagerDao
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
import yaml
import re

class ApiTestCaseService:

    @staticmethod
    async def add_api_case_project(case_project_name: str, case_project_desc: str, user_key:str):
        case_project_key = str(uuid.uuid4())
        data = await ApiTestCaserDao.add_api_case_project(case_project_key, case_project_name, case_project_desc, user_key)
        return data

    @staticmethod
    async def get_api_case_projects():
        api_projects = await ApiTestCaserDao.get_api_case_projects()
        return api_projects

    @staticmethod
    async def edit_api_case_project(case_project_key: str, case_project_name: str, case_project_desc: str):
        data = await ApiTestCaserDao.edit_api_case_project(case_project_key, case_project_name, case_project_desc)
        return data

    @staticmethod
    async def del_api_case_project(case_project_key: str):
        data = await ApiTestCaserDao.del_api_case_project(case_project_key)
        return data

    @staticmethod
    async def add_api_case_branch(case_project_key:str, case_branch_name: str, branch_source: str):
        b_count = await ApiTestCaserDao.get_api_case_branch_count(case_project_key)
        is_default = 0
        if b_count[0] == 0:
            is_default = 1
        branch_key = str(uuid.uuid4())
        if is_empty(branch_source):
            data = await ApiTestCaserDao.add_api_case_branch(case_project_key, branch_key, case_branch_name, is_default)
        else:
            data = await ApiTestCaserDao.add_api_copy_branch(case_project_key, branch_key, case_branch_name, branch_source)
        return data

    @staticmethod
    async def get_api_case_branchs(case_project_key:str):
        api_projects = await ApiTestCaserDao.get_api_case_branch(case_project_key)
        return api_projects

    @staticmethod
    async def edit_api_case_branch(case_branch_key: str, case_branch_name: str, case_branch_order: int):
        data = await ApiTestCaserDao.edit_api_case_branch(case_branch_key, case_branch_name, case_branch_order)
        return data

    @staticmethod
    async def del_api_case_branch(case_branch_key: str):
        data = await ApiTestCaserDao.del_api_case_branch(case_branch_key)
        return data

    @staticmethod
    async def get_testcases(case_project_key: str, case_branch_key:str):
        case_folder_data = await ApiTestCaserDao.get_api_case_folders(case_project_key, case_branch_key)
        test_case_data = await ApiTestCaserDao.get_api_testcase(case_project_key, case_branch_key)
        api_case_map = defaultdict(list)
        no_folder_api_list = []
        for test_case in test_case_data:
            if is_empty(test_case.case_folder_key):
                no_folder_api_list.append({**test_case, 'label': test_case.case_name})
            else:
                api_case_map[test_case.case_folder_key].append({**test_case, 'label': test_case.case_name})
        test_cases = []
        for case_folder in case_folder_data:
            test_cases.append(
                {
                    "case_project_key": case_folder.case_project_key,
                    "case_branch_key": case_folder.case_branch_key,
                    "case_folder_key": case_folder.case_folder_key,
                    "case_folder_name": case_folder.case_folder_name,
                    "case_folder_order": case_folder.case_folder_order,
                    "type": case_folder.type,
                    "label": case_folder.case_folder_name,
                    "children": api_case_map.get(case_folder.case_folder_key, [])
                }
            )
        test_cases.extend(no_folder_api_list)
        return {"testcases": test_cases}


    @staticmethod
    async def add_api_case_folder(case_project_key: str, case_branch_key: str, case_folder_key: str, case_folder_name: str):
        data = await ApiTestCaserDao.add_api_case_folder(case_project_key, case_branch_key, case_folder_key, case_folder_name)
        return data

    @staticmethod
    async def edit_api_case_folder(case_folder_key: str, case_folder_name: str):
        data = await ApiTestCaserDao.edit_api_case_folder(case_folder_key, case_folder_name)
        return data

    @staticmethod
    async def del_api_case_folder(case_folder_key: str):
        data = await ApiTestCaserDao.del_api_case_folder(case_folder_key)
        return data

    @staticmethod
    async def get_api_case_folder(case_project_key: str, case_branch_key: str):
        data = await ApiTestCaserDao.get_api_case_folder(case_project_key, case_branch_key)
        print(f"目录{data}")
        return data
    
    @staticmethod
    async def get_api_components():
        data = await ApiTestCaserDao.get_api_components()
        result_list = []
        for item in data:
            data_dict = item.dict()
            for key in ["parent_keys", "allow_child_categories", "props"]:
                value = data_dict.get(key)
                if value:  # 不为空才解析
                    try:
                        data_dict[key] = json.loads(value)
                    except json.JSONDecodeError:
                        data_dict[key] = []
            result_list.append(data_dict)
        return result_list


    @staticmethod
    async def manage_api_testcase(case_project_key:str, case_branch_key:str, case_folder_key:str, case_key:str, case_name:str, case_content:str, case_struct_data:List):
        data = await ApiTestCaserDao.manage_api_testcase(case_project_key, case_branch_key, case_folder_key, case_key, case_name, case_content, json.dumps(case_struct_data, ensure_ascii=False))
        return data

    @staticmethod
    async def del_api_testcase(project_key: str, branch_key: str, case_key: str):
        data = await ApiTestCaserDao.del_api_testcase(project_key, branch_key, case_key)
        return data

    @staticmethod
    async def debug_api_testcase(agent_key:str ,case_name:str, case_content:str, current_user_key:str):
        try:
            api_data = parse_test_plan_xml(case_content)
            api_list = []
            for item in api_data:
                res_data = await ApiManagerDao.get_api_yml(item.get('api_project'),item.get('api_branch'),item.get('interface_name'))
                api_list.append(res_data[0].doc_content)
            print('1')
            print(api_list)
            task_key = str(uuid.uuid4())
            res = await ApiTaskDao.assign_temp_task(
                task_key,'临时调试任务', agent_key, 'ready','api',
                str(uuid.uuid4()), case_name, case_content, json.dumps(api_list, ensure_ascii=False), current_user_key
            )
            return {"msg": f"{res.get('msg')}", "task_key": f"{task_key}"}
        except Exception as e:
            print(e)
            return {"msg": "任务下发失败"}

    @staticmethod
    async def send_case_task(agent_key: str, task_name: str, tasks: List, twins_flame: bool, current_user_key: str):
        try:
            plans = []
            task_key = str(uuid.uuid4())
            for task in tasks:
                api_data = parse_test_plan_xml(task.get('case_content'))
                api_list = []
                for api in api_data:
                    res_data = await ApiManagerDao.get_api_yml(api.get('api_project'), api.get('api_branch'),
                                                               api.get('interface_name'))
                    api_list.append(res_data[0].doc_content)
                plan_key = str(uuid.uuid4())
                plans.append(
                    StrTestPlan(
                        suite_key=task_key,
                        plan_key=plan_key,
                        plan_name=task.get('case_name'),
                        case_content=task.get('case_content'),
                        doc_content=json.dumps(api_list, ensure_ascii=False),
                        status='ready'
                    )
                )
            suite = StrTestSuite(
                user_key=current_user_key,
                suite_key=task_key,
                suite_name=task_name,
                suite_agent_key=agent_key,
                twins_flame=1 if twins_flame else 0,
                status='ready',
                type='api'
            )
            res = await ApiTaskDao.assign_tasks(suite, plans)
            return {"msg": f"{res.get('msg')}", "task_key": f"{task_key}"}
        except Exception as e:
            print(e)
            return {"msg": "任务下发失败"}
