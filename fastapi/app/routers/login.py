"""
登录验证
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import token_service
from app.core.exception_handler import ServiceError
from app.db.session import get_db
from app.schemas.common import ajax_success
from app.schemas.login import LoginBody
from app.services import user_service
from app.utils.security_utils import matches_password

router = APIRouter()

@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    # 步骤1:验证参数是否为空
    user_name = (body.user_name or "").strip()
    password = (body.password or "").strip()
    if not user_name or not password:
        raise ServiceError("用户名或密码不能为空")

    # 步骤2:验证用户是否存在
    user = user_service.select_user_by_name(db, user_name)
    if user is None:
        raise ServiceError("用户名错误")

    # 步骤3:验证密码是否正确
    if not matches_password(password, user.get("password") or ""):
        raise ServiceError("密码错误")

    # 步骤4:
    login_user = {
        "userId": user["userId"],
        "user":{
            "userId": user["userId"],
            "userName": user["userName"],
            "sex": user["sex"],
            "avatar": user["avatar"],
            "password": user["password"],
        },
    }

    # 步骤5: 生成JWT令牌
    token = token_service.create_token(login_user)
    return ajax_success(token = token)