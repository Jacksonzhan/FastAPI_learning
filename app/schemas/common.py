"""
操作消息提醒(统一响应格式)
作用：规定所有接口统一返回{code, msg, data}
"""

def ajax_success(msg: str = "操作成功", data = None, **extra) -> dict:
    result = {"code":200, "msg": msg}
    """
    返回成功消息
    ：param msg: 返回信息
    ：param data: 数据对象(没有数据时为None，不会出现在响应走)
    ：param extra: 额外的顶层字段(比如登陆接口需要额外返回Token)
    """
    if data is not None:
        result["data"] = data
    # 把额外字段平铺到顶层(比如token, imgUrl)
    result.update(extra)
    return result

def ajax_error(msg: str = "操作失败", code: int = 500) -> dict:
    """
    返回错误消息
    :param msg:
    :param code:
    """
    return {"code":code, "msg": msg}

def to_ajax(rows: int) -> dict:
    return ajax_success("操作成功") if rows > 0 else ajax_error("操作失败")
