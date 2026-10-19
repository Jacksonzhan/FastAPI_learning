"""
用户相关的响应模型
"""
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer

class UserSchema(BaseModel):
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

    @field_serializer("create_time")
    def serialize_time(self, value: datetime | None):
        """时间格式化: 返回给前端时统一显示为 xxxx-xx-xx xx:xx:xx"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")