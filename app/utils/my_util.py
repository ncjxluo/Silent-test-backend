# -*- coding: utf-8 -*-
# @Time    : 2025/11/17 16:05
# @Author  : lwc
# @File    : my_util.py
# @Description : 一些辅助函数的设置
from typing import List,Dict,Any
import ast
import json

def is_empty(value):
    """判断值是否为 None 或空字符串"""
    return value is None or value == ""


def sort_filed_recursive(nodes: List[Dict[str, Any]], sorted_row:str, sorted_field:str) -> List[Dict[str, Any]]:
    """
    安装字典中的某个列和字段进行排序
    :param nodes:
    :param sorted_row:
    :param sorted_field:
    :return:
    """
    for node in nodes:
        # 对当前节点的子节点排序：按 group_order 转为整数后排序（避免字符串排序异常，如 "10" < "2"）
        node[sorted_row] = sorted(
            node[sorted_row],
            key=lambda x: int(x.get(sorted_field))  # 转为int排序，适配数字字符串
        )
        # 递归排序子节点的子节点（支持无限多层级）
        sort_filed_recursive(node[sorted_row], sorted_row, sorted_field)
    return nodes


def parse_kv(separator: str,text: str) -> dict[str, str]:
    """
    将行拆分为字典
    :param separator: 分隔符
    :param text: 一个包含 xxx 分隔符 xxx 这样的带有格式的字符串
    :return: 拆分后的字典
    """
    res_dic = {}
    for line in text.splitlines():
        if separator not in line:
            continue
        key, value = line.split(separator, 1)
        res_dic[key.strip()] = value.strip()
    return res_dic


def my_formatting(v: str) -> str:
    """
    格式化一个值
    :param v: 值
    :return: 格式化的值
    """
    if isinstance(v,int):
        return str(v)
    else:
        v = v.replace('\n', '')
        v = v.replace('"', '')
        v = v.replace("'", '')
        return v.strip()


# def my_literal_eval(v_type:str, val:str):
#     if val is None or val == "":
#         return val
#     try:
#         if v_type in ["integer", "long", "number"]:
#             return int(val)
#         elif v_type in ["object", "array"]:
#             if "${" in val and "}" in val:
#                 return val.strip('"')
#             else:
#                 return json.loads(val)
#         elif v_type == "boolean":
#             return ast.literal_eval(val)
#         else:
#             return val
#     except:
#         return val

def normalize_example(value, type_):
    if value is None:
        return None
    if type_ == "object":
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                return {}
        return value
    elif type_ == "array":
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                return []
        return value
    else:
        return value