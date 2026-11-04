"""
登陆注册相关的请求模型
"""
from pydantic import BaseModel, Field

class LoginBody(BaseModel):
    # "populate_by_name": True:允许同时用字段名(user_name)和别名(userName)接收数据
    model_config = {"populate_by_name": True}

    #用户名(alias = "userName":前端传的是驼峰命名)
    user_name : str | None = Field(default=None, alias = "userName")
    #用户密码
    password : str | None = None

class RegisterBody(BaseModel):
    model_config = {"populate_by_name": True}

    user_name : str | None = Field(default=None, alias="userName")

    password : str | None = None


class UpdateProfileBody(BaseModel):
    """
    修改个人信息的对象
    """
    model_config = {"populate_by_name": True}

    # 用户名
    user_name: str | None = Field(default=None, alias="userName")
    # 用户性别
    sex: int | None = None

class SubmitPwdBody(BaseModel):
    """
    修改个人密码的对象
    """
    model_config = {"populate_by_name": True}

    # 旧密码
    old_password: str | None = Field(default=None, alias="oldPassword")
    # 新密码
    new_password: str | None = Field(default=None, alias="newPassword")
    # 确认密码
    confirm_password: str | None = Field(default=None, alias="confirmPassword")