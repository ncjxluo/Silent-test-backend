# -*- coding: utf-8 -*-
# @Time    : 2026/3/6 10:24
# @Author  : lwc
# @File    : deploy_strategy_schema.py
# @Description :

from pydantic import BaseModel
from typing import Optional,Dict,List,Union
from datetime import datetime
from app.schemas.base_res_model import BaseResponseModel


class DeployStrategyRequest(BaseModel):

    strategy_name: str
    process_mode: str
    app_product_line: str
    virtual_key: str
    app_config: str
    deployment_path: str
    deployment_config_content: str
    message_config: str

class EditDeployStrategyRequest(BaseModel):

    strategy_key: str
    strategy_name: str
    process_mode: str
    app_product_line: str
    virtual_key: str
    app_config: str
    deployment_path: str
    deployment_config_content: str
    message_config: str

class DeployStrategyItem(BaseResponseModel):

    strategy_key: str
    strategy_name: str
    process_mode: str
    app_product_line: str
    virtual_key: str
    virtual_name: str
    app_config: str
    deployment_path: str
    deployment_config_content: str
    message_config: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class DeployStrategyResponse(BaseModel):

    total_count: int
    deploy_strategys: List[DeployStrategyItem]

class DelDeployStrategyRequest(BaseModel):

    strategy_key: str