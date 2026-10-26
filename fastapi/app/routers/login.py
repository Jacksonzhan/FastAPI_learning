"""
登录验证
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import token_service
from app.core.deps import get_current_user
from app.core.exception_handler import ServiceError
from app.db.session import get_db
from app.schemas.common import ajax_success, ajax_error
from app.schemas.login import LoginBody, RegisterBody
from app.services import user_service
from app.utils.security_utils import matches_password, get_user_id

router = APIRouter()

@router.post("/login", summary="用户登录")
def login(body: LoginBody, db: Session = Depends(get_db)):
    """
    登录接口
    - 参数：用户名 + 密码
    - 返回：token
    """
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

    # 步骤6: 返回成功结果
    return ajax_success(token = token)

@router.get("/getInfo")
def gen_info(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    获取当前用户信息
    """
    # 步骤1:获取当前登录用户的用户ID
    user_id = get_user_id(current_user)

    # 步骤2:根据用户ID查询用户信息
    user = user_service.select_user_by_user_id(db, user_id)

    # 步骤3:返回用户信息
    return ajax_success(data=user)


@router.post("/register", summary="用户注册")
def login(body: RegisterBody, db: Session = Depends(get_db)):
    """
    注册接口
    """

    user_name = body.user_name
    password = body.user_name

    if not user_name:
        return ajax_error("用户名不存在")

    if not password:
        return ajax_error("密码不能为空")

    # 执行注册逻辑
    reg_flag = user_service.register_user(db, body.model_dump(by_alias=True))

    if not reg_flag:
        return ajax_error("注册失败")

    return ajax_success()