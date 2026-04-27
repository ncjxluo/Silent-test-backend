# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 14:23
# @Author  : lwc
# @File    : api_manager.py
# @Description : 接口文档管理的接口
import json

from fastapi import APIRouter, Depends
from typing import List
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.schemas.ifaceauto.api_manager_schema import (
    AddApiProjectRequest,
    EditApiProjectRequest,
    DelApiProjectRequest,
    ApiProjectResponse,
    AddApiBranchRequest,
    EditApiBranchRequest,
    DelApiBranchRequest,
    ApiBranchResponse,
    AddApiFolderRequest,
    EditApiFolderRequest,
    DelApiFolderRequest,
    ApiDataResponse,
    ManageEnvRequest,
    ApiEnvResponse,
    DelEnvRequest,
    ApiDebugRequest,
    ManageApiRequest,
    DelApiRequest
)
from app.services.ifaceauto.api_manager_service import ApiManagerService

router = APIRouter()

@router.post("/add_api_project",response_model=ApiResponse)
async def add_api_project(obj:AddApiProjectRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.add_api_project(obj.project_name,obj.project_desc,current_user_key)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_projects",response_model=ApiResponse[List[ApiProjectResponse]])
async def get_api_projects(current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.get_api_projects()
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_api_project",response_model=ApiResponse)
async def edit_api_project(obj:EditApiProjectRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.edit_api_project(obj.project_key,obj.project_name,obj.project_desc)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_api_project",response_model=ApiResponse)
async def del_api_project(obj:DelApiProjectRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.del_api_project(obj.project_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/add_api_branch",response_model=ApiResponse)
async def add_api_branch(obj:AddApiBranchRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.add_api_branch(obj.project_key, obj.branch_name, obj.branch_source)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_branchs",response_model=ApiResponse[List[ApiBranchResponse]])
async def get_api_branchs(project_key:str=None, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.get_api_branchs(project_key)
    return ApiResponse(data=res) # type: ignore


@router.get("/get_apis",response_model=ApiResponse[ApiDataResponse])
async def get_apis(project_key:str=None, branch_key:str=None, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.get_apis(project_key, branch_key)
    return ApiResponse(data=res) # type: ignore


# @router.post("/edit_api_branch",response_model=ApiResponse)
# async def edit_api_branch(obj:EditApiBranchRequest, current_user_key: str = Depends(get_current_user)):
#     res = await ApiManagerService.edit_api_branch(obj.branch_key, obj.branch_name, obj.branch_order)
#     return ApiResponse(data=res) # type: ignore
#
# @router.post("/del_api_branch",response_model=ApiResponse)
# async def del_api_branch(obj:DelApiBranchRequest, current_user_key: str = Depends(get_current_user)):
#     res = await ApiManagerService.del_api_branch(obj.branch_key)
#     return ApiResponse(data=res) # type: ignore



@router.post("/add_api_folder",response_model=ApiResponse)
async def add_api_folder(obj:AddApiFolderRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.add_api_folder(obj.project_key, obj.branch_key, obj.folder_key, obj.folder_name)
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_api_folder",response_model=ApiResponse)
async def edit_api_folder(obj:EditApiFolderRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.edit_api_folder(obj.folder_key, obj.folder_name)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_api_folder",response_model=ApiResponse)
async def del_api_folder(obj:DelApiFolderRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.del_api_folder(obj.folder_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/manage_api_env",response_model=ApiResponse)
async def manage_api_env(obj:ManageEnvRequest, current_user_key: str = Depends(get_current_user)):
    print(obj)
    res = await ApiManagerService.manage_api_env(obj.env_key, obj.env_name, obj.env_icon, obj.env_url, obj.env_color)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_envs",response_model=ApiResponse[ApiEnvResponse])
async def get_api_envs(current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.get_api_env()
    return ApiResponse(data=res) # type: ignore

@router.post("/del_api_env",response_model=ApiResponse)
async def del_api_env(obj:DelEnvRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.del_api_env(obj.env_key)
    return ApiResponse(data=res) # type: ignore

@router.post("/api_debug",response_model=ApiResponse)
async def api_debug(obj:ApiDebugRequest, current_user_key: str = Depends(get_current_user)):
    print(f"调试的所有参数{obj}")
    params = None
    if obj.doc_method == "GET":
        params = { item.get("name"):item.get("example") for item in obj.apiParams}
    else:
        if obj.req_content_type == 'json':
            params = json.loads(obj.debug_json_params)
        elif obj.req_content_type == 'form_data':
            params = { item.get("name"):item.get("example") for item in obj.apiParamsFdata}
        else:
            params = None
    res = await ApiManagerService.api_debug(obj.env_url, obj.doc_method, obj.doc_path,
                  obj.req_content_type, { item.get("name"):item.get("example") for item in obj.apiHeaderParams }, params)
    print(f"res{res}")
    return ApiResponse(data=res) # type: ignore

@router.post("/manage_api",response_model=ApiResponse)
async def manage_api(obj:ManageApiRequest, current_user_key: str = Depends(get_current_user)):
    print(obj)
    res = await ApiManagerService.manage_api(obj.project_key, obj.branch_key, obj.folder_key, obj.doc_key,
        obj.doc_name, obj.doc_method, obj.doc_path, obj.doc_desc,
        obj.apiParams, obj.apiParamsFdata, obj.apiParamsJson, obj.debug_json_params,
        obj.req_content_type, obj.res_content_type, obj.apiResResult, obj.version, obj.author
    )
    return ApiResponse(data=res) # type: ignore


@router.post("/del_api",response_model=ApiResponse)
async def del_api_env(obj:DelApiRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiManagerService.del_api(obj.doc_key)
    return ApiResponse(data=res) # type: ignore