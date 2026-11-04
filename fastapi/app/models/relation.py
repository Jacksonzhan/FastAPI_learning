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

class RoleMenu(Base):
    """
    角色和菜单关联 role_menu
    """
    __tablename__ = "role_menu"

    # 角色ID
    role_id: int = Column(Integer, primary_key=True, comment="角色ID")
    # 菜单ID
    menu_id: int = Column(Integer, primary_key=True, comment="菜单ID")