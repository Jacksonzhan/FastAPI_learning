"""
菜单模型 menu
"""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Menu(Base):
    """菜单对象 menu"""
    __tablename__ = "menu"

    # 菜单ID(自增主键)
    menu_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="菜单ID")
    # 菜单名称
    menu_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="菜单名称")
    # 父菜单ID(0表示顶级菜单)
    parent_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="父菜单ID")
    # 菜单排序
    menu_sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="菜单排序")
    # 路由地址
    path: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="路由地址")
    # 组件路径
    component: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="组件路径")
    # 菜单类型(M目录 C菜单)
    menu_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="菜单类型(M目录 C菜单)")
    # 菜单图标
    icon: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="菜单图标")
    # 创建时间(数据库默认当前时间)
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.current_timestamp(), comment="创建时间"
    )