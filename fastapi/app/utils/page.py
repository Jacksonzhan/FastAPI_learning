"""
分页工具
作用：封装通用的分页参数处理和分页结果封装
"""

def start_page(page_num: int | None, page_size: int | None) -> tuple[int, int]:
    """
    设置请求分页数据, 计算真实的页码和每页条数
    :param page_num: 前端传的页码
    :param page_size: 前端传的每页条数
    :return: (页码, 每页条数)

    合理化分页:
    - 当pageNum<=0时, 自动设置为第1条
    - 当pageSize<=0时, 自动设置为10条
    """
    page_num = page_num if page_num and page_num > 0 else 1
    page_size = page_size if page_size and page_size > 0 else 10
    return page_num, page_size

def get_data_table(rows: list, total: int) -> dict:
    """
    组装分页结果
    :param rows: 当前页的列表数据
    :param total: 数据总数
    :return: 数据返回格式(包含数据)
    """
    return {
        "total": total,
        "rows": rows,
        "code": 200,
        "msg": "查询列表成功"
    }