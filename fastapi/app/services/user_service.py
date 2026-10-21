"""
用户业务处理
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserSchema

def _to_schema(user: User) -> dict:
    """
    把数据库查询出来的用户对象转换成返回前端的字典(驼峰命名)
    :param user:
    :return:
    """
    # 从数据库模型对象中创建自动映射同名字段，再按照别名输出驼峰命名
    return UserSchema.model_validate(user).model_dump(by_alias=True)

def select_user_by_name(db:Session, user_name: str) -> dict | None:
    """
    根据用户名查询用户
    :param db:数据库会话
    :param user_name:用户名
    :return:用户的对象信息(没查询到就返回None)
    """
    user = db.execute(select(User).where(User.user_name == user_name)).scalar_one_or_none()
    if user is None:
        return None
    return _to_schema(user)

def select_user_by_user_id(db: Session, user_id: int) -> dict | None:
    """
    根据用户ID查询用户
    :param db:数据库会话
    :param user_id:用户ID
    :return:用户的对象信息(没查询到就返回None)
    """
    user = db.get(User, user_id)
    if user is None:
        return None
    return _to_schema(user)