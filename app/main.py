from fastapi import FastAPI
from app.core.logger import logger
from app.core.config import settings
from app.schemas.common import ajax_success, ajax_error
from app.schemas.login import LoginBody

# 创建fastapi应用实例(整个后端就靠它干活)

app = FastAPI(title = "FastAPI权限系统")

# 定义一个接口
@app.get("/")
def home():
    logger.info(f"当前使用的数据库名称：{settings.db_name}")
    # 接口要返回的内容
    return "你好，恭喜你成功启动了后端"

@app.get("/testSuccess")
def test_success():
    return ajax_success(data={"name":"小杰"})

@app.get("/testError")
def test_error():
    return ajax_error(msg="操作失败")

@app.post("/testLogin")
def test_login(body: LoginBody):
    return ajax_success(data={"收到用户名":body.user_name, "收到密码":body.password})
