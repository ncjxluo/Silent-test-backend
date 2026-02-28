# -*- coding: utf-8 -*-
# @Time    : 2026/2/28 16:36
# @Author  : lwc
# @File    : manage.py
# @Description :
from pydantic import BaseModel
from app.schemas.base_res_model import BaseResponseModel
from typing import Optional,List
from datetime import datetime


class NoticeResponse(BaseResponseModel):

    notice_title: Optional[str]
    notice_content: Optional[str]
    created_at: Optional[datetime]


class MemoRequest(BaseModel):

    memo_title: Optional[str]
    memo_content: Optional[str]
    memo_level: Optional[str]
    memo_complete: Optional[str]

class DelMemoRequest(BaseModel):

    memo_key: Optional[str]

class EditMemoRequest(BaseModel):

    memo_key: Optional[str]
    memo_complete: Optional[str]


class MemoItemResponse(BaseResponseModel):

    memo_key: Optional[str]
    memo_title: Optional[str]
    memo_content: Optional[str]
    memo_level: Optional[str]
    memo_complete: Optional[str]
    created_at: Optional[datetime]

class MemosResponse(BaseResponseModel):

    total_count: int
    memos: List[MemoItemResponse]