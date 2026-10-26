<template>
  <div class="login-container">
    <div style="display: flex;width: 500px;background: rgba(255,255,255,0.65)">
      <div style="flex: 1;padding: 40px;display: flex;flex-direction: column;justify-content: center">
        <div style="text-align: center">
          <h3 style="font-size: 28px;color: #333">注册</h3>
          <p style="color: #999;font-size: 14px">请输入您的注册信息</p>
        </div>

        <el-form :model="registerForm" ref="registerRef" :rules="rules">
          <el-form-item prop="userName">
            <el-input v-model="registerForm.userName" size="large" placeholder="请输入用户名"/>
          </el-form-item>
          <el-form-item prop="password">
            <el-input show-password v-model="registerForm.password" size="large" placeholder="请输入密码"/>
          </el-form-item>
          <el-form-item prop="confirmPassword">
            <el-input show-password v-model="registerForm.confirmPassword" size="large" placeholder="请确认密码"/>
          </el-form-item>

          <el-form-item style="width: 100%;">
            <el-button type="primary"
                       style="width: 100%;"
                       :loading="loading"
                       @click="handleRegister"
            >注册
            </el-button>
          </el-form-item>

        </el-form>

      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {register} from "@/api/register.js";
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";

//加载状态
const loading = ref(false)

//表单实例
const registerRef = ref()

//表单参数
const registerForm = ref({
  userName: null,
  password: null,
  confirmPassword: null
})

//验证两次密码输入是否相同
const equalToPassword = (rule, value, callback) => {
  if (registerForm.value.password !== value) {
    callback(new Error('两次输入的密码不一致'))
  }else {
    callback()
  }
}

//表单校验
const rules = ref({
  userName: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入您的密码', trigger: 'blur' },
    { required: true, validator: equalToPassword, trigger: 'blur' }
  ],
})

//路由实例
const router = useRouter()

//注册方法
const handleRegister = () => {
  registerRef.value.validate(valid => {
    if (valid) {
      //打开加载状态
      loading.value = true
      //调用注册接口
      register(registerForm.value).then(res => {
        ElMessage.success('恭喜你, 你的账号' + registerForm.value.userName + "注册成功")
        router.push('/login')
      }).catch(() => {
        loading.value = false
      })
    }
  })
}

</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: url("@/assets/images/background.jpg") no-repeat center;
  background-size: cover;
  position: relative;
}
</style>
