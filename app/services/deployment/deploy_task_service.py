# -*- coding: utf-8 -*-
# @Time    : 2026/3/14 18:08
# @Author  : lwc
# @File    : deploy_task_service.py
# @Description : 部署执行的业务操作
import asyncio
import json
from typing import List
import os
import re
from string import Template
from app.utils.my_util import is_empty
from app.utils.ssh_async_utils import SSHSession
from app.dao.systems.str_log_dao import StrLogDao
from app.dao.deployment.app_config_dao import AppconfigDao
from app.dao.message_center.message_dao import MessageDao
from app.dao.host_management.server_setting_dao import ServerSettingDao
import uuid
from app.utils.send_message import send_mes

class DeployTaskService:

    @staticmethod
    async def get_deploy_result(task_id:str) -> dict:
        sign = '0'
        logs = await StrLogDao.get_deploy_log(task_id)
        print(logs)
        if all(v.get("status") == "complete" for v in logs) and all("silent test run deploy task success" in v.get("content") or "silent test run deploy task fail" in v.get("content") for v in logs):
            sign = '1'
        return {"sign": sign, "logs": logs}


    @staticmethod
    async def create_deploy_task(strategy_key: str,strategy_name: str,process_mode: str,app_product_line: str,
        virtual_key: str,virtual_name: str,app_config: List,deployment_path: str,deployment_config_content: dict,
        message_config: dict, deploy_tool_internal_path:str, current_user_key:str, deploy_cmd:str) -> dict:
        """
        部署前的准备工作
        :param strategy_key:
        :param strategy_name:
        :param process_mode:
        :param app_product_line:
        :param virtual_key:
        :param virtual_name:
        :param app_config:
        :param deployment_path:
        :param deployment_config_content:
        :param message_config:
        :param deploy_tool_internal_path:
        :param current_user_key:
        :param deploy_cmd:
        :return:
        """
        try:
            task_id = str(uuid.uuid4())
            deploy_apps = await AppconfigDao.get_deploy_app([ item.get("app_id") for item in app_config])
            print(f"deploy_apps${deploy_apps}")
            message_channel = await MessageDao.get_message(message_config.get("message_key"))
            vm = await ServerSettingDao.get_virtual_machine_info([virtual_key])
            # ------------------------------------------------------------------------------------
            message_config["mes_url"] = message_channel[0].mes_url
            map1 = {item["app_id"]: item for item in app_config}
            print(f"map1{map1}")
            map2 = {item1["id"]: item1 for item1 in [item.model_dump() for item in deploy_apps] }
            print(f"map2{map2}")
            deploy_tasks = []
            for key in map1:
                merged = {**map1[key], **map2.get(key, {})}
                deploy_tasks.append(merged)

            await StrLogDao.record_deploy_log(
                task_id,
                current_user_key,
                deploy_tasks,
                "0",
                virtual_name,
                app_product_line
            )
            print(f"部署的应用${deploy_apps}")
            asyncio.create_task(DeployTaskService.exec_deploy_task(
                task_id, process_mode, deployment_path, deployment_config_content, deploy_tool_internal_path,
                [ item.model_dump() for item in vm][0],
                message_config,
                deploy_tasks,
                app_product_line,
                virtual_name,
                deploy_cmd
            ))
            return {"msg": "部署开始", "task_id": task_id}
        except Exception as e:
            print(e)
            return {"msg": "部署下发失败", "task_id": 0}


    @staticmethod
    async def exec_deploy_task(task_id:str, process_mode: str, deployment_path: str, deployment_config_content: dict, deploy_tool_internal_path: str,
                               virtual_machine: dict, message_config: dict, apps: list, app_product_line:str, virtual_name:str, deploy_cmd:str):
        """
        开始部署
        :param task_id: 任务编号
        :param process_mode: 处理模式
        :param deployment_path: 部署工具所在机器的路径
        :param deployment_config_content: 部署工具的配置文件
        :param deploy_tool_internal_path: 部署工具内部的路径，deployment_config_content + deploy_tool_internal_path + 应用名字,便成为了全路径
        :param virtual_machine: 要部署的虚机的信息
        :param message_config: 消息通道的设置
        :param apps: 本次要部署的应用
        :param app_product_line: 产品线
        :param virtual_name: 虚机名字
        :param deploy_cmd: 最后要执行的命令
        :return: 无返回值
        """
        try:

            if message_config.get("timing_sending") in ["部署前", "部署前后"]:
                send_content = DeployTaskService.build_params_dict(message_config.get("before_content"),apps,app_product_line,virtual_name)
                print(f"部署前发送的内容（验证）:{send_content}")
                await send_mes(message_config.get("mes_url"), send_content)
            ssh_session = SSHSession(virtual_machine.get("virtual_ip_address"), virtual_machine.get("virtual_ip_port"),
                                     virtual_machine.get("virtual_username"), virtual_machine.get("virtual_password"))
            ssh_client = await ssh_session.get_conn()
            c_path = os.path.join(deployment_path,'cluster.json')
            cmd = f"""cat > {c_path} << 'EOF' 
{json.dumps(deployment_config_content,ensure_ascii=False,indent=2)} 
EOF"""
            await ssh_client.run(cmd)
            if process_mode == '串行':
                for app in apps:
                    await DeployTaskService.deploy(task_id, app, deployment_path, deploy_tool_internal_path, ssh_client)
            else:
                tasks = [
                    DeployTaskService.deploy(task_id, app, deployment_path, deploy_tool_internal_path, ssh_client) for app in apps
                ]
                await asyncio.gather(*tasks)
            if not is_empty(deploy_cmd):
                print("最终的命令执行了")
                await ssh_client.run(deploy_cmd)
            if message_config.get("timing_sending") in ["部署后", "部署前后"]:
                send_content = DeployTaskService.build_params_dict(message_config.get("end_content"), apps, app_product_line, virtual_name)
                print(f"部署后发送的内容（验证）:{send_content}")
                await send_mes(message_config.get("mes_url"), send_content)
        except Exception as e:
            print(e)


    @staticmethod
    async def deploy(task_id:str, app:dict, deployment_path:str, deploy_tool_internal_path:str, ssh_client):
        try:
            # 构建删除原有包的命令
            rm_cmd = f"rm -rf {os.path.join(deployment_path, deploy_tool_internal_path, app.get('app_deploy_name'), 'package', app.get('app_before_name'))}*{app.get('app_end_name')}"
            print(f"删除命令{rm_cmd}")
            await ssh_client.run(rm_cmd)
            # 构建名字
            f_name = f"{app.get('app_before_name')}{app.get('version')}{app.get('app_end_name')}"
            if app.get("app_download_type") == 'ftp':
                down_path = f"{app.get('app_download_type')}://{app.get('app_download_ip')}:{app.get('app_download_port')}/{os.path.join(app.get('app_download_path'), f_name)}"
                save_path = f"{os.path.join(deployment_path, deploy_tool_internal_path, app.get('app_deploy_name'), 'package', f_name)}"
                down_cmd = f"curl -sI --user {app.get('app_download_uname')}:{app.get('app_download_passwd')} {down_path} | grep -i Content-Length | awk '{{print $2}}' | tr -d '\\r'"
                cmd = f"curl -s --user {app.get('app_download_uname')}:{app.get('app_download_passwd')} {down_path} -o {save_path}"
            else:
                down_path = f"{app.get('app_download_type')}://{app.get('app_download_ip')}:{app.get('app_download_port')}{os.path.join(app.get('app_download_path') + app.get('version'), f_name)}"
                save_path = f"{os.path.join(deployment_path, deploy_tool_internal_path, app.get('app_deploy_name'), 'package', f_name)}"
                down_cmd = f"curl -sI {down_path} | grep -i Content-Length | awk '{{print $2}}' | tr -d '\\r'"
                cmd = f"curl -s -o {save_path} {down_path}"
            # 构建部署命令
            deploy_cmd = f"cd {deployment_path} && {app.get('exec_cmd')}"
            total_size = await ssh_client.run(down_cmd)
            if is_empty(total_size):
                await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '', f'没有找到{f_name}，部署失败', "1")
                await StrLogDao.set_deploy_log_status(task_id, app.get('app_nickname'), 'complete')
                return ''
            total_size = int(total_size.stdout)
            await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '', f'正在下载{f_name}', "1")
            process = await ssh_client.create_process(cmd)
            last_progress = -1
            while process.exit_status is None:
                try:
                    if total_size > 0:
                        cmd_current = f"stat -c %s {save_path} 2>/dev/null || echo 0"
                        p_cur = await ssh_client.create_process(cmd_current)
                        current_size = await p_cur.stdout.readline()
                        current_size = int(current_size.strip() or 0)
                        progress = int((current_size / total_size) * 100)
                        if progress != last_progress and progress <= 100:
                            await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), str(progress), '', "0")
                            last_progress = progress
                except Exception:
                    pass
                await asyncio.sleep(0.5)
            await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '100', '', "0")
            # 执行部署命令
            process = await ssh_client.create_process(f"{deploy_cmd}")
            async for line in process.stdout:
                await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '', line.strip(), "1")
            if not is_empty(app.get("verify_cmd")):
                process = await ssh_client.create_process(app.get('verify_cmd'))
                async for line in process.stdout:
                    await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '', line.strip(), "1")
            await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '', 'silent test run deploy task success', "1")
            await StrLogDao.set_deploy_log_status(task_id, app.get('app_nickname'), 'complete')

            return ''
        except Exception as e:
            print(e)
            await StrLogDao.append_deploy_log(task_id, app.get('app_nickname'), '',
                                              'silent test run deploy task fail', "1")
            await StrLogDao.set_deploy_log_status(task_id, app.get('app_nickname'), 'complete')
            return ''

    @staticmethod
    def build_params_dict(mes_content: str, apps:list, p_line:str, v_name:str) -> str:
        """
        构建参数字典
        :param mes_content:
        :param apps:
        :param p_line:
        :param v_name:
        :return:
        """
        pattern = r'\$\{([^}]+)\}'
        result = re.findall(pattern, mes_content)
        deploy_dic = {app.get("app_nickname").replace('-','_'):app.get("version") for app in apps}
        p_dic = {}
        for item in result:
            if item == 'app_product_line':
                p_dic[item] = p_line
            elif item == 'virtual_name':
                p_dic[item] = v_name
            else:
                p_dic[item] = deploy_dic.get(item, '')
        content = Template(mes_content).substitute(p_dic)
        return content


