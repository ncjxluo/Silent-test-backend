# -*- coding: utf-8 -*-
# @Time    : 2025/12/4 18:32
# @Author  : lwc
# @File    : depts.py
# @Description :

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.base import ApiResponse
from app.services.systems.depts_services import DeptService
from app.schemas.systems.depts import DeptRequest,DeptResponse,DelDeptRequest,EditDeptRequest


router = APIRouter()

@router.get("/get_depts",response_model=ApiResponse[DeptResponse])
async def get_depts(current_user_key: str = Depends(get_current_user), current_page:int = 1, current_count:int = 30):
    dept_res = await DeptService.get_all_dept(current_page, current_count)
    return ApiResponse(data=dept_res) # type: ignore


@router.post("/addition_dept",response_model=ApiResponse)
async def addition_dept(dept:DeptRequest, current_user_key: str = Depends(get_current_user)):
    res = await DeptService.addition_dept(dept.dept_name, dept.status)
    return ApiResponse(data=res) # type: ignore


@router.post("/del_dept",response_model=ApiResponse)
async def del_dept(dept:DelDeptRequest, current_user_key: str = Depends(get_current_user)):
    res = await DeptService.del_dept(dept.dept_key)
    return ApiResponse(data=res) # type: ignore


@router.post("/edit_dept",response_model=ApiResponse)
async def edit_dept(dept:EditDeptRequest, current_user_key: str = Depends(get_current_user)):
    # res = await DeptService.del_dept(dept.dept_key)
    res = await DeptService.edit_dept(dept.dept_key, dept.dept_name, dept.status)
    print(dept)
    return ApiResponse(data=res) # type: ignore