<template>
  <div>
    <!-- 顶部导航栏 -->
    <el-header
        style="background-color: #fff;height: 50px;display: flex;position: fixed; left: 0;right: 0;box-shadow: 0 1px 4px rgba(0,23,45,0.08)">
      <div style="display: flex; align-items: center">
        <img :src="logo" alt="" style="width: 40px; height: 40px;margin-right: 12px">
        <span style="font-weight: bold; font-size: 28px">后台管理端</span>
      </div>

      <div style="flex: 1;display: flex; margin-left: 20px">
        <el-breadcrumb separator="/" style="align-items: center; flex:1;display: flex">
          <el-breadcrumb-item v-for="(item, index) in breadItems" :key="index">{{ item.meta.title }}
            <span>{{ item.meta.title }}</span>
          </el-breadcrumb-item>
        </el-breadcrumb>

        <div style="display: flex; align-items: center">
          <span style="margin-right: 15px">您好：{{ userStore.name }}</span>

          <el-button type="text" @click="logout">
            <svg-icon icon-class="退出登录"/>
            <span>退出登录</span>
          </el-button>

            <el-dropdown trigger="click" style="cursor: pointer">
              <div>
                <img :src="userStore.avatar" alt="" style="width: 36px; height: 36px">
                <el-icon class="el-icon--right">
                  <arrow-down/>
                </el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <router-link to="/user/profile">
                    <el-dropdown-item>个人中心</el-dropdown-item>
                  </router-link>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
        </div>
      </div>
    </el-header>
  </div>
</template>

<script setup>
import logo from '@/assets/logo/logo.png'
import useUserStore from '@/stores/modules/userStore'
import {useRoute} from "vue-router";
import {onMounted, ref, watch} from "vue";
import {ElMessageBox} from "element-plus";
import {ArrowDown} from "@element-plus/icons-vue";
import SvgIcon from "@/components/SvgIcon/index.vue";

const route = useRoute()

//退出登录
const logout = () => {
   ElMessageBox.confirm(
    '确定退出登录吗?',
    '系统提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      userStore.logOut().then(() => {
        //退出成功之后直接跳转到登录页
        location.href = '/login'
      })
    })
}
//用户状态信息
const userStore = useUserStore()

// 面包屑数据
const breadItems = ref([])

//判断当前路由是否是首页
const isDashboard = (route) => {
  const name = route && route.name
  if (!name) return false
  return name.trim() === 'Index'
}

//获取面包屑数据
const getBread = () => {
  //1.从当前的路由匹配数组中过滤出我们需要显示的面包屑
  const matched = route.matched.filter(item => {
    item.meta && item.meta.title
  })

  //2.如果不是首页，就要在最前面添加首页项
  if (!isDashboard(matched[0])) {
    matched.unshift({
      path: 'Index',
      meta: {title: '首页'}
    })
  }

  //3.更新面包屑数组
  breadItems.value = matched

}
//组件挂载后执行
onMounted(() => {
  getBread()
})

//监听路由变化
watch(() => route.path, () => {
  getBread()
})

</script>

<style scoped>

</style>