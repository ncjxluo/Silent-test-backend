# -*- coding: utf-8 -*-
# @Time    : 2025/11/3 15:46
# @Author  : lwc
# @File    : initdb.py
# @Description : 初始化数据库

import asyncio
from sqlmodel import SQLModel
from app.core.db import engine
from app.models.str_sys_user import StrSysUser
from app.models.str_sys_role import StrSysRole
from app.models.str_sys_menu import StrSysMenu
from app.models.str_sys_dept import StrSysDept
from app.models.str_sys_user_role import StrSysUserRole
from app.models.str_sys_role_menu import StrSysRoleMenu
from app.models.str_test_suite import StrTestSuite
from app.models.str_test_plan import StrTestPlan
from app.models.str_test_case import StrTestCase

async def init_db():
    """
    通过该函数，来初始化数据库
    :return:
    """
    print("Creating database tables...")
    async with engine.begin() as conn:
        # 等价于 Base.metadata.create_all()
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Inserting base data...")
    async with engine.begin() as conn:

        await conn.execute(
            StrSysUser.__table__.insert(),
            [{"nickname": "admin", "username": "admin"}]
        )

        await conn.execute(
            StrSysDept.__table__.insert(),
            [{"dept_name": "产品部"},{"dept_name": "研发部"},{"dept_name": "测试部"}]
        )

        await conn.execute(
            StrSysRole.__table__.insert(),
            [{"role_name": "管理员", "description": "拥有系统最高权限"},
             {"role_name": "测试", "description": "拥有系统测试、部署相关权限"},
             {"role_name": "研发", "description": "拥有系统测试报告查看、部署相关权限"},
             {"role_name": "产品", "description": "拥有系统测试报告查看、部分部署相关权限"}]
        )

    print("Database initialized.")


if __name__ == "__main__":
    asyncio.run(init_db())