# -*- coding: utf-8 -*-
# @Time    : 2025/10/30 16:05
# @Author  : lwc
# @File    : db.py.py
# @Description : 数据库链接的

from app.utils.helper import get_config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker


IP = get_config().get("db").get("host")
PORT = get_config().get("db").get("port")
UNAME = get_config().get("db").get("user")
PASSWD = get_config().get("db").get("password")
SCHEMA = get_config().get("db").get("schema")

DATABASE_URL = f"mysql+asyncmy://{UNAME}:{PASSWD}@{IP}:{PORT}/{SCHEMA}"

engine = create_async_engine(DATABASE_URL,
            echo=True,                # 是否展示sql
            future=True,              # 开启未来模式
            pool_size=10,             # 连接池中保持的连接数量
            max_overflow=20,          # 在pool_size之外最多还能开多少连接（峰值负载时）
            pool_recycle=3600,        # 连接回收时间（秒），防止 MySQL 空闲断开
            pool_timeout=30)          # 获取连接超时)


async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,    # 手动控制 flush
    autocommit=False,   # 手动控制提交
)