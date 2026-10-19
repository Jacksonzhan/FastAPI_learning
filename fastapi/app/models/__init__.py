"""
模型统一导出
作用：保证定义模型时Base只被创建一次(放到__init__.py文件里就是为了保证这个)，所有模型共享一个Base
"""
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """所有模型类的基类"""
    pass

from app.models.user import User

__all__ = ["Base","User"]