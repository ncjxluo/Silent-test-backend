# -*- coding: utf-8 -*-
# @Time    : 2026/1/28 16:48
# @Author  : lwc
# @File    : ssh_async_utils.py
# @Description : 操作shell的类

import asyncssh
from typing import Dict, Any, Optional
from asyncssh import SSHClientConnection


class SSHSession:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.conn: Optional[SSHClientConnection] = None
        self.process: Optional[asyncssh.SSHClientProcess] = None  # 添加类型注解
        self.reader = None  # 添加reader引用


    async def connect(self, term_type="xterm", rows=24, cols=80):
        self.conn = await asyncssh.connect(
            self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            known_hosts=None
        )

        self.process = await self.conn.create_process(
            term_type=term_type,
            term_size=(rows, cols)
        )
        self.reader = self.process.stdout


    async def write(self, data: str):
        if self.process and not self.process.stdin.is_closing():
            self.process.stdin.write(data)
            # 添加drain确保数据发送
            await self.process.stdin.drain()

    async def read(self, n=1024):
        try:
            if self.reader:
                # 读取数据，使用at_least=False避免阻塞
                data = await self.reader.read(n)
                return data if data else ""
            return ""
        except Exception as e:
            print(f"SSH read error: {e}")
            return ""

    def resize(self, rows, cols):
        if self.process:
            self.process.change_terminal_size(cols, rows)

    async def close(self):
        if self.process:
            try:
                # 发送退出命令
                self.process.stdin.write("\x03")  # Ctrl+C
                self.process.stdin.close()
                await self.process.wait_closed()
            except:
                pass
        if self.conn:
            self.conn.close()

    async def check_ssh(self) -> dict:
        try:
            async with asyncssh.connect(self.host, port=self.port, username=self.username, password=self.password, known_hosts=None, login_timeout=15) as conn:
                return {"status": True, "resultset": ""}
        except Exception as e:
            return {"status": False, "resultset": str(e)}

    async def run_cmd(self, cmd) -> dict:
        try:
            async with asyncssh.connect(self.host, port=self.port, username=self.username, password=self.password, known_hosts=None, login_timeout=15) as conn:
                result = await conn.run(cmd, check=False)
                return {
                    "status": True,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.exit_status
                }
        except Exception as e:
            return {"status": False, "resultset": str(e)}

    async def get_conn(self)-> SSHClientConnection:
        conn = await asyncssh.connect(self.host, port=self.port, username=self.username, password=self.password, known_hosts=None, login_timeout=15)
        return conn
#     """Paramiko异步封装工具类：极简获取执行结果"""
#     def __init__(
#         self,
#         username: str,
#         password: str,
#         host: str,
#         port: int = 22,
#
#         connect_timeout: int = 5
#     ):
#         self.host = host
#         self.port = port
#         self.username = username
#         self.password = password
#         self.connect_timeout = connect_timeout
#         self.ssh_client = paramiko.SSHClient()
#         self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     # 同步执行函数：内部使用，封装连接+执行+解析
#     def _sync_exec(self, command: str, exec_timeout: int) -> Dict[str, Any]:
#         """同步执行命令并解析结果（内部方法，提交到线程池）"""
#         try:
#             # 建立连接（若未连接）
#             if not self.ssh_client.get_transport() or not self.ssh_client.get_transport().is_active():
#                 self.ssh_client.connect(
#                     self.host,
#                     self.port,
#                     self.username,
#                     self.password,
#                     timeout=self.connect_timeout,
#                     look_for_keys=False,
#                     allow_agent=False
#                 )
#             # 执行命令
#             stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=exec_timeout)
#             # 解析结果：统一解码+去空白
#             output = stdout.read().decode("utf-8", errors="ignore").strip()
#             error = stderr.read().decode("utf-8", errors="ignore").strip()
#             # 结果返回
#             if error:
#                 return {"success": True, "output": output, "error": error, "msg": "命令执行成功，有错误输出"}
#             return {"success": True, "output": output, "error": error, "msg": "命令执行成功"}
#         except Exception as e:
#             return {"success": False, "output": "", "error": "", "msg": f"执行失败：{str(e)}"}
#
#     async def connect(self) -> None:
#         """异步建立连接（单独调用，用于仅测试连接）"""
#         loop = asyncio.get_running_loop()
#         await loop.run_in_executor(
#             THREAD_POOL,
#             self.ssh_client.connect,
#             self.host,
#             self.port,
#             self.username,
#             self.password,
#             None,
#             False,
#             False,
#             self.connect_timeout
#         )
#
#     async def exec_command(self, command: str, exec_timeout: int = 10) -> Dict[str, Any]:
#         """
#         异步执行命令：一键获取解析后的结果（核心方法，推荐使用）
#         :param command: 要执行的命令
#         :param exec_timeout: 命令执行超时时间
#         :return: 解析后的字典结果
#         """
#         loop = asyncio.get_running_loop()
#         # 将同步执行函数提交到线程池，返回异步结果
#         res = await loop.run_in_executor(
#             THREAD_POOL,
#             self._sync_exec,
#             command,
#             exec_timeout
#         )
#         return res
#
#     def close(self) -> None:
#         """关闭连接"""
#         if self.ssh_client.get_transport() and self.ssh_client.get_transport().is_active():
#             self.ssh_client.close()
#
# # 异步上下文管理器：自动连接+自动关闭（推荐，无需手动管理连接）
# async def create_ssh_client(
#         username: str,
#         password: str,
#     host: str,
#     port: int = 22,
#
#     connect_timeout: int = 5
# ) -> AsyncSSHClient:
#     client = AsyncSSHClient(host, port, username, password, connect_timeout)
#     try:
#         await client.connect()
#         yield client
#     finally:
#         client.close()
#
