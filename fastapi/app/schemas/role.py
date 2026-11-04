"""
角色模型
"""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base
from pydantic import BaseModel, Field, field_serializer


class Role(Base):
    """
    角色对象
    """
    __tablename__ = "role"

    # 角色ID
    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="角色ID")
    # 角色名称
    role_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="角色名称")
    # 显示排序
    role_sort: Mapped[int] = mapped_column(Integer, nullable=False, comment="显示排序")
    # 创建时间(数据库默认当前时间)
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=func.current_timestamp(), comment="创建时间"
    )

class RoleSchema(BaseModel):
    """
    角色信息(返回给前端的格式)致
    """
    model_config = {"populate_by_name": True, "from_attributes": True}

    # 角色ID
    role_id: int | None = Field(default=None, alias="roleId")
    # 角色名称
    role_name: str | None = Field(default=None, alias="roleName")
    # 显示顺序
    role_sort: int | None = None
    # 创建时间
    create_time: datetime | None = Field(default=None, alias="createTime")
    # 菜单组
    menu_ids: list[int] | None = Field(default=None, alias="menuIds")

    @field_serializer("create_time")
    def serialize_time(self, value: datetime | None):
        """时间格式化: 返回给前端时统一显示为 xxxx-xx-xx xx:xx:xx"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

class RoleBody(BaseModel):
    """
    新增/修改角色时的请求对象
    """

    # 角色ID
    role_id: int | None = Field(default=None, alias="roleId")
    # 角色名称
    role_name: str | None = Field(default=None, alias="roleName")
    # 显示顺序
    role_sort: int | None = Field(default=None, alias="roleSort")
    # 菜单组
    menu_ids: list[int] | None = Field(default=None, alias="menuIds")