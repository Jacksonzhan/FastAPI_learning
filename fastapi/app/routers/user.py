"""
用户信息
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.common import ajax_success

router = APIRouter(prefix="/system/user", dependencies=[Depends(get_current_user)])

@router.get("/test")
def test(db: Session = Depends(get_db)):
    return ajax_success(data="需要登录才能看到我")