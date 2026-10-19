"""
首页路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import get_db
from sqlalchemy import select
from app.models import User
from app.schemas.common import ajax_success

# 创建一个路由对象(一个路由对象就代表一个借口)
router = APIRouter()

@router.get("/", summary="后端首页")
def home():
    logger.info("访问了首页")
    return "欢迎访问首页！"

@router.get("/testdb")
def test_db(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return ajax_success(data=[u.user_name for u in users])