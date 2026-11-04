"""
角色信息
"""
from fastapi import APIRouter, Depends, Query
from loguru import logger
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.common import ajax_success, to_ajax
from app.schemas.role import RoleBody
from app.services import role_service
from app.utils import page as page_utils

router = APIRouter(prefix="/system/role", dependencies=[Depends(get_current_user)])


@router.get("/selectAllRole")
def select_all_role(db: Session = Depends(get_db)):
    """
    查询所有角色列表(用于新增/修改用户时的角色下拉框)
    """
    data = [role_service._to_schema(role) for role in role_service.select_role_list(db)]
    return ajax_success(data=data)

@router.get("/selectRoleList")
def select_role_list(
        page_num: int | None = Query(default=None, alias="pageNum"),
        page_size: int | None = Query(default=None, alias="pageSize"),
        role_name: str | None = Query(default=None, alias="roleName"),
        db: Session = Depends(get_db)
):
    """
    查询角色列表(分页)
    """
    page_num, page_size = page_utils.start_page(page_num, page_size)
    data, total = role_service.select_role_page(db, page_num, page_size, role_name)
    return page_utils.get_data_table(data, total)

@router.get("/selectRoleByRoleId/{role_id}")
def select_role_by_role_id(role_id: int, db: Session = Depends(get_db)):
    """
    根据角色ID查询角色信息(包含勾选的菜单ID数组)
    """
    role = role_service.select_role_by_role_id(db, role_id)
    return ajax_success(data=role)

@router.post("/insertRole")
def insert_role(body: RoleBody, db: Session = Depends(get_db)):
    """
    新增角色(同时新增角色菜单关联)
    """
    return to_ajax(role_service.insert_role(db, body.model_dump(by_alias=True)))

@router.put("/updateRole")
def update_role(body: RoleBody, db: Session = Depends(get_db)):
    """
    修改角色(同时修改角色菜单关联)
    """
    return to_ajax(role_service.update_role(db, body.model_dump(by_alias=True)))

@router.delete("/deleteRoleByRoleIds/{role_ids}")
def delete_role_by_role_ids(role_ids: str, db: Session = Depends(get_db)):
    """
    删除角色(支持批量, 路径参数是逗号分隔的ID: 1,2,3)
    """
    # 把"1,2,3"这样的字符串拆成[1, 2, 3]
    ids = [int(x) for x in role_ids.split(",") if x.strip()]
    return to_ajax(role_service.delete_role_by_role_ids(db, ids))