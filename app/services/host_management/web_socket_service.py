# -*- coding: utf-8 -*-
# @Time    : 2026/2/9 15:06
# @Author  : lwc
# @File    : web_socket_service.py
# @Description :

from app.dao.host_management.server_setting_dao import ServerSettingDao
from typing import List


class WebSocketService:

    @staticmethod
    async def get_virtual_machine_info(v_key:List) -> dict:
        res_data = await ServerSettingDao.get_virtual_machine_info(v_key)
        return res_data[0]