"""
菜单信息
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.common import ajax_success, to_ajax
from app.schemas.menu import MenuBody
from app.services import menu_service
from app.utils.security_utils import get_user_id

router = APIRouter(prefix="/system/menu", dependencies=[Depends(get_current_user)])


@router.get("/selectMenuList")
def select_menu_list(
        menu_name: str | None = Query(default=None, alias="menuName"),
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    查询菜单列表(管理员看所有, 其他角色根据权限过滤)
    """
    user_id = get_user_id(current_user)
    data = menu_service.select_menu_list(db, menu_name, user_id)
    return ajax_success(data=data)


@router.post("/insertMenu")
def insert_menu(body: MenuBody, db: Session = Depends(get_db)):
    """
    新增菜单
    """
    return to_ajax(menu_service.insert_menu(db, body.model_dump(by_alias=True)))

@router.get("/selectMenuByMenuId/{menu_id}")
def select_menu_by_menu_id(menu_id: int, db: Session = Depends(get_db)):
    """
    根据菜单ID查询菜单信息
    """
    menu = menu_service.select_menu_by_menu_id(db, menu_id)
    return ajax_success(data=menu)

@router.put("/updateMenu")
def update_menu(body: MenuBody, db: Session = Depends(get_db)):
    """
    修改菜单
    """
    return to_ajax(menu_service.update_menu(db, body.model_dump(by_alias=True)))

@router.delete("/deleteMenuByMenuId/{menu_id}")
def delete_menu_by_menu_id(menu_id: int, db: Session = Depends(get_db)):
    """
    删除菜单
    """
    return to_ajax(menu_service.delete_menu_by_menu_id(db, menu_id))

@router.get("/selectRoleMenusTree")
def select_role_menus_tree(db: Session = Depends(get_db)):
    """
    查询前端所需要的菜单下拉树结构(用于新增角色)
    """
    menus = menu_service.select_menu_list_by_user_id(db, None, None)
    return ajax_success(data=menu_service.build_menu_tree_select(menus))

@router.get("/selectRoleMenuTree/{role_id}")
def select_role_menu_tree(role_id: int, db: Session = Depends(get_db)):
    """
    根据角色ID查询对应的菜单树
    返回: 该角色勾选的菜单ID数组 + 下拉树结构
    """
    # 查询所有菜单(管理员视角)并且构建前端所需要的下拉树结构
    menus = menu_service.select_menu_list_by_user_id(db, None, None)
    tree = menu_service.build_menu_tree_select(menus)
    # 根据角色ID查询勾选的菜单ID数组
    checked_keys = menu_service.select_menu_list_by_role_id(db, role_id)
    return ajax_success(checkedkeys=checked_keys, menus=tree)

@router.get("/getRouters")
def get_routers(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    获取路由信息(菜单权限)
    功能: 获取当前用户的菜单权限, 用于前端动态生成路由
    """
    # 获取当前用户的ID
    user_id = get_user_id(current_user)
    # 根据用户ID查询该用户的菜单树并且构建成前端需要的路由格式
    routers = menu_service.select_menu_tree_router_by_user_id(db, user_id)
    return ajax_success(data=routers)