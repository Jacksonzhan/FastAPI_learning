"""
个人信息(个人头像图片上传)
"""
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.db.session import get_db
from app.schemas.common import ajax_error, ajax_success, to_ajax
from app.schemas.login import UpdateProfileBody, SubmitPwdBody
from app.services import user_service
from app.utils.security_utils import get_user_id, matches_password
from loguru import logger

# 路由前缀
router = APIRouter(prefix="/system/user/profile", dependencies=[Depends(get_current_user)])


@router.post("/avatar")
async def avatar(
        file: UploadFile = File(...),
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    头像上传
    """
    # 第一步: 检查用户是否上传了文件
    if file is None or not file.filename:
        return ajax_error("上传头像失败, 请重新上传")

    # 第二步: 获取当前登录用户的信息
    user_id = get_user_id(current_user)

    # 第三步: 准备存放头像文件的文件夹
    upload_dir = Path(settings.fast_profile + "/avatar")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # 第四步: 为上传的文件生成一个唯一的文件名
    original_filename = file.filename
    extension = ""
    if "." in original_filename:
        extension = original_filename[original_filename.rfind("."):]
    # 拼接一个uuid
    unique_filename = uuid.uuid4().hex + extension
    logger.info(unique_filename + "这里打印")


    # 第五步: 将文件保存到服务器的硬盘上
    file_path = upload_dir / unique_filename
    content = await file.read()
    file_path.write_bytes(content)

    # 第六步: 构建头像的访问路径(给前端用的地址)
    avatar_url = f"/profile/avatar/{unique_filename}"

    # 第七步: 更新数据库中的用户头像信息
    if user_service.update_user_avatar(db, user_id, avatar_url) > 0:
        # 第八步: 准备返回给前端的成功响应
        return ajax_success(imgUrl=avatar_url)

    # 第九步: 上传失败(数据库更新失败)
    return ajax_error("上传头像失败, 请重新上传")

@router.put("")
def update_profile(
        body: UpdateProfileBody,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    修改个人信息
    """
    # 获取当前用户的ID
    user_id = get_user_id(current_user)
    #调用服务层更新用户信息(用户名和性别)
    return to_ajax(user_service.update_profile(db, user_id, body.user_name, body.sex))

@router.put("/updatePwd")
def update_pwd(
        body: SubmitPwdBody,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    重置密码
    """
    # 用户输入的旧密码和新密码
    old_password = body.old_password or ""
    new_password = body.new_password or ""

    # 获取当前用户的ID
    user_id = get_user_id(current_user)
    # 数据库当前的密码密文
    db_user = user_service.select_user_by_user_id(db, user_id)
    password = (db_user or {}).get("password") or ""

    logger.info("旧密码")
    logger.info(old_password)

    logger.info("新密码")
    logger.info(password)

    # 校验1: 新密码不能与旧密码相同
    if matches_password(new_password, password):
        return ajax_error("新密码不能与旧密码相同")
    # 校验2: 旧密码是否正确
    if not matches_password(old_password, password):
        return ajax_error("旧密码错误")

    # 修改该用户的密码
    if user_service.reset_user_pwd(db, user_id, new_password) > 0:
        return ajax_success()

    return ajax_error("修改密码失败, 请重新填写后提交")