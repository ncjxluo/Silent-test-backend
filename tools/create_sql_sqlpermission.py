# -*- coding: utf-8 -*-
# @Time    : 2025/11/24 16:51
# @Author  : lwc
# @File    : create_sql_sqlpermission.py
# @Description : 创建权限匹配表中的数据

import sqlparse
from app.core.db import async_session
from app.models.str_sql_template import StrSqlTemplate
from app.models.str_test_template import StrTestTemplate
from app.models.str_user_template import StrUserTemplate
from sqlmodel import select,and_
import ast
import asyncio

def sql_parser(sql_groups, expect):
    sql_group = sqlparse.split(sql_groups)
    for statements in sql_group:
        if (statements.lower().startswith("insert") or statements.lower().startswith("update") or statements.lower().startswith("delete") or statements.lower().startswith("with") or statements.lower().startswith("replace")) and "影响行数" not in expect:
            expect = expect + " or 影响行数"
    return expect


async def create_sql_temp_data():
    count = 0
    async with async_session() as session:
        query = select(StrUserTemplate)
        result = await session.execute(query)
        users = result.scalars().all()
        res_list = list()
        for user in users:
            db_info = ast.literal_eval(user.t_user_db_name)
            username =  user.t_user_name
            user_permission = ast.literal_eval(user.t_user_permission)
            print(f"--1{user_permission}")
            for item in db_info:
                db_name = item[0]
                db_type = item[1]

                sql_t_query = select(StrSqlTemplate).where(
                    and_(
                        StrSqlTemplate.sql_type == db_type,
                        StrSqlTemplate.sql_exec_timing == "mid"
                    )
                )

                result = await session.execute(sql_t_query)

                sql_templates = result.scalars().all()

                for sql_template in sql_templates:
                    sql_lang = sql_template.sql_lang
                    per_len = len(sql_template.sql_permission.split(','))
                    if sql_template.sql_permission == "export_instance_auth":
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    elif sql_template.sql_permission != "instance_marage" and user_permission[0] == "all":
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    elif sql_template.sql_permission == "instance_marage" and user_permission[0] not in (
                    "instance_marage"):
                        # expect = "没有\s+([a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)?)\s+的\s+([A-Z ]+)\s+权限"
                        expect = "没有\s+([A-Z ]+)\s+数据库的执行权限"
                    elif sql_template.sql_permission.startswith("drop_") and user_permission[
                        0] == "drop_instance_auth" and per_len <= 1:
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    elif sql_template.sql_permission.startswith("create_") and user_permission[
                        0] == "create_instance_auth" and per_len <= 1:
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    elif sql_template.sql_permission.startswith("alter_") and user_permission[
                        0] == "alter_instance_auth" and per_len <= 1:
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    # elif any(Counter(user_permission) == Counter(item1.split(",")) for item1 in sql_template.sql_permission.split(";")):
                    #     # 这个地方有问题，集合应该是包含，而不是相等(比如:用户有select insert update权限，sql需要insert select权限，那么也是可以执行成功)
                    #     expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    elif "select_instance_auth,statistics_instance_auth" in sql_template.sql_permission and \
                            user_permission[0] == "statistics_instance_auth":
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    elif any(set(item1.split(",")).issubset(set(user_permission)) for item1 in sql_template.sql_permission.split(";")):
                        # 应该修改成这样才对，判断sql所需要的权限，是否为用户具备权限的子集合
                        print(f"------:{user_permission}")
                        print(f"------:{sql_template.sql_permission}")
                        expect = sql_parser(sql_lang, "执行成功 or SQL Error")
                    else:
                        expect = "没有\s*([a-zA-Z0-9_.\-]+(?:\s*,\s*[a-zA-Z0-9_.\-]+)*)\s*的\s*([A-Z ]+|[A-Za-z\u4e00-\u9fa5 ]+)\s*权限"
                    if (sql_lang.lower().startswith("insert") or sql_lang.lower().startswith(
                            "update") or sql_lang.lower().startswith("delete") or sql_lang.lower().startswith(
                            "with") or sql_lang.lower().startswith("replace")) and "执行成功" in expect:
                        expect = "执行成功 or 影响行数 or SQL Error"
                    test_temp = StrTestTemplate(
                        username=username,
                        dbname=db_name,
                        schemaname=username,
                        dbtype=db_type,
                        sql=sql_lang,
                        expect=expect,
                    )
                    res_list.append(test_temp)
                    if len(res_list) > 1000:
                        await to_db(res_list)
                        res_list.clear()
                    # session.add(test_temp)
                    # await session.commit()
                    count += 1
                    print(f"已插入{count}条数据")


async def to_db(data_list):
    """
    批量提交报告到数据库
    :param data_list: 一个需要向数据库提交的数据列表
    :return:
    """
    async with async_session() as session:
        session.add_all(data_list)
        await session.commit()

if __name__ == '__main__':
    asyncio.run(create_sql_temp_data())