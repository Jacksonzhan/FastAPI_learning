"""
公共依赖
作用：提供整个项目通用的依赖注入函数
相当于系统的安检员 - 检查每个访客的通行证（token)，验证通过才放行
"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core import token_service

# 安全方案: Bearer Token
# 声明成 HTTPBearer 后, FastAPI 会自动写入 openapi.json, Swagger 右上角就会出现 Authorize 按钮
# auto_error=False: 缺少请求头时不在框架层报错, 继续往下走统一返回"登录已过期"
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict:
    # 步骤1: 从请求头中提取token
    authorization = f"Bearer {credentials.credentials}" if credentials else None
    token = token_service.get_token(authorization)

    # 步骤2: 解析token, 获取用户信息
    login_user = token_service.get_login_user(token)
    if login_user is None:
        raise HTTPException(status_code=401, detail="登录已过期, 请重新登录")

    # 步骤3: 验证token是否过期
    if not token_service.verify_token(login_user):
        raise HTTPException(status_code=401, detail="登录已过期, 请重新登录")

    # 步骤4: 验证通过, 返回用户信息
    return login_user