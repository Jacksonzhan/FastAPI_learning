"""
用户相关的响应模型
作用: 规定返回给前端的字段名(驼峰)和格式(比如时间格式)
"""
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer


class UserSchema(BaseModel):
    """
    用户信息(返回给前端的格式)
    Python里习惯用蛇形命名(user_name), 前端习惯用驼峰命名(userName)
    通过alias做映射, 保证前后端字段一致
    """
    # from_attributes=True: 允许直接从数据库模型对象(User)创建
    # populate_by_name=True: 允许同时用字段名(userName)和别名接收数据
    model_config = {"populate_by_name": True, "from_attributes": True}

    # 用户ID
    user_id: int | None = Field(default=None, alias="userId")
    # 用户名
    user_name: str | None = Field(default=None, alias="userName")
    # 用户性别
    sex: int | None = None
    # 用户头像
    avatar: str | None = None
    # 密码
    password: str | None = None
    # 创建时间
    create_time: datetime | None = Field(default=None, alias="createTime")
    # 角色ID
    role_id: int | None = Field(default=None, alias="roleId")
    # 角色名称
    role_name: str | None = Field(default=None, alias="roleName")

    @field_serializer("create_time")
    def serialize_time(self, value: datetime | None):
        """时间格式化: 返回给前端时统一显示为 xxxx-xx-xx xx:xx:xx"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

class UserBody(BaseModel):
    """
    新增/修改用户时的请求对象
    """
    model_config = {"populate_by_name": True}

    # 用户ID
    user_id: int | None = Field(default=None, alias="userId")
    # 用户名
    user_name: str | None = Field(default=None, alias="userName")
    # 用户性别
    sex: int | None = None
    # 用户头像
    avatar: str | None = None
    # 密码
    password: str | None = None
    # 角色ID(该字段用于关联角色信息)
    role_id: int | None = Field(default=None, alias="roleId")