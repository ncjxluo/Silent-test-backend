# -*- coding: utf-8 -*-
# @Time    : 2026/3/14 17:40
# @Author  : lwc
# @File    : deploy_task_schema.py
# @Description :

from pydantic import BaseModel
from typing import List,Optional

class DeployStrategyRequest(BaseModel):

    strategy_key: str
    strategy_name: str
    process_mode: str
    app_product_line: str
    virtual_key: str
    virtual_name: str
    app_config: List
    deployment_path: str
    deployment_config_content: str
    message_config: str
    deploy_cmd: str

class DeployLogItem(BaseModel):

    task_id: Optional[str]
    app_name: Optional[str]
    progress: Optional[str]
    content: Optional[str]

class DeployLogResponse(BaseModel):

    sign: str
    logs: List[DeployLogItem]