"""
全局异常处理
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ajax_error

class ServiceError(Exception):
    """
    业务异常
    作用：业务逻辑中主动抛出(比如“用户名已存在”)
    """
    def __init__(self, message: str):
        self.message = message

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ServiceError)
    async def handle_service_error(request: Request, exc: ServiceError):
        """
        处理异常
        比如：用户名已存在、密码错误等预期内的问题
        返回：{ "code": 500,"msg": "用户名已存在"}
        """
        logger.info(f"系统异常: {exc.message}")
        return JSONResponse(status_code=200, content=ajax_error(exc.message))

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        """
        处理HTTP异常
        比如：404、500等预期内的问题
        返回：{ "code": 500,"msg": "服务器错误"}
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "msg": exc.detail}
        )