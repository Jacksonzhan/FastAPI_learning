"""
用户信息
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.common import ajax_success, to_ajax
from app.schemas.user import UserBody
from app.services import user_service
from app.utils import page as page_utils

router = APIRouter(prefix="/system/user", dependencies=[Depends(get_current_user)])


@router.get("/selectUserList")
def select_user_list(
        page_num: int | None = Query(default=None, alias="pageNum"),
        page_size: int | None = Query(default=None, alias="pageSize"),
        user_name: str | None = Query(default=None, alias="userName"),
        db: Session = Depends(get_db)
):
    """
    查询用户列表
    """
    # 步骤1: 启动分页功能(合理化分页参数)
    page_num, page_size = page_utils.start_page(page_num, page_size)
    # 步骤2: 查询用户列表(带角色关联)
    data, total = user_service.select_user_list(db, page_num, page_size, user_name)
    # 步骤3: 组装分页数据返回
    return page_utils.get_data_table(data, total)

@router.post("/insertUser")
def insert_user(body: UserBody, db: Session = Depends(get_db)):
    """
    新增用户
    """
    return to_ajax(user_service.insert_user(db, body.model_dump(by_alias=True)))

@router.get("/selectUserByUserId/{user_id}")
def select_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    根据用户ID查询用户信息
    """
    user = user_service.select_user_by_user_id(db, user_id)
    return ajax_success(data=user)

@router.put("/updateUser")
def update_user(body: UserBody, db: Session = Depends(get_db)):
    """
    修改用户
    """
    return to_ajax(user_service.update_user(db, body.model_dump(by_alias=True)))

@router.delete("/deleteUserByUserIds/{user_ids}")
def delete_user_by_user_ids(user_ids: str, db: Session = Depends(get_db)):
    """
    删除用户(支持批量, 路径参数是逗号分隔的ID: 1,2,3)
    """
    # 把"1,2,3"这样的字符串拆成[1, 2, 3]
    ids = [int(x) for x in user_ids.split(",") if x.strip()]
    return to_ajax(user_service.delete_user_by_user_ids(db, ids))