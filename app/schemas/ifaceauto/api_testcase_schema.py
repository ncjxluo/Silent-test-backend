# -*- coding: utf-8 -*-
# @Time    : 2026/3/30 15:56
# @Author  : lwc
# @File    : api_testcase_schema.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from pydantic import RootModel
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class AddApiCaseProjectRequest(BaseModel):
    case_project_name: str
    case_project_desc: Optional[str]


class EditApiCaseProjectRequest(BaseModel):
    case_project_key: str
    case_project_name: str
    case_project_desc: Optional[str]

class DelApiCaseProjectRequest(BaseModel):
    case_project_key: str

class ApiCaseProjectResponse(BaseResponseModel):

    case_project_key: Optional[str]
    case_project_name: Optional[str]
    case_project_desc: Optional[str]
    user_key: Optional[str]
    created_at: Optional[datetime]

class AddApiCaseBranchRequest(BaseModel):

    case_project_key: str
    case_branch_name: str
    case_branch_source: str

class EditApiBranchRequest(BaseModel):

    branch_key: str
    branch_name: str
    branch_order: int

class DelApiBranchRequest(BaseModel):

    branch_key: str

class ApiCaseBranchResponse(BaseResponseModel):

    case_branch_key: Optional[str]
    case_branch_name: Optional[str]
    is_default: Optional[int]
    created_at: Optional[datetime]

class TestCaseItem(BaseModel):
    case_project_key: str
    case_branch_key: str
    case_folder_key: Optional[str] = None
    case_key: str
    case_name: str
    case_content: str
    case_struct_data: str
    type:Optional[str] = ''
    label:Optional[str] = ''

class TestCasesData(BaseModel):
    case_project_key: str
    case_branch_key: str
    case_folder_key: str
    case_folder_name: str
    case_folder_order: int
    type: Optional[str] = ''
    label: Optional[str] = ''
    children: Optional[List[TestCaseItem]] = None


class TestCaseDataResponse(BaseModel):
    testcases: List[Union[TestCaseItem, TestCasesData]]


class AddApiCaseFolderRequest(BaseModel):

    case_project_key: str
    case_branch_key: str
    case_folder_key: str
    case_folder_name: str


class EditApiCaseFolderRequest(BaseModel):

    case_folder_key: str
    case_folder_name: str


class DelApiCaseFolderRequest(BaseModel):
    case_folder_key: str

class FoldersResponse(BaseModel):

    case_folder_key:str
    case_folder_name: str


class ComponentsItem(BaseModel):

    component_key: str
    component_name: str
    component_type: str
    component_category: str
    component_xml_tag: str
    is_container: int
    parent_keys: List
    allow_child_categories: List
    props:List
    component_order: int
    component_desc: str

class ApiTestCaseRequest(BaseModel):

    case_key:str
    case_project_key:str
    case_folder_key:str
    case_branch_key: str
    case_name: str
    case_content: str
    case_struct_data: List


class DebugTestCaseRequest(BaseModel):

    agent_key: str
    case_name: str
    case_content: str


class TaskTestCaseRequest(BaseModel):

    task_name: str
    twins_flame: bool
    agent_key: str
    task_cases: List

class DelTestCaseRequest(BaseModel):

    case_project_key: str
    case_branch_key: str
    case_key: str