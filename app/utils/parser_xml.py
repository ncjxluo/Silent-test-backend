# -*- coding: utf-8 -*-
# @Time    : 2026/4/6 17:39
# @Author  : lwc
# @File    : parser_xml.py
# @Description :

import xml.etree.ElementTree as ET

def parse_test_plan_xml(xml_str: str):
    """
    解析前端传来的 JMeter XML
    提取所有 HttpSampler 及其接口配置
    """
    root = ET.fromstring(xml_str)
    http_samplers = []

    nodes_to_visit = [root]

    while nodes_to_visit:
        node = nodes_to_visit.pop(0)

        # 找到 HttpSampler 就解析
        if node.tag == "HttpSampler":
            sampler_name = node.get("name", "")
            config = {
                "sampler_name": sampler_name,
                "api_project": None,
                "api_branch": None,
                "env": None,
                "interface_name": None,
            }

            # 解析 httpProp
            for prop in node.findall("httpProp"):
                name = prop.get("name", "")
                value = prop.text.strip() if prop.text else ""

                if name == "h:env":
                    config["env"] = value
                elif name == "api_project":
                    config["api_project"] = value
                elif name == "api_branch":
                    config["api_branch"] = value
                elif name == "h:interface":
                    config["interface_name"] = value

            http_samplers.append(config)

        # 把子节点加入队列（代替递归）
        for child in node:
            nodes_to_visit.append(child)

    return http_samplers