"""
系统日志配置
作用：配置项目统一的日志输出
loguru的好处：开箱即用，输出彩色日志，不用像内置的一样写一堆配置
"""
import sys
from loguru import logger
#移除loguru默认的日志输出配置
logger.remove()

#重新添加控制台输出
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# 同时把日志写入文件(每天一个文件, 最多保留7天)
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="00:00", # 每天0点创建新文件
    retention="7 days", # 日志文件最多保留7天
    encoding="utf-8", # 使用utf-8编码, 避免中文乱码
)