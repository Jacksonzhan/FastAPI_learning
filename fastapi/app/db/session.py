"""
数据库连接配置
作用：创建数据库引擎和会话工厂
相当于整个系统的数据源
"""

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建数据库引擎，用于连接数据库
engine = create_engine(
    settings.database_url,
    # 连接池预检，每次连接使用前都进行预检
    pool_pre_ping=True,
    # 连接池回收时间，单位为秒，超过此时间(1h)的连接将被回收
    pool_recycle=3600,
    # 是否开启SQL语句的打印，用于调试(调试时可改为True)
    echo=False
)

#创建会话工厂
"""
autocommit=False: 禁用自动提交
autoflush=False: 禁用自动刷新
bind=engine: 绑定数据库引擎
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
