"""
Token验证处理
作用：JWT令牌的生成、解析、验证
相当于整个系统的“身份证制作站和检查站”
"""

import json
import time

import jwt

from app.core.config import settings


def create_token(login_user: dict) -> str:
    """
    创建JWT令牌
    功能：根据用户信息生成token
    使用场景：用户登录成功之后调用

    """
    # 1.获取当前的时间戳(毫秒)
    now = int(time.time() * 1000)

    # 2.计算过期时间(将分钟转换为毫秒)
    expiration_time = now + settings.token_expire_time * 60 * 1000

    # 3.更新用户信息中的时间字段
    login_user["loginTime"] = now # 登录时间
    login_user["expireTime"] = expiration_time  # 过期时间

    # 4.准备JWT的声明数据
    claims = {"user_key": json.dumps(login_user, ensure_ascii=False)}

    # 5.构建JWT token并且返回(用密钥签名，防止造假)
    return jwt.encode(claims,settings.token_secret, algorithm="HS256")

def parse_token(token: str) -> dict | None:
    """
    解析字符串，获取声明数据
    """
    try:
        return jwt.decode(token, settings.token_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        # 签名错误/token过去/格式错误等情况
        return None

def get_login_user(token: str) -> dict | None:
    """
    根据token获取用户信息
    :param token:令牌
    :return: 用户信息字典或者None
    """
    if not token:
        return None #用户未登录
    # 1.解析token，获取声明数据
    claims = parse_token(token)
    if claims is None:
        return None
    # 2.从声明数据中获取存储的用户Json字符串，并且反序列化为字典
    user_json = claims.get("user_key")
    if not user_json:
        return None
    return json.loads(user_json)

def verify_token(login_user: dict) -> bool:
    """
    验证token是否过期
    :return: True=未过期, False=已过期
    """
    return login_user.get("expireTime", 0) > int(time.time() * 1000)

def get_token(authorization: str | None) -> str | None:
    """
    从请求头Authorization的值中提取token
    前端传的格式: "Bearer xxxxx.yyyyy.zzzzz"
    我们要把"Bearer "前缀去掉, 只留token本体
    """
    if not authorization:
        return None
    if authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization