# -*- coding: utf-8 -*-
# @Time    : 2025/10/30 15:41
# @Author  : lwc
# @File    : helper.py
# @Description : 帮助类

import os
import json


def get_rootpath() -> str:
    """
    获取根路径
    :return: 返回获取运行文件的上级路径
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_realpath(path: str) -> str:
    """
    获取真实路径
    :param path: 传入路径
    :return: 返回拼接后的路径
    """
    return str(os.path.join(get_rootpath(), *filter(None, path.split("/"))))



def get_config() -> dict:
    """
    获取配置信息
    :return: 配置信息字典对象
    """
    config_path = get_realpath("config/config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f).get("str-config")