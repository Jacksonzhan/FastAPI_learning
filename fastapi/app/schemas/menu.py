"""
菜单相关的模型
"""
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer


class MenuSchema(BaseModel):
    """菜单信息(返回给前端的格式)"""
    model_config = {"populate_by_name": True, "from_attributes": True}

    # 菜单ID
    menu_id: int | None = Field(default=None, alias="menuId")
    # 菜单名称
    menu_name: str | None = Field(default=None, alias="menuName")
    # 父菜单ID
    parent_id: int | None = Field(default=None, alias="parentId")
    # 菜单排序
    menu_sort: int | None = Field(default=None, alias="menuSort")
    # 路由地址
    path: str | None = None
    # 组件路径
    component: str | None = None
    # 菜单类型(M目录 C菜单)
    menu_type: str | None = Field(default=None, alias="menuType")
    # 菜单图标
    icon: str | None = None
    # 创建时间
    create_time: datetime | None = Field(default=None, alias="createTime")

    @field_serializer("create_time")
    def serialize_time(self, value: datetime | None):
        """时间格式化: 返回给前端时统一显示为 xxxx-xx-xx xx:xx:xx"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

class MenuBody(BaseModel):
    """新增/修改菜单时的请求对象"""
    model_config = {"populate_by_name": True}

    # 菜单ID
    menu_id: int | None = Field(default=None, alias="menuId")
    # 菜单名称
    menu_name: str | None = Field(default=None, alias="menuName")
    # 父菜单ID
    parent_id: int | None = Field(default=None, alias="parentId")
    # 菜单排序
    menu_sort: int | None = Field(default=None, alias="menuSort")
    # 路由地址
    path: str | None = None
    # 组件路径
    component: str | None = None
    # 菜单类型(M目录 C菜单)
    menu_type: str | None = Field(default=None, alias="menuType")
    # 菜单图标
    icon: str | None = None