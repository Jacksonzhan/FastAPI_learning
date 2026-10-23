from fastapi import FastAPI
from app.core.config import settings
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import index, login, user
from loguru import logger

from app.core.exception_handler import register_exception_handlers

# ./.venv/bin/python -m uvicorn app.main:app --reload --port 8080
# curl -i "http://127.0.0.1:8080/testSuccess" -H "Origin: http://127.0.0.1:90"
# 创建fastapi应用实例(整个后端就靠它干活)


app = FastAPI(title = "FastAPI权限系统",
              docs_url="/docs",
              redoc_url="/redoc")
# 注册路由(以后每写一个路由文件，就在这里注册一次)
app.include_router(index.router)
app.include_router(login.router)
app.include_router(user.router)
#注册全局异常处理器：
register_exception_handlers(app)
# 跨域配置
# 这个配置就是告诉浏览器: "允许外部网站访问我"
app.add_middleware(
    CORSMiddleware,
    # 1.允许哪些来源访问(正则.*表示允许所有来源)
    # 注意: 要配合下面的credentials=True, 必须用正则方式, 写allow_origins=["*"]是不生效的
    allow_origin_regex=".*",
    # 2.允许携带凭证(如cookies、HTTP认证信息)
    allow_credentials=True,
    # 3.允许哪些HTTP方法(GET POST PUT DELETE等等)
    allow_methods=["*"],
    # 4.允许携带哪些请求头
    allow_headers=["*"],
    # 5.预检请求的缓存时间(秒): 浏览器发送复杂请求前会先发OPTIONS预检请求, 1800秒内不用重复发
    max_age=1800,
)

# 静态资源挂载
# 比如访问 /profile/logo.png => 读取 ./file/logo.png
# 把配置里的路径变成path路径
profile_dir = Path(settings.fast_profile)
# 路径没有就创建，有就直接访问
profile_dir.mkdir(parents=True, exist_ok=True)
# 完成挂载
app.mount("/profile", StaticFiles(directory=profile_dir), name="profile")


# 后端启动标识: 应用启动完成后自动执行
@app.on_event("startup")
async def startup():
    banner = (
        "\n------------------------------------------\n"
        "  FastAPI权限系统 启动成功!\n"
        f"  接口文档地址: http://localhost:{settings.server_port}/docs\n"
        f"  后端首页地址: http://localhost:{settings.server_port}/\n"
        "------------------------------------------"
    )
    logger.info(banner)