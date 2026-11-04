"""
角色 业务处理
"""
from loguru import logger
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from app.models import Role, RoleMenu
from app.schemas.role import RoleSchema


def _to_schema(role: Role) -> dict:
    """
    把角色对象转换成返回给前端的字典(驼峰命名)
    """
    schema = RoleSchema.model_validate(role)
    return schema.model_dump(by_alias=True, exclude_none=True)


def select_role_list(db: Session, role_name: str | None = None) -> list[Role]:
    """
    查询角色列表(不分页, 用于下拉框)
    条件角色名称模糊搜索
    排序: 按显示顺序字段正序排序
    :return: 角色列表数据
    """
    stmt = (
        select(Role)
    )

    # 条件查询: 用户名模糊搜索
    if role_name:
        stmt = stmt.where(Role.role_name.like(f"%{role_name}%"))

    stmt = stmt.order_by(Role.role_sort)

    return list(db.execute(stmt).scalars().all())


def select_role_page(db: Session, page_num: int, page_size: int, role_name: str | None) -> tuple[list[dict], int]:
    """
    查询角色(分页)
    :return: (角色列表, 数据总数)
    """
    stmt = (select(Role))

    if role_name:
        stmt = stmt.where(Role.role_name.like(f"%{role_name}%"))

    # 查询数据总数
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar() or 0

    # 分页查询(按显示顺序字段正序排序)
    stmt = stmt.order_by(Role.role_sort).offset((page_num - 1) * page_size).limit(page_size)
    roles =list(db.execute(stmt).scalars().all())

    data = [_to_schema(role) for role in roles]
    return data, total

def select_role_by_role_id(db: Session, role_id: int) -> dict | None:
    """
    通过角色ID查询角色信息
    """
    role = db.get(Role, role_id)
    if role is None:
        return None
    # 同时查询该角色勾选的菜单ID数组(角色菜单权限)
    menu_ids = list(
        db.execute(select(RoleMenu.menu_id).where(RoleMenu.role_id == role_id)).scalars().all()
    )
    schema = RoleSchema.model_validate(role)
    schema = schema.model_copy(update={"menu_ids": menu_ids})
    return schema.model_dump(by_alias=True, exclude_none=True)

def _insert_role_menu(db: Session, role_id: int, menu_ids: list[int]) -> int:
    """
    批量新增角色菜单关联
    """
    if not menu_ids:
        return 1
    db.add_all([RoleMenu(role_id=role_id, menu_id=menu_id) for menu_id in menu_ids])
    return len(menu_ids)

def insert_role(db: Session, role_body: dict) -> int:
    """
    新增角色(同时新增角色菜单关联信息)
    """
    # 步骤1: 新增角色
    role = Role(
        role_name=role_body.get("roleName") or "",
        role_sort=role_body.get("roleSort") or 0,
    )
    db.add(role)
    db.flush()  # 拿到自增主键role_id

    # 步骤2: 新增角色菜单关联信息
    rows = _insert_role_menu(db, role.role_id, role_body.get("menuIds") or [])

    db.commit()
    return rows

def update_role(db: Session, role_body: dict) -> int:
    """
    修改角色(同时先删后插更新角色菜单权限)
    """
    role_id = role_body.get("roleId")

    # 步骤1: 修改角色
    role = db.get(Role, role_id)
    if role is None:
        return 0
    if role_body.get("roleName"):
        role.role_name = role_body["roleName"]
    if role_body.get("roleSort"):
        role.role_sort = role_body["roleSort"]

    rows = 1

    # 步骤2: 根据角色ID删除角色和菜单关联(先删)
    db.execute(delete(RoleMenu).where(RoleMenu.role_id == role_id))

    # 步骤3: 新增角色菜单信息(后插)
    _insert_role_menu(db, role_id, role_body.get("menuIds") or [])

    db.commit()
    return rows

def delete_role_by_role_ids(db: Session, role_ids: list[int]) -> int:
    """
    删除角色(同时删除与菜单的关联)
    """

    # 步骤1: 删除角色
    roles = db.execute(select(Role).where(Role.role_id.in_(role_ids))).scalars().all()
    for role in roles:
        db.delete(role)

    # 步骤2: 批量删除角色菜单关联信息
    db.execute(delete(RoleMenu).where(RoleMenu.role_id.in_(role_ids)))

    db.commit()
    return len(roles)