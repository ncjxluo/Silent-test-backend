# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 14:25
# @Author  : lwc
# @File    : api_manager_schema.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from pydantic import RootModel
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class AddApiProjectRequest(BaseModel):
    project_name: str
    project_desc: Optional[str]


class EditApiProjectRequest(BaseModel):
    project_key: str
    project_name: str
    project_desc: Optional[str]

class DelApiProjectRequest(BaseModel):
    project_key: str

class ApiProjectResponse(BaseResponseModel):

    project_key: Optional[str]
    project_name: Optional[str]
    project_desc: Optional[str]
    user_key: Optional[str]
    created_at: Optional[datetime]

class AddApiBranchRequest(BaseModel):
    project_key: str
    branch_name: str
    branch_source: str

class EditApiBranchRequest(BaseModel):

    branch_key: str
    branch_name: str
    branch_order: int

class DelApiBranchRequest(BaseModel):

    branch_key: str

class ApiBranchResponse(BaseResponseModel):

    branch_key: Optional[str]
    branch_name: Optional[str]
    is_default: Optional[int]
    created_at: Optional[datetime]

class ApisItem(BaseModel):
    project_key: str
    branch_key: str
    folder_key: Optional[str] = None
    doc_key: str
    doc_name: str
    doc_transfer_protocol: str
    doc_ip: str
    doc_port: str
    doc_path: str
    doc_method: str
    doc_operationId: str
    doc_req_content_type: str
    doc_req_params: str
    doc_req_required: str
    doc_res_status: str
    doc_res_content_type: str
    doc_res_params: str
    doc_res_params: str
    doc_order: int
    doc_desc: str
    type:Optional[str] = ''
    label:Optional[str] = ''

class ApisData(BaseModel):
    project_key: str
    branch_key: str
    folder_key: str
    folder_name: str
    folder_order: int
    type: Optional[str] = ''
    label: Optional[str] = ''
    children: Optional[List[ApisItem]] = None


class ApiDataResponse(BaseModel):
    apis: List[Union[ApisItem, ApisData]]


class AddApiFolderRequest(BaseModel):

    project_key: str
    branch_key: str
    folder_key: str
    folder_name: str


class EditApiFolderRequest(BaseModel):

    folder_key: str
    folder_name: str


class DelApiFolderRequest(BaseModel):
    folder_key: str

class ManageEnvRequest(BaseModel):

    env_key: str
    env_name: str
    env_icon: str
    env_url: str
    env_color: str

class EnvItem(BaseModel):
    env_key: str
    env_name: str
    env_icon: str
    env_url: str
    env_color: str

class ApiEnvResponse(BaseModel):
    envs: List[EnvItem]

class DelEnvRequest(BaseModel):
    env_key: str


class ApiDebugRequest(BaseModel):

    env_key: str
    env_url: str
    doc_method: str
    doc_path: str
    apiHeaderParams: List
    apiParams: List
    apiParamsFdata:List
    apiParamsJson: List
    debug_json_params: str
    req_content_type: str


class ManageApiRequest(BaseModel):

    project_key: str
    branch_key: str
    folder_key: str
    doc_key: str
    doc_name:str
    doc_method: str
    doc_path: str
    doc_desc: str
    apiParams: List
    apiParamsFdata:List
    apiParamsJson: List
    debug_json_params: str
    req_content_type: str
    res_content_type: str
    apiResResult:List
    version: str
    author: str

class DelApiRequest(BaseModel):
    doc_key: str