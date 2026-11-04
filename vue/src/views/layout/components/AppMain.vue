
<template>
<div style="padding: 16px">
  <router-view v-slot="{ Component, route }">
    <el-card style="min-height: calc(100vh - 92px)">
      <component v-if="!route.meta.link" :is="Component" :key="route.path"/>
    </el-card>
  </router-view>
</div>
</template>

<script setup>

</script>

<style scoped>

</style>
