from fastapi import FastAPI
from app.core.logger import logger
from app.core.config import settings

# 创建fastapi应用实例(整个后端就靠它干活)

app = FastAPI(title = "FastAPI权限系统")

# 定义一个接口
@app.get("/")
def home():
    logger.info(f"当前使用的数据库名称：{settings.db_name}")
    # 接口要返回的内容
    return "你好，恭喜你成功启动了后端"