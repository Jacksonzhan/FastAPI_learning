import bcrypt

"""
bcrypt特点：
1.同一个密码每次加密的结果都不一样(自带随机盐)
2.无法从密文反推明文
3.校验时用checkpw对比明文和密文
"""

def encrypt_password(password: str) -> str:
    """
    加密密码
    :param password: 明文密码
    :return: 密文密码
    """
    # 1.把明文编码成字节
    password = password.encode('utf-8')
    # 2.生成盐(括号中的数字越大越安全，但是越大也越慢)
    salt = bcrypt.gensalt(rounds=12)
    # 3.对密码进行加密
    encrypted_password = bcrypt.hashpw(password, salt)
    # 4.返回加密后的密码
    return encrypted_password.decode('utf-8')

def matches_password(password: str, hashed: str) -> str:
    """
    校验密码是否正确
    :param password: 用户输入的明文密码
    :param hashed: 数据库中存储的密文
    :return:true = 密码正确，flase = 密码不同
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        #密文错误(比如数据库里存的是旧数据)，直接返回密码错误
        return False

def get_user_id(current_user: dict) -> int:
    """
    从当前登录用户中获取用户ID
    :param current_user: 当前用户信息
    :return: 用户ID
    """
    user_id = current_user.get("userId")
    if user_id is None:
        raise SyntaxError("获取用户信息失败")
    return user_id