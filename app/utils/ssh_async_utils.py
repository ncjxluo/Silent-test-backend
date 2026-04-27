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