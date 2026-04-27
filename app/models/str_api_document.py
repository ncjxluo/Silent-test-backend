# -*- coding: utf-8 -*-
# @Time    : 2026/3/19 10:34
# @Author  : lwc
# @File    : str_api_document.py
# @Description : 接口文档的表

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
import uuid
from sqlalchemy import SMALLINT


class StrApiDocument(SQLModel, table=True):

    __tablename__ = 'str_api_document'
    # 文档代表接文档

    doc_key:str = Field(max_length=100, primary_key=True, default_factory=lambda: str(uuid.uuid4()), description="文档的uuid")
    project_key: str = Field(max_length=100, index=True, description="项目的uuid")
    folder_key: Optional[str]  = Field(max_length=100, index=True, default=None, description="组的uuid")
    branch_key: str = Field(max_length=100, index=True, description="文档的分支")
    doc_name: str = Field(max_length=50, description="文档的名称,也是标题")
    doc_transfer_protocol:Optional[str] = Field(max_length=50, default='${schema}', description="接口的传输协议")
    doc_ip: Optional[str] = Field(max_length=50, default='${schema_host}', description="接口的ip")
    doc_port: Optional[str] = Field(max_length=50, default='${schema_port}', description="接口的ip")
    doc_path: str = Field(max_length=300, description="文档的请求路径")
    doc_method: str = Field(max_length=10, description="文档的请求方法")
    doc_operationId:str = Field(max_length=500, description="接口的唯一id")
    doc_req_content_type:str = Field(max_length=300, description="请求的编码格式")
    doc_req_params: str = Field(sa_type=TEXT, description="请求的参数")
    doc_req_required: str = Field(sa_type=TEXT, description="必须要传输的参数")
    doc_res_status: str = Field(max_length=300, description="返回的响应状态")
    doc_res_content_type: str = Field(max_length=300, description="返回的编码格式")
    doc_res_params: str = Field(sa_type=TEXT, description="返回的参数")
    doc_res_required: str = Field(sa_type=TEXT, description="必须要返回的参数")
    doc_order: Optional[int] = Field(sa_type=SMALLINT,default=1, description="文档排序")
    doc_desc: str = Field(sa_type=TEXT, description="文档的描述")
    doc_content: str = Field(sa_type=TEXT, description="文档的格式")
    doc_debug_json: Optional[str]  = Field(sa_type=TEXT, description="文档调试时候,json格式的存储")
    is_delete: int = Field(sa_type=SMALLINT, default=0, description="是否删除,1=是 0=否")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())