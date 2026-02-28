# -*- coding: utf-8 -*-
# @Time    : 2026/2/9 14:04
# @Author  : lwc
# @File    : web_sockets.py
# @Description : 连接远端命令

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.host_management.web_socket_service import WebSocketService
from app.utils.ssh_async_utils import SSHSession
import json, base64
import asyncio

router = APIRouter()


@router.websocket("/ws_ssh")
async def ws_ssh(ws: WebSocket):
    await ws.accept()

    v_key = ws.query_params.get("v_key")
    print(f"链接虚机的${v_key}")

    try:
        vm_data = await WebSocketService.get_virtual_machine_info([v_key])
        if not vm_data:
            await ws.send_json({"type": "error", "message": "虚拟机不存在"})
            await ws.close()
            return
        init_msg = await asyncio.wait_for(ws.receive_text(), timeout=5.0)
        init_data = json.loads(init_msg)
        if init_data.get("type") != "init":
            await ws.send_json({"type": "error", "message": "无效的初始化消息"})
            return
        cols = init_data.get("data", {}).get("cols", 80)
        rows = init_data.get("data", {}).get("rows", 24)
        ssh_session = SSHSession(
            vm_data.virtual_ip_address,
            vm_data.virtual_ip_port,
            vm_data.virtual_username,
            vm_data.virtual_password
        )
        await ssh_session.connect(rows=rows, cols=cols)
        await ws.send_json({
            "type": "connection",
            "status": "connected",
            "message": f"Connected to {vm_data.virtual_ip_address}"
        })
        await asyncio.gather(
            ssh_to_ws(ssh_session, ws),
            ws_to_ssh(ws, ssh_session),
            return_exceptions=True
        )
    except Exception as e:
        print(f"SSH连接错误: {e}")
        try:
            await ws.send_json({
                "type": "error",
                "message": f"连接失败: {str(e)}"
            })
        except:
            pass
    finally:
        try:
            await ssh_session.close()
        except:
            pass
        await ws.close()


async def ssh_to_ws(ssh: SSHSession, ws: WebSocket):
    """SSH → WebSocket（修复：正确处理SSH输出）"""
    try:
        while True:
            # 修复：使用SSH session的read方法
            data = await ssh.read(1024)
            if data:
                # 修复：直接发送base64编码的数据
                await ws.send_json({
                    "type": "terminal",
                    "data": base64.b64encode(data.encode('utf-8', errors='ignore')).decode()
                })
            else:
                # 没有数据时稍作等待
                await asyncio.sleep(0.01)
    except Exception as e:
        print(f"ssh_to_ws error: {e}")

async def ws_to_ssh(ws: WebSocket, ssh: SSHSession):
    """WebSocket → SSH（修复：正确解析消息格式）"""
    try:
        while True:
            msg = await ws.receive_text()
            msg_data = json.loads(msg)

            # 修复：根据前端发送的消息类型处理
            if msg_data.get("type") == "terminal":
                # 修复：前端发送的格式可能是{base64: data}或直接data
                if isinstance(msg_data.get("data"), dict) and "base64" in msg_data["data"]:
                    input_data = base64.b64decode(msg_data["data"]["base64"]).decode('utf-8', errors='ignore')
                else:
                    # 直接解码base64字符串
                    input_data = base64.b64decode(msg_data.get("data", "")).decode('utf-8', errors='ignore')

                await ssh.write(input_data)

            elif msg_data.get("type") == "resize":
                rows = msg_data.get("data", {}).get("rows", 24)
                cols = msg_data.get("data", {}).get("cols", 80)
                ssh.resize(rows, cols)

    except WebSocketDisconnect:
        print("客户端断开连接")
    except Exception as e:
        print(f"ws_to_ssh error: {e}")
    # init_msg = await ws.receive_text()
    # init_data = json.loads(init_msg)
    # cols = init_data.get("cols", 80)
    # rows = init_data.get("rows", 24)
    # ssh_session = SSHSession(vm_data.virtual_ip_address, vm_data.virtual_ip_port, vm_data.virtual_username, vm_data.virtual_password)
    # await ssh_session.connect(rows=rows,cols=cols)

    # 后端循环读取 SSH 输出并发送给前端
    # try:
    #     while True:
    #         output = await ssh_session.read(1024)
    #         print(output)
    #         if output:
    #             await ws.send_json({
    #                 "type": "terminal",
    #                 "data": base64.b64encode(output.encode()).decode()
    #             })
    #         # 检查前端输入
    #         try:
    #             msg = await ws.receive_text()
    #             print(msg)
    #             msg_data = json.loads(msg)
    #             if msg_data["type"] == "terminal":
    #                 print("我进来了")
    #                 input_data = base64.b64decode(msg_data["data"]["base64"]).decode()
    #                 await ssh_session.write(input_data)
    #             elif msg_data["type"] == "resize":
    #                 rows = msg_data["data"]["rows"]
    #                 cols = msg_data["data"]["cols"]
    #                 if ssh_session.process:
    #                     ssh_session.process.set_terminal_size(rows, cols)
    #         except Exception:
    #             # 没有数据可读时继续循环
    #             pass
    # try:
    #     await asyncio.gather(
    #         ssh_to_ws(ssh_session, ws),
    #         ws_to_ssh(ws, ssh_session)
    #     )
    # except Exception as e:
    #     print("SSH WebSocket error:", e)
    # finally:
    #     await ssh_session.close()
#
# async def ssh_to_ws(ssh, ws):
#     """SSH → WebSocket"""
#     try:
#         while True:
#             data = await ssh.read(1024)
#             if not data:
#                 break
#
#             await ws.send_json({
#                 "type": "terminal",
#                 "data": {
#                     "base64": base64.b64encode(data.encode()).decode()
#                 }
#             })
#     except Exception as e:
#         print(e)
#
# async def ws_to_ssh(ws, ssh):
#     """WebSocket → SSH"""
#     try:
#         while True:
#             msg = await ws.receive_text()
#             msg = json.loads(msg)
#
#             if msg["type"] == "terminal":
#                 data = base64.b64decode(
#                     msg["data"]["base64"]
#                 ).decode()
#                 await ssh.write(data)
#
#             elif msg["type"] == "resize":
#                 if ssh.process:
#                     ssh.process.set_terminal_size(msg["data"]["rows"], msg["data"]["cols"])
#                 # ssh.resize(
#                 #     msg["data"]["rows"],
#                 #     msg["data"]["cols"]
#                 # )
#     except WebSocketDisconnect:
#         pass
