from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import RoleIdConstants
from app.models import Menu, RoleMenu, UserRole
from app.schemas.menu import MenuSchema

def _to_schema(menu: Menu, children: list[dict] | None = None) -> dict:
    """
    把菜单对象转换成返回给前端的格式(驼峰命名)
    """
    data = MenuSchema.model_validate(menu).model_dump(by_alias=True)
    # 子菜单列表(不为空时才放入)
    if children:
        data["children"] = children
    return data

def select_menu_list_by_user_id(db: Session, menu_name: str | None, user_id: int | None) -> list[Menu]:
    """
    根据用户ID查询菜单列表
    """
    stmt = select(Menu)
    if user_id is not None:
        # 非管理员: 只查询该用户拥有的菜单(通过角色关联)
        stmt = (
            stmt.outerjoin(RoleMenu, Menu.menu_id == RoleMenu.menu_id)
            .outerjoin(UserRole, RoleMenu.role_id == UserRole.role_id)
            .where(UserRole.user_id == user_id)
        )
    if menu_name:
        stmt = stmt.where(Menu.menu_name.like(f"%{menu_name}%"))
    stmt = stmt.order_by(Menu.menu_sort)
    return list(db.execute(stmt).scalars().all())

def select_role_id_by_user_id(db: Session, user_id: int) -> int | None:
    """
    根据用户ID查询角色ID
    """
    return db.execute(
        select(UserRole.role_id).where(UserRole.user_id == user_id)
    ).scalar_one_or_none()

def select_menu_list(db: Session, menu_name: str | None, user_id: int) -> list[dict]:
    """
    查询菜单列表
    需求: 每个用户都有自己对应的角色, 每个角色的菜单权限是不同的
    例如: 管理员可以看到所有菜单, 普通用户只能看到某些菜单
    """
    # 1.根据用户ID查询对应的角色ID
    role_id = select_role_id_by_user_id(db, user_id)

    # 2.管理员显示所有菜单信息, 其他用户按照权限过滤
    if role_id == RoleIdConstants.ADMIN_ROLE_ID:
        menus = select_menu_list_by_user_id(db, menu_name, None)
    else:
        menus = select_menu_list_by_user_id(db, menu_name, user_id)

    # 3.转换成前端需要的格式
    return [_to_schema(menu) for menu in menus]

def insert_menu(db:Session, menu_body: dict) -> int:
    """
    新增菜单
    """
    menu = Menu(
        menu_name=menu_body.get("menuName") or "",
        parent_id=menu_body.get("parentId") or 0,
        menu_sort=menu_body.get("menuSort") or 0,
        path=menu_body.get("path"),
        component=menu_body.get("component"),
        menu_type=menu_body.get("menuType") or "C",
        icon=menu_body.get("icon"),
    )
    db.add(menu)
    db.commit()
    return 1

def select_menu_by_menu_id(db: Session, menu_id: int) -> dict | None:
    """
    根据菜单ID查询菜单信息
    """
    menu = db.get(Menu, menu_id)
    if menu is None:
        return None
    return _to_schema(menu)

def update_menu(db:Session, menu_body: dict) -> int:
    """
    修改菜单
    """
    menu_id = menu_body.get("menuId")
    menu = db.get(Menu, menu_id)
    if menu is None:
        return 0
    # 传了才更新, 没传保持原值
    if menu_body.get("menuName"):
        menu.menu_name = menu_body["menuName"]
    if menu_body.get("parentId") is not None:
        menu.parent_id = menu_body["parentId"]
    if menu_body.get("menuSort") is not None:
        menu.menu_sort = menu_body["menuSort"]
    if menu_body.get("path") is not None:
        menu.path = menu_body["path"]
    if menu_body.get("component") is not None:
        menu.component = menu_body["component"]
    if menu_body.get("menuType"):
        menu.menu_type = menu_body["menuType"]
    if menu_body.get("icon") is not None:
        menu.icon = menu_body["icon"]
    db.commit()
    return 1

def delete_menu_by_menu_id(db:Session, menu_id: int) -> int:
    """
    删除菜单
    """
    menu = db.get(Menu, menu_id)
    if menu is None:
        return 0
    db.delete(menu)
    from sqlalchemy import delete as sa_delete
    # 同时删除角色菜单关联(保持数据库干净)
    db.execute(sa_delete(RoleMenu).where(RoleMenu.menu_id == menu_id))
    db.commit()
    return 1

def select_menu_list_by_role_id(db:Session, role_id: int) -> list[int]:
    """
    根据角色ID查询菜单ID列表(该角色勾选的菜单)
    """
    return list(
        db.execute(select(RoleMenu.menu_id).where(RoleMenu.role_id == role_id)).scalars().all()
    )

def build_menu_dict_tree(menus: list[Menu]) -> list[dict]:
    """
    把平铺的菜单列表构建成树形结构的字典列表
    构建思路:
    1. 把所有的菜单放进字典(menu_id => 菜单字段), 方便查找
    2. 遍历每个菜单: 父ID=0的是根节点; 否则挂到父菜单的children下
    """
    # 步骤1: 把菜单列表变成字典, 方便根据ID快速查找
    menu_map: dict[int, dict] = {}
    for menu in menus:
        menu_map[menu.menu_id] = _to_schema(menu)

    # 步骤2: 构建树形结构(父子关系)
    root_menus: list[dict] = []  # 存储所有的根节点菜单
    for menu in menus:
        data = menu_map[menu.menu_id]
        # 判断是否是根节点菜单(父ID=0)
        if menu.parent_id == 0:
            # 根节点: 直接添加到根菜单列表
            root_menus.append(data)
        else:
            # 不是根节点: 找到它的父菜单, 把自己加入到父菜单children中
            parent = menu_map.get(menu.parent_id)
            if parent is not None:
                parent.setdefault("children", []).append(data)

    # 步骤3: 清理空的children(没有子菜单的节点不需要children字段)
    def clean_empty(nodes: list[dict]):
        for node in nodes:
            if not node.get("children"):
                node.pop("children", None)
            else:
                clean_empty(node["children"])

    clean_empty(root_menus)
    return root_menus


def build_menu_tree_select(menus: list[Menu]) -> list[dict]:
    """
    构建前端所需要的下拉树结构
    转换: {menuId, menuName, children} => {id, label, children}
    """
    # 先构建成普通树结构
    tree = build_menu_dict_tree(menus)

    # 再把字段名转换成下拉树需要的格式
    def convert(nodes: list[dict]) -> list[dict]:
        result = []
        for node in nodes:
            item = {"id": node["menuId"], "label": node["menuName"]}
            if node.get("children"):
                # 递归转换子节点
                item["children"] = convert(node["children"])
            result.append(item)
        return result

    return convert(tree)

def select_menu_tree_router_by_user_id(db: Session, user_id: int) -> list[dict]:
    """
    根据用户ID查询该用户的菜单树并且构建成前端需要的路由格式
    """
    # 步骤1: 判断用户身份, 获取对应平铺的菜单列表数据
    role_id = select_role_id_by_user_id(db, user_id)
    if role_id == RoleIdConstants.ADMIN_ROLE_ID:
        # 管理员显示所有菜单信息
        menus = select_menu_list_by_user_id(db, None, None)
    else:
        menus = select_menu_list_by_user_id(db, None, user_id)

    # 步骤2: 构建树形结构(父子关系)
    menu_map: dict[int, Menu] = {}
    for m in menus:
        menu_map[m.menu_id] = m
    # 给每个菜单准备children容器
    children_map: dict[int, list[Menu]] = {m.menu_id: [] for m in menus}
    root_menus: list[Menu] = []
    for m in menus:
        if m.parent_id == 0:
            root_menus.append(m)
        else:
            parent = menu_map.get(m.parent_id)
            if parent is not None:
                children_map[parent.menu_id].append(m)

    # 步骤3: 把构建好的树形菜单转换成前端需要的路由格式
    return build_menus(root_menus, children_map)

def build_menus(menus: list[Menu], children_map: dict[int, list[Menu]]) -> list[dict]:
    """
    构建前端需要的路由格式
    """
    routers: list[dict] = []
    for menu in menus:
        # 1.路由的名称(name属性): 顶级菜单加菜单ID后缀保证唯一
        router_name = menu.path or ""
        if menu.parent_id == 0 and menu.menu_id is not None:
            router_name = f"{menu.path}_{menu.menu_id}"

        # 2.路由的访问路径(path属性)
        router_path = menu.path or ""
        if menu.parent_id == 0 and menu.menu_type == "M":
            # 一级目录的路径需要以斜杠开头: "system" -> "/system"
            router_path = "/" + (menu.path or "")
        elif menu.parent_id == 0 and menu.menu_type == "C":
            # 一级菜单的路径设置为根路径
            router_path = "/"

        # 3.路由对应的组件(component)
        component = "Layout"
        if menu.component and not (menu.parent_id == 0 and menu.menu_type == "C"):
            # 菜单配置了组件, 并且不是一级C类型菜单 => 使用菜单配置的组件路径
            component = menu.component
        elif not menu.component and menu.parent_id != 0 and menu.menu_type == "M":
            # 没配置组件, 但是是二级以上的目录 => 使用ParentView
            component = "ParentView"

        # 4.组装路由对象(空值不放入)
        router: dict = {"name": router_name, "path": router_path, "component": component}
        # 路由元数据meta: 标题 + 图标
        router["meta"] = {"title": menu.menu_name, "icon": menu.icon}

        # 5.处理子菜单(递归处理)
        c_menus = children_map.get(menu.menu_id, [])
        if c_menus and menu.menu_type == "M":
            # 当前菜单中有子菜单, 并且它是目录(M)
            router["alwaysShow"] = True
            router["children"] = build_menus(c_menus, children_map)
        elif menu.parent_id == 0 and menu.menu_type == "C":
            # 特殊情况: 一级菜单(C类型) => 包一层子路由
            children: list[dict] = [{
                "path": menu.path,
                "component": menu.component,
                "name": menu.path,
                "meta": {"title": menu.menu_name, "icon": menu.icon, "path": menu.path}
            }]
            router["children"] = children
            # 一级菜单情况: 副路由不显示meta
            router.pop("meta", None)

        routers.append(router)

    return routers