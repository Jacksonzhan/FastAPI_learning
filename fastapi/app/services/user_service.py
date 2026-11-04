"""
用户业务处理
"""

from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from app.core.exception_handler import ServiceError
from app.models import User, Role, UserRole
from app.models.relation import UserRole
from app.schemas.user import UserSchema
from app.utils.security_utils import encrypt_password


def _to_schema(user: User, role_id: int | None = None, role_name: str | None = None) -> dict:
    """
    把数据库查询出来的用户对象转换成返回给前端的字典(驼峰命名)
    :param user: 用户对象
    :param role_id: 关联查询出来的角色ID(没查到就传None)
    :param role_name:  关联查询出来的角色名称(没查到就传None)
    :return:
    """
    # 从数据库模型对象中创建自动映射同名字段, 再按照别名输出驼峰命名
    # 步骤1: 从数据库模型对象创建schema(自动映射同名字段)
    schema = UserSchema.model_validate(user)
    # 步骤2: 补充关联查询出来的角色字段
    # 角色信息不在user对象上, model_validate拿不到它们, 只能创建完schema后再手动塞进去
    schema = schema.model_copy(update={"role_id": role_id, "role_name": role_name})

    return schema.model_dump(by_alias=True)


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
    通过用户ID查询用户信息(关联查询角色ID和角色名称)
    :param db:
    :param user_id:
    :return:
    """
    # 基础查询: 用户表 左连接 用户角色关联表 左连接 角色表
    stmt = (
        select(User, UserRole.role_id, Role.role_name)
        .outerjoin(UserRole, User.user_id == UserRole.user_id)
        .outerjoin(Role, UserRole.role_id == Role.role_id)
        .where(User.user_id == user_id)
    )
    row = db.execute(stmt).first()

    if row is None:
        return None
    # (User对象, 角色ID, 角色名称)
    return _to_schema(row[0], row[1], row[2])


def register_user(db: Session, user_body: dict) -> int:
    # 步骤1: 根据用户名查询用户信息(查重)
    user_name = user_body.get("userName") or ""
    existing = db.execute(select(User).where(User.user_name == user_name)).scalar_one_or_none()
    if existing is not None:
        raise ServiceError("用户名已存在, 请更换用户名后再注册")

    # 步骤2: 新增用户
    user = User(
        user_name=user_name,
        password=encrypt_password(user_body.get("password") or "")
    )

    db.add(user)
    db.flush()

    # 步骤3: 注册用户的角色默认为普通用户(角色ID=2)
    from app.constants import RoleIdConstants
    db.add(UserRole(user_id=user.user_id, role_id=RoleIdConstants.USER_ROLE_ID))

    db.commit()
    return 1


def update_user_avatar(db: Session, user_id: int, avatar: str) -> int:
    """
    更新用户头像
    """
    user = db.get(User, user_id)
    if user is None:
        return 0
    user.avatar = avatar
    db.commit()
    return 1


def update_profile(db: Session, user_id: int, user_name: str | None, sex: int | None) -> int:
    """
    修改个人信息(修改当前登录用户的用户名和性别)
    """
    user = db.get(User, user_id)
    if user is None:
        return 0
    # 传了才更新, 没传保持原值
    if user_name:
        user.user_name = user_name
    if sex is not None:
        user.sex = sex
    db.commit()
    return 1


def reset_user_pwd(db: Session, user_id: int, password: str) -> int:
    """
    重置用户密码(密码加密后更新)
    """
    user = db.get(User, user_id)
    if user is None:
        return 0
    # 新密码同样要加密
    user.password = encrypt_password(password)
    db.commit()
    return 1


def select_user_list(db: Session, page_num: int, page_size: int, user_name: str | None) -> tuple[list[dict], int]:
    """
    查询用户列表(关联查询角色ID和角色名称, 支持分页)
    :return: (用户列表, 数据总数)
    """
    # 基础查询: 用户表 左连接 用户角色关联表 左连接 角色表
    stmt = (
        select(User, UserRole.role_id, Role.role_name)
        .outerjoin(UserRole, User.user_id == UserRole.user_id)
        .outerjoin(Role, UserRole.role_id == Role.role_id)
    )

    # 条件查询: 用户名模糊搜索
    if user_name:
        stmt = stmt.where(User.user_name.like(f"%{user_name}%"))

    # 步骤1: 查询数据总数(分页需要, 前端需要total计算一共有多少页)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar() or 0

    # 步骤2: 分页查询数据
    stmt = stmt.order_by(User.user_id).offset((page_num - 1) * page_size).limit(page_size)
    rows = db.execute(stmt).all()

    # 步骤3: 转换成前端需要的格式(驼峰命名)
    data = [_to_schema(row[0], row[1], row[2]) for row in rows]
    return data, total


def insert_user(db: Session, user_body: dict) -> int:
    """
    新增用户
    :return: 是否新增成功(1成功 0失败)
    """
    # 步骤1: 密码加密(不能存明文!!!)
    password = encrypt_password(user_body.get("password") or "")

    # 步骤2: 新增用户
    user = User(
        user_name=user_body.get("userName") or "",
        sex=user_body.get("sex"),
        password=password,
    )
    db.add(user)
    db.flush()  # flush后数据库会分配自增主键, user.user_id就有值了(还没有真正入库)
    rows = 1

    # 步骤3: 新增用户与角色关联(如果传了roleId)
    role_id = user_body.get("roleId")
    if role_id:
        db.add(UserRole(user_id=user.user_id, role_id=role_id))

    db.commit()
    return rows


def update_user(db: Session, user_body: dict) -> int:
    """
    修改用户(同时先删后插更新用户与角色的关联)
    :return: 是否修改成功(1成功 0失败)
    """
    user_id = user_body.get("userId")

    # 步骤1: 查询出要修改的用户
    user = db.get(User, user_id)
    if user is None:
        raise ServiceError("用户不存在")

    # 步骤2: 更新用户基本字段(传了才更新, 没传保持原值)
    if user_body.get("userName"):
        user.user_name = user_body["userName"]
    if user_body.get("sex"):
        user.sex = user_body["sex"]
    # 密码加密后更新
    if user_body.get("password"):
        user.password = encrypt_password(user_body["password"])
    rows = 1

    # 步骤3: 根据用户ID删除用户和角色的关联(先删)
    db.execute(delete(UserRole).where(UserRole.user_id == user_id))

    # 步骤4: 新增用户和角色关联(后插)
    role_id = user_body.get("roleId")
    if role_id:
        db.add(UserRole(user_id=user_id, role_id=role_id))

    db.commit()
    return rows


def delete_user_by_user_ids(db: Session, user_ids: list[int]) -> int:
    """
    批量删除用户(同时删除与角色的关联数据)
    :return: 受到影响的行数
    """
    # 步骤1: 删除用户
    users = db.execute(select(User).where(User.user_id.in_(user_ids))).scalars().all()
    for user in users:
        db.delete(user)

    # 步骤2: 批量删除用户与角色关联(不删的话数据库会残留垃圾数据)
    db.execute(delete(UserRole).where(UserRole.user_id.in_(user_ids)))

    db.commit()
    return len(users)