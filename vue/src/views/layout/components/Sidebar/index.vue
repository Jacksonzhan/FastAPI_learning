<template>
  <el-scrollbar>
    <el-menu :default-active="activeMenu" class="sidebar-menu">
      <SidebarItem :item="route"
        v-for="(route, index) in sidebarRouters"
        :key="route.path + index"
        :base-path="route.path"
        />
    </el-menu>
  </el-scrollbar>
</template>

<script setup>
  import {computed, ref} from "vue";
  import {useRoute} from "vue-router";
  import SidebarItem from "@/views/layout/components/Sidebar/SidebarItem.vue";
  import useRouteStore from "@/stores/modules/routeStore.js";

  const route = useRoute()

  const routeStore = useRouteStore()

  //动态路由数据
  const sidebarRouters = computed(() => routeStore.sidebarRouters)

  // //模拟的静态路由数据
  // const sidebarRouters = ref([
  //   {
  //     path: '/index',
  //     meta: {title: '首页', icon: '首页', hidden: false}
  //   },
  //   {
  //     path: '/system',
  //     meta: {title: '系统管理', icon: '系统管理', hidden: false},
  //     children: [
  //       {
  //         path: '/user',
  //         meta: {title: '用户管理', icon: '用户管理', hidden: false}
  //       },
  //       {
  //         path: '/role',
  //         meta: {title: '角色管理', icon: '角色管理', hidden: false}
  //       },
  //       {
  //         path: '/menu',
  //         meta: {title: '菜单管理', icon: '菜单管理', hidden: false}
  //       },
  //     ]
  //   }
  // ])

  //计算当前应该高亮哪个菜单项
  const activeMenu = computed(() => {
    //从当前路由对象中解耦数据
    const {meta, path} = route

    return meta.activeMenu || path
  })
</script>

<style scoped>
  .sidebar-menu {
    padding: 8px 0;
    border-right: none;
  }

  .sidebar-menu :deep(.el-menu-item) {
    color: #606266;
    height: 55px;
  }

  .sidebar-menu :deep(.el-menu-item).is-active {
    background: var(--el-color-primary) !important;
    color: #fff;
    position: relative;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-radius: 8px;
  }
</style>
