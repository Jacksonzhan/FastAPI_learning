<template>
  <div>
    <el-header style="background-color: #fff;height: 50px; display: flex; align-items: center;
                position: fixed;left: 0;right: 0;box-shadow: 0 1px 4px rgba(0,23,45,0.08)">
      <div style="display: flex; align-items: center">
        <span style="font-weight: bold; font-size: 22px">用户前台</span>
      </div>
      <div style="flex: 1;display: flex;justify-content: flex-end;align-items: center">
        <span style="margin-right: 15px">您好: {{ userStore.name }}</span>
        <el-button type="text" @click="logout">退出登录</el-button>
      </div>
    </el-header>

    <main style="position: relative;top: 50px">
      <router-view/>
    </main>
  </div>
</template>

<script setup>
import useUserStore from "@/stores/modules/userStore.js";
import {ElMessageBox} from "element-plus";

const userStore = useUserStore()

//退出登录
const logout = () => {
  ElMessageBox.confirm('确定退出系统吗?', '系统提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    userStore.logOut().then(() => {
      location.href = '/login'
    })
  })
}
</script>
