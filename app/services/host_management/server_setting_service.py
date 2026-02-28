# -*- coding: utf-8 -*-
# @Time    : 2026/1/21 16:45
# @Author  : lwc
# @File    : server_setting_service.py
# @Description :
import uuid

from sqlalchemy.orm.sync import update

from app.models.str_virtual_machine import StrVirtualMachine
from app.utils.my_util import sort_filed_recursive
from typing import List
from app.dao.host_management.server_setting_dao import ServerSettingDao
from app.utils.ssh_async_utils import SSHSession
from app.utils.my_util import parse_kv,my_formatting
import math
import json

class ServerSettingService:

    @staticmethod
    async def add_server_group(group_key:str, parent_key:str, group_name:str, group_type:str, group_order:int) -> dict:
        """
        增加服务器分组
        :param group_key: 分组的key
        :param parent_key: 分组父级的key
        :param group_name: 分组的名字
        :param group_type: 分组的类型
        :param group_order: 分组的排序
        :return: 返回增加成功or失败的一个字典
        """
        if group_key == '0' or group_key == '-1':
            group_key = str(uuid.uuid4())
            data = await ServerSettingDao.add_server_group(group_key, parent_key, group_name, group_type, str(group_order))
        else:
            data = await ServerSettingDao.update_server_group_name(group_key, group_name)
        return data

    @staticmethod
    async def del_server_group(group_key: str) -> dict:
        """
        删除服务器分组
        :param group_key: 分组的key
        :return: 返回增加成功or失败的一个字典
        """
        data = await ServerSettingDao.del_server_group(group_key)
        return data

    @staticmethod
    async def get_server_group() -> list:
        """
        获取服务器分组
        :return:
        """
        data = await ServerSettingDao.get_server_group()
        # 创建一个存储每个节点的身份库，键是每一行的group——key，值就是这个字典
        node_card_db = {}
        for group in data:
            group_dict = group.dict()
            group_dict["children"] = []
            node_card_db[group.group_key] = group_dict
        # print(node_card_db)
        # 创建一个列表，用于存储最终的结构
        root_nodes = []
        for group_dict in node_card_db.values():
            # 这里要获取身份库中，存储值中的父节点的key
            parent_key = group_dict.get("parent_key")
            if parent_key == "0":
                # 如果 父节点的key是0，说明它就是一级分组，直接加入最终的列表
                root_nodes.append(group_dict)
            else:
                # 如果它不是一级节点，则 判断下，是否在身份库中（避免测试数据报错）
                if parent_key in node_card_db:
                    # 如果父节点能够找到，说明要挂到这个节点的children中
                    node_card_db.get(parent_key)["children"].append(group_dict)
        # print(root_nodes)
        # 这里要对存储中的一级节点排序
        root_nodes = sorted(root_nodes, key=lambda x: int(x.get("group_order")))
        root_nodes = sort_filed_recursive(root_nodes, 'children', 'group_order')
        # print(root_nodes)
        return root_nodes

    @staticmethod
    async def add_virtual_machine(group_key: str, virtual_name:str, virtual_env:str, virtual_ip_address:str,
             virtual_ip_port:str, virtual_username:str, virtual_password:str, description:str) -> dict:
        """
        新增虚拟机
        :param group_key: 分组的key
        :param virtual_name: 虚机的名字
        :param virtual_env: 虚机的环境标签
        :param virtual_ip_address: 虚机的ip地址
        :param virtual_ip_port: 虚机的端口号
        :param virtual_username: 虚机的用户名
        :param virtual_password: 虚机的密码
        :param description: 虚机的描述备注
        :return: 返回增加成功or失败的一个字典
        """
        vm_key = str(uuid.uuid4())
        data = await ServerSettingDao.add_virtual_machine(
            group_key, vm_key, virtual_name, virtual_env,
            virtual_ip_address, virtual_ip_port, virtual_username, virtual_password,
            description)
        return data

    @staticmethod
    async def edit_virtual_machine(group_key: str, virtual_key:str, virtual_name:str, virtual_env:str, virtual_ip_address:str,
             virtual_ip_port:str, virtual_username:str, virtual_password:str, description:str) -> dict:
        """
        编辑服务器分组
        :param group_key: 分组的key
        :param virtual_key: 虚机的key
        :param virtual_name: 虚机的名字
        :param virtual_env: 虚机的环境标签
        :param virtual_ip_address: 虚机的ip地址
        :param virtual_ip_port: 虚机的端口号
        :param virtual_username: 虚机的用户名
        :param virtual_password: 虚机的密码
        :param description: 虚机的描述备注
        :return: 返回增加成功or失败的一个字典
        """

        data = await ServerSettingDao.edit_virtual_machine(
            group_key, virtual_key, virtual_name, virtual_env,
            virtual_ip_address, virtual_ip_port, virtual_username, virtual_password,
            description)
        return data


    @staticmethod
    async def get_virtual_machine(group_key:str, fuzzy_search:str, current_page, current_count) -> dict:
        """
        获取虚拟机的方法
        :param group_key:
        :param fuzzy_search:
        :param current_page:
        :param current_count:
        :return:
        """
        data = await ServerSettingDao.get_virtual_machine(group_key, fuzzy_search, current_page, current_count)
        count = await ServerSettingDao.get_virtual_machine_count(group_key, fuzzy_search)
        return {"total_count": count[0], "virtual_machines": data}


    @staticmethod
    async def verify_virtual_machine(virtual_keys: List[str]) -> dict:
        """
        测试虚机的连通性，并获取基础配置
        :param virtual_keys:
        :return:
        """
        vms = await ServerSettingDao.get_virtual_machine_info(virtual_keys)
        v_res = []
        machine_info = {}
        for vm in vms:
            print(
                f"开始测试虚机：{vm.virtual_key}，IP：{vm.virtual_ip_address}，端口：{vm.virtual_ip_port}，用户名：{vm.virtual_username}")
            ssh_session = SSHSession(vm.virtual_ip_address, vm.virtual_ip_port, vm.virtual_username, vm.virtual_password)
            check_res = await ssh_session.check_ssh()
            if check_res.get("status") is True:
                v_res.append({
                    f"{vm.virtual_ip_address}": "可连接"
                })
                os_release = "获取失败"
                cpu_count = "获取失败"
                men_total = "获取失败"
                disk_info = "获取失败"
                ssh_client = None
                try:
                    ssh_client = await ssh_session.get_conn()
                    res = await ssh_client.run("cat /etc/os-release | grep PRETTY_NAME")
                    os_info = parse_kv("=",res.stdout)
                    if "PRETTY_NAME" in os_info:
                        os_release = os_info.get("PRETTY_NAME")
                    res = await ssh_client.run("nproc")
                    cpu_count = res.stdout
                    res = await ssh_client.run("cat /proc/meminfo | grep MemTotal")
                    men_info = parse_kv(":",res.stdout)
                    print(men_info)
                    if "MemTotal" in men_info:
                        men_total = math.ceil(float(men_info.get("MemTotal").replace('kB', '').strip()) / 1024 / 1024)
                    res = await ssh_client.run("""lsblk -b -d -n -o NAME,SIZE | grep -E '^sd|^vd|^hd|^nvme' | awk '!seen[$1]++ {sum+=$2} END {printf "%.1fG\n", sum/1024/1024/1024}'""")
                    disk_info = res.stdout
                except Exception as e:
                    print()
                finally:
                    if ssh_client is not None:
                        ssh_client.close()
                        await ssh_client.wait_closed()
                machine_info["系统发行版"] = my_formatting(os_release)
                machine_info["cpu(核心数)"] = my_formatting(cpu_count)
                machine_info["内存"] = my_formatting(men_total)
                machine_info["磁盘"] = my_formatting(disk_info)
                await ServerSettingDao.verify_virtual_machine_info(vm.virtual_key, "可连接", json.dumps(machine_info,ensure_ascii=False))
            else:
                v_res.append({
                    f"{vm.virtual_ip_address}": f"无法连接:{check_res.get('resultset')}"
                })
                await ServerSettingDao.verify_virtual_machine_info(vm.virtual_key, "无法连接","")
        return {"result": v_res}

    @staticmethod
    async def get_virtual_machine_all_search(fuzzy_search:str, current_page, current_count) -> dict:
        """
        获取虚拟机的方法
        :param fuzzy_search:
        :param current_page:
        :param current_count:
        :return:
        """
        data = await ServerSettingDao.get_virtual_machine_all_search(fuzzy_search, current_page, current_count)
        return {"virtual_machines": data}


    @staticmethod
    async def del_virtual_machine(virtual_key: str) -> dict:
        """
        删除虚拟机
        :param virtual_key: 虚机的key
        :return: 返回增加成功or失败的一个字典
        """
        data = await ServerSettingDao.del_virtual_machine(virtual_key)
        return data