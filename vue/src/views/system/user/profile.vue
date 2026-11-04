<template>
  <div style="text-align: center;margin: 20px auto;max-width: 500px;">
    <div>
      <el-upload
          class="avatar-uploader"
          :action="uploadUrl"
          :headers="headers"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :on-error="handleAvatarError"
          :before-upload="beforeUpload"
      >
        <img :src="userStore.avatar" class="avatar" alt=""/>
      </el-upload>

    </div>
    <ul class="list-group" style="display: inline-block; text-align: left; width: 100%;max-width: 300px">
      <li class="list-group-item">
        用户名称
        <div class="pull-right">{{ userStore.name }}</div>
      </li>
      <li class="list-group-item">
        性别
        <div class="pull-right" v-if="state.user.sex === 0">男</div>
        <div class="pull-right" v-else>女</div>
      </li>
    </ul>
    <div style="margin-top: 20px">
      <el-button type="primary" @click="editUserInfo">修改基本资料</el-button>
      <el-button type="primary" @click="editPassword">修改密码</el-button>
    </div>

    <!--  基本资料修改对话框  -->
    <vxe-modal title="修改基本资料" v-model="userInfoOpen" width="500px" showFooter show-maximize resize>
      <el-form ref="userRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="userName">
          <el-input v-model="form.userName"/>
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <el-radio-group v-model="form.sex">
            <el-radio :value="0">男</el-radio>
            <el-radio :value="1">女</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <div>
          <el-button type="primary" @click="submitUserInfo">保存</el-button>
          <el-button @click="userInfoOpen = false">取消</el-button>
        </div>
      </template>
    </vxe-modal>

    <!--  修改密码对话框  -->
    <vxe-modal title="修改密码" v-model="pwdOpen" width="500px" showFooter show-maximize resize>
      <el-form ref="pwdRef" :model="pwdForm" :rules="pwdRules" label-width="80px">
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input v-model="pwdForm.oldPassword" placeholder="请输入旧密码"/>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="pwdForm.newPassword" placeholder="请输入新密码"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="pwdForm.confirmPassword" placeholder="请确认密码"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div>
          <el-button type="primary" @click="submitPassword">保存</el-button>
          <el-button @click="pwdOpen = false">取消</el-button>
        </div>
      </template>
    </vxe-modal>

  </div>
</template>

<script setup>
import useUserStore from "@/stores/modules/userStore.js";
import {onMounted, reactive, ref} from "vue";
import {getInfo} from "@/api/login.js";
import {getToken} from "@/utils/auth.js";
import {ElMessage} from "element-plus";
import {updateProfile} from "@/api/system/user.js";

//修改密码表单实例
const pwdRef = ref()

//修改密码的对话框是否打开
const pwdOpen = ref(false)

//修改密码按钮
const editPassword = () => {
  pwdOpen.value = true
}

//修改密码的表单参数
const pwdForm = ref({
  oldPassword: null,
  newPassword: null,
  confirmPassword: null
})

//修改密码的表单校验
const pwdRules = ref({
  oldPassword: [
    {required: true, message: '请输入旧密码', trigger: 'blur'}
  ],
  newPassword: [
    {required: true, message: '请输入新密码', trigger: 'blur'}
  ],
  confirmPassword: [
    {required: true, message: '请确认新密码', trigger: 'blur'}
  ],
})

//提交修改密码
const submitPassword = () => {
  if (pwdForm.value.newPassword !== pwdForm.value.oldPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  pwdRef.value.validate(valid => {
    if (valid) {
      updatePwd(pwdForm.value).then(res => {
        ElMessage.success('修改成功')
        pwdOpen.value = false
      })
    }
  })
}

//修改基本资料的表单实例
const userRef = ref()

//用户资料表单
const form = ref({})

//表单校验
const rules = ref({
  userName: [
    {required: true, message: '请输入用户名', trigger: 'blur'}
  ]
})

//修改基本资料的对话框是否打开
const userInfoOpen = ref(false)

//修改基本资料按钮
const editUserInfo = () => {
  userInfoOpen.value = true
}

//提交用户修改信息
const submitUserInfo = () => {
  userRef.value.validate(valid => {
    if (valid) {
      updateProfile(form.value).then(res => {
        userInfoOpen.value = false
        ElMessage.success('修改成功')
        getUser()
        //同步更新顶部栏显示的用户名
        userStore.name = form.value.userName
      })
    }
  })
}

//头像上传接口地址
const uploadUrl = import.meta.env.VITE_APP_BASE_API + "/system/user/profile/avatar"

//请求头部
const headers = {Authorization: "Bearer " + getToken()}

//用户状态
const userStore = useUserStore()

//数据状态
const state = reactive({
  user: {}
})

//上传前处理
const beforeUpload = (file) => {
  const isJpg = file.type === 'image/jpeg' || file.type === 'image/png'

  if (!isJpg) {
    ElMessage.error('上传头像图片只能是jpg或者png格式!')
  }

  return isJpg
}

//处理上传成功
const handleAvatarSuccess = (res) => {
  if (res.code === 200) {
    userStore.avatar = import.meta.env.VITE_APP_BASE_API + res.imgUrl
  } else {
    ElMessage.error(res.msg || '修改失败')
  }
}

//处理上传失败
const handleAvatarError = () => {
  ElMessage.error('上传失败')
}

//获取用户信息
const getUser = () => {
  getInfo().then(res => {
    state.user = res.data
    console.log(state.user, '看看更新后的信息');
    form.value = {
      userName: state.user.userName,
      sex: state.user.sex
    }
  })
}

//组件挂载后执行
onMounted(() => {
  getUser()
})
</script>

<style scoped>
.list-group {
  padding-left: 0;
  list-style: none;
}

.pull-right {
  float: right;
}

.list-group-item {
  margin-bottom: -1px;
  padding: 11px 0;
  font-size: 14px;
}

.avatar-uploader .avatar {
  width: 120px;
  height: 120px;
  display: block;
  border-radius: 50%;
}
</style>
