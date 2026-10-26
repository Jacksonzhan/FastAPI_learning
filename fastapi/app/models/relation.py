"""
关联表模型
用户和角色关联
"""
from app.models import Base
from sqlalchemy import Column, Integer

class UserRole(Base):
    """用户和角色关联 user_role"""
    __tablename__ = "user_role"
    # 用户ID
    user_id: int = Column(Integer, primary_key=True, comment="用户ID")
    # 角色ID
    role_id: int = Column(Integer, primary_key=True, comment="角色ID")