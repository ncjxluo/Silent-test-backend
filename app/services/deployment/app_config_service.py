# -*- coding: utf-8 -*-
# @Time    : 2026/3/2 17:27
# @Author  : lwc
# @File    : app_config_service.py
# @Description :

from app.dao.deployment.app_config_dao import AppconfigDao

class AppConfigService:

    @staticmethod
    async def add_app_config(app_nickname:str,app_product_line:str,
                             app_before_name:str,app_end_name:str,app_download_type:str,
                             app_download_ip:str,app_download_port:str,
                             app_download_uname:str,app_download_passwd:str,app_download_path:str) -> dict:

        data = await AppconfigDao.add_app_config(
            app_nickname,app_product_line,app_before_name,app_end_name,app_download_type,
            app_download_ip,app_download_port,app_download_uname,app_download_passwd,app_download_path
        )
        return data

    @staticmethod
    async def add_app_line(app_product_line:str) -> dict:
        data = await AppconfigDao.add_app_line(
            app_product_line
        )
        return data


    @staticmethod
    async def get_app_config(app_nickname:str, app_product_line, current_page:int, current_count:int) -> dict:

        data = await AppconfigDao.get_app_config(app_nickname, app_product_line, current_page, current_count)
        count = await AppconfigDao.get_app_config_count(app_nickname, app_product_line)
        return {"total_count": count[0], "app_configs": data}


    @staticmethod
    async def edit_app_config(id:int, app_nickname:str,app_product_line:str,
                             app_before_name:str,app_end_name:str,app_download_type:str,
                             app_download_ip:str,app_download_port:str,
                             app_download_uname:str,app_download_passwd:str,app_download_path:str) -> dict:

        data = await AppconfigDao.edit_app_config(
            id,app_nickname,app_product_line,app_before_name,app_end_name,app_download_type,
            app_download_ip,app_download_port,app_download_uname,app_download_passwd,app_download_path
        )
        return data

    @staticmethod
    async def del_app_config(id:int) -> dict:

        data = await AppconfigDao.del_app_config(id)
        return data

    @staticmethod
    async def get_app_line() -> dict:

        data = await AppconfigDao.get_app_line()
        return data

    @staticmethod
    async def get_app_config_selected(app_product_line:str) -> dict:
        data = await AppconfigDao.get_app_config_selected(app_product_line)
        return data