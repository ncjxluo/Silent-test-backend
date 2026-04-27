# -*- coding: utf-8 -*-
# @Time    : 2026/3/30 15:56
# @Author  : lwc
# @File    : api_testcase.py
# @Description :

from fastapi import APIRouter, Depends
from typing import List
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.schemas.ifaceauto.api_testcase_schema import (
    AddApiCaseProjectRequest,
    ApiCaseProjectResponse,
    EditApiCaseProjectRequest,
    DelApiCaseProjectRequest,
    AddApiCaseBranchRequest,
    ApiCaseBranchResponse,
    TestCaseDataResponse,
    AddApiCaseFolderRequest,
    EditApiCaseFolderRequest,
    DelApiCaseFolderRequest,
    ComponentsItem,
    ApiTestCaseRequest,
    DebugTestCaseRequest,
    TaskTestCaseRequest,
    DelTestCaseRequest,
    FoldersResponse
)
from app.services.ifaceauto.api_testcase_service import ApiTestCaseService

router = APIRouter()

@router.post("/add_api_case_project",response_model=ApiResponse)
async def add_api_case_project(obj:AddApiCaseProjectRequest, current_user_key: str = Depends(get_current_user)):
    print(obj)
    res = await ApiTestCaseService.add_api_case_project(obj.case_project_name, obj.case_project_name, current_user_key)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_case_projects",response_model=ApiResponse[List[ApiCaseProjectResponse]])
async def get_api_case_projects(current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.get_api_case_projects()
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_api_case_project",response_model=ApiResponse)
async def edit_api_case_project(obj:EditApiCaseProjectRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.edit_api_case_project(obj.case_project_key, obj.case_project_name, obj.case_project_desc)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_api_case_project",response_model=ApiResponse)
async def del_api_case_project(obj:DelApiCaseProjectRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.del_api_case_project(obj.case_project_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/add_api_case_branch",response_model=ApiResponse)
async def add_api_case_branch(obj:AddApiCaseBranchRequest, current_user_key: str = Depends(get_current_user)):
    print('积分')
    res = await ApiTestCaseService.add_api_case_branch(obj.case_project_key, obj.case_branch_name, obj.case_branch_source)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_case_branchs",response_model=ApiResponse[List[ApiCaseBranchResponse]])
async def get_api_case_branchs(case_project_key:str=None, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.get_api_case_branchs(case_project_key)
    return ApiResponse(data=res) # type: ignore


@router.get("/get_api_testcases",response_model=ApiResponse[TestCaseDataResponse])
async def get_api_testcases(case_project_key:str=None, case_branch_key:str=None, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.get_testcases(case_project_key, case_branch_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/add_api_case_folder",response_model=ApiResponse)
async def add_api_case_folder(obj:AddApiCaseFolderRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.add_api_case_folder(obj.case_project_key, obj.case_branch_key, obj.case_folder_key, obj.case_folder_name)
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_api_case_folder",response_model=ApiResponse)
async def edit_api_case_folder(obj:EditApiCaseFolderRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.edit_api_case_folder(obj.case_folder_key, obj.case_folder_name)
    return ApiResponse(data=res) # type: ignore

@router.post("/del_api_case_folder",response_model=ApiResponse)
async def del_api_case_folder(obj:DelApiCaseFolderRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.del_api_case_folder(obj.case_folder_key)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_case_folder",response_model=ApiResponse[List[FoldersResponse]])
async def get_api_case_folder(case_project_key:str=None, case_branch_key:str=None, current_user_key: str = Depends(get_current_user)):

    res = await ApiTestCaseService.get_api_case_folder(case_project_key, case_branch_key)
    return ApiResponse(data=res) # type: ignore

@router.get("/get_api_components",response_model=ApiResponse[List[ComponentsItem]])
async def get_api_components(current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.get_api_components()
    return ApiResponse(data=res) # type: ignore


@router.post("/manage_api_testcase",response_model=ApiResponse)
async def manage_api_testcase(obj:ApiTestCaseRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.manage_api_testcase(obj.case_project_key, obj.case_branch_key, obj.case_folder_key,
                                                       obj.case_key, obj.case_name, obj.case_content, obj.case_struct_data)
    return ApiResponse(data=res) # type: ignore


@router.post("/debug_api_testcase",response_model=ApiResponse)
async def debug_api_testcase(obj:DebugTestCaseRequest, current_user_key: str = Depends(get_current_user)):
    print(obj)
    res = await ApiTestCaseService.debug_api_testcase(obj.agent_key, obj.case_name, obj.case_content, current_user_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/send_case_task",response_model=ApiResponse)
async def send_case_task(obj:TaskTestCaseRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.send_case_task(obj.agent_key, obj.task_name, obj.task_cases, obj.twins_flame, current_user_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/del_api_testcase",response_model=ApiResponse)
async def del_api_testcase(obj:DelTestCaseRequest, current_user_key: str = Depends(get_current_user)):
    res = await ApiTestCaseService.del_api_testcase(obj.case_project_key, obj.case_branch_key, obj.case_key)
    return ApiResponse(data=res) # type: ignore