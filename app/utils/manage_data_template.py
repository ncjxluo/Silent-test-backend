# -*- coding: utf-8 -*-
# @Time    : 2026/4/7 15:38
# @Author  : lwc
# @File    : manage_data_template.py
# @Description : 创建ES模板（后续可能将mysql迁入）的地方
import asyncio
from app.core.es import es

# async def create_ilm_policy():
#     body = {
#         "policy": {
#             "phases": {
#                 "hot": {
#                     "min_age": "0ms",
#                     "actions": {
#                         "rollover": {
#                             "max_age": "7d",
#                             "max_size": "50gb",
#                             "max_docs": 10000000
#                         },
#                         "set_priority": {"priority": 100}
#                     }
#                 },
#                 "delete": {
#                     "min_age": "90d",
#                     "actions": {"delete": {}}
#                 }
#             }
#         }
#     }
#
#
#     await es.ilm.put_lifecycle(
#         policy="str_test_case_step_policy",
#         body=body
#     )
#
#     body = {
#         "policy": {
#             "phases": {
#                 "hot": {
#                     "min_age": "0ms",
#                     "actions": {
#                         "rollover": {
#                             "max_age": "7d",
#                             "max_size": "50gb",
#                             "max_docs": 10000000
#                         },
#                         "set_priority": {"priority": 100}
#                     }
#                 },
#                 "delete": {
#                     "min_age": "90d",
#                     "actions": {"delete": {}}
#                 }
#             }
#         }
#     }
#
#     await es.ilm.put_lifecycle(
#         policy="str_monitor_policy",
#         body=body
#     )
#
# async def create_index_template():
#     body = {
#         "index_patterns": ["str_test_case_step-*"],
#         "priority": 500,
#         "template": {
#             "settings": {
#                 "number_of_shards": 1,
#                 "number_of_replicas": 0,
#                 "index.lifecycle.name": "str_test_case_step_policy",
#                 "index.lifecycle.rollover_alias": "str_test_case_step"
#             },
#             "mappings": {
#                 "dynamic": True,
#                 "properties": {
#                     "suite_key": {"type": "keyword"},
#                     "plan_key": {"type": "keyword"},
#                     "case_key": {"type": "keyword"},
#                     "step_id": {"type": "keyword"},
#                     "step_name": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {"type": "keyword"}
#                         }
#                     },
#                     "user_variables": {"type": "flattened"},
#                     "request_url": {"type": "keyword"},
#                     "request_param": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {"type": "keyword", "ignore_above": 2048}
#                         }
#                     },
#                     "real_response": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {"type": "keyword", "ignore_above": 2048}
#                         }
#                     },
#                     "response_time": {"type": "float"},
#                     "assert_res_sign": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {"type": "keyword", "ignore_above": 2048}
#                         }
#                     },
#                     "assert_res_details": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {"type": "keyword", "ignore_above": 2048}
#                         }
#                     },
#                     "assert_ver_sign": {
#                         "type": "text",
#                         "fields": {
#                             "keyword": {"type": "keyword", "ignore_above": 2048}
#                         }
#                     },
#                     "assert_time_sign": {"type": "keyword"},
#                     "created_at": {"type": "date"},
#                     "updated_at": {"type": "date"}
#                 }
#             }
#         }
#     }
#
#     await es.indices.put_index_template(
#         name="str_test_case_step_template",
#         body=body
#     )
#
#     body = {
#         "index_patterns": ["str_monitor-*"],
#         "priority": 500,
#         "template": {
#             "settings": {
#                 "number_of_shards": 1,
#                 "number_of_replicas": 0,
#                 "index.lifecycle.name": "str_monitor_policy",
#                 "index.lifecycle.rollover_alias": "str_monitor"
#             },
#             "mappings": {
#                 "dynamic": True,
#                 "properties": {
#                     "container_name": {"type": "keyword"},
#                     "cpu_usage": {"type": "float"},
#                     "mem_percent": {"type": "float"},
#                     "blkio_bytes": {"type": "float"},
#                     "lock_wait": {"type": "float"},
#                     "event_type": {"type": "keyword"},
#                     "trigger_time": {"type": "date"},
#                     "file_path": {"type": "keyword"},
#                     "created_at": {"type": "date"},
#                     "updated_at": {"type": "date"}
#                 }
#             }
#         }
#     }
#
#     await es.indices.put_index_template(
#         name="str_monitor_template",
#         body=body
#     )
#
#
# async def init_index():
#     await es.indices.create(
#         index="str_test_case_step-000001",
#         body={
#             "aliases": {
#                 "str_test_case_step": {
#                     "is_write_index": True
#                 }
#             }
#         }
#     )
#     await es.indices.create(
#         index="str_monitor-000001",
#         body={
#             "aliases": {
#                 "str_monitor": {
#                     "is_write_index": True
#                 }
#             }
#         }
#     )

async def create_ilm_policy():
    body = {
        "policy": {
            "phases": {
                "hot": {
                    "min_age": "0ms",
                    "actions": {
                        "rollover": {
                            "max_age": "7d",
                            "max_size": "50gb",
                            "max_docs": 10000000
                        },
                        "set_priority": {"priority": 100}
                    }
                },
                "delete": {
                    "min_age": "90d",
                    "actions": {"delete": {}}
                }
            }
        }
    }

    await es.ilm.put_lifecycle(
        policy="str_monitor_policy",
        body=body
    )


async def create_index_template():
    body = {
        "index_patterns": ["str_monitor-*"],
        "priority": 500,
        "template": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "index.lifecycle.name": "str_monitor_policy",
                "index.lifecycle.rollover_alias": "str_monitor"
            },
            "mappings": {
                "dynamic": True,
                "properties": {
                    "container_name": {"type": "keyword"},
                    "cpu_usage": {"type": "float"},
                    "mem_percent": {"type": "float"},
                    "blkio_bytes": {"type": "float"},
                    "lock_wait": {"type": "float"},
                    "event_type": {"type": "keyword"},
                    "trigger_time": {"type": "date"},
                    "file_path": {"type": "keyword"},
                    "created_at": {"type": "long"},
                    "updated_at": {"type": "long"}
                }
            }
        }
    }

    await es.indices.put_index_template(
        name="str_monitor_template",
        body=body
    )


async def init_index():
    await es.indices.create(
        index="str_monitor-000001",
        body={
            "aliases": {
                "str_monitor": {
                    "is_write_index": True
                }
            }
        }
    )

async def main(mtype: int):
    if mtype == 1:
        print("🚀 开始初始化 ES ILM + 模板 + 索引...")
        try:
            await create_ilm_policy()
            await create_index_template()
            await init_index()
            print("\n🎉 所有 ES 初始化配置执行完成！")
        except Exception as e:
            print(f"\n❌ 执行失败: {str(e)}")
        finally:
            await es.close()  # 关闭连接
    elif mtype == 2:
        await es.indices.delete(index="str_monitor-*")
        await es.ilm.delete_lifecycle(policy="str_monitor_policy")
        print("♻️ ILM 策略已删除")
        await es.indices.delete_index_template(name="str_monitor_template")
        print("♻️ 索引模板已删除")
    else:
        await es.indices.delete(index="str_test_case_step-*")
        await es.ilm.delete_lifecycle(policy="str_test_case_step_policy")
        print("♻️ ILM 策略已删除")
        await es.indices.delete_index_template(name="str_test_case_step_template")
        print("♻️ 索引模板已删除")
        await es.indices.delete(index="str_monitor-*")
        await es.ilm.delete_lifecycle(policy="str_monitor_policy")
        print("♻️ ILM 策略已删除")
        await es.indices.delete_index_template(name="str_monitor_template")
        print("♻️ 索引模板已删除")


if __name__ == "__main__":
    asyncio.run(main(1))