<template>
  <div style="text-align: center">
    <h1>该网页不存在</h1>
    <el-button type="primary" @click="router.go(-1)">返回</el-button>
  </div>
</template>

<script setup>
import {useRouter} from "vue-router";

//路由实例
const router = useRouter()

</script>

<style scoped>

</style>
