"""
首页路由
"""
from fastapi import APIRouter
from app.core.logger import logger

# 创建一个路由对象(一个路由对象就代表一个借口)
router = APIRouter()

@router.get("/", summary="后端首页")
def home():
    logger.info("访问了首页")
    return "欢迎访问首页！"
