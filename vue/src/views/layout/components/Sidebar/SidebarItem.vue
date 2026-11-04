<template>
  <!-- 第一步: 检查这个菜单项是否应该显示 -->
  <div v-if="!item.hidden">
    <!-- 情况1: 当这个菜单项只需要显示为一个简单的菜单项(没有子菜单) -->
    <template v-if="shouldShowSingleItem">
      <app-link :to="singleItemPath">
        <el-menu-item :index="singleItemPath">
          <svg-icon :icon-class="onlyOneChild.meta.icon || (item.meta && item.meta.icon)"
                    style="margin-right: 10px"/>
          <template #title>
            <span style="margin-left: 2px">
              {{ onlyOneChild.meta.title }}
            </span>
          </template>
        </el-menu-item>
      </app-link>
    </template>

    <!-- 情况2: 当这个菜单项需要显示为有子菜单的折叠菜单 -->
    <el-sub-menu v-else :index="resolvePath(item.path)" teleported>
      <template v-if="item.meta" #title>
        <svg-icon :icon-class="item.meta.icon" style="margin-right: 10px"/>
        <span style="margin-left: 2px">
              {{ item.meta.title }}
        </span>
      </template>

      <!-- 递归渲染子菜单项 -->
      <sidebar-item v-for="child in item.children"
                    :key="child.path"
                    :item="child"
                    :base-path="resolvePath(child.path)"
                    is-next
      />
    </el-sub-menu>
  </div>
</template>

<script setup>
import {computed} from "vue";
import AppLink from "@/views/layout/components/Sidebar/AppLink.vue";
import SvgIcon from "@/components/SvgIcon/index.vue";

const props = defineProps({
  //菜单项的数据对象, 必须传入
  item: {
    type: Object,
    required: true
  },
  //标记是否是嵌套调用
  isNext: {
    type: Boolean,
    default: false
  },
  //基础路径, 用于拼接完整的路由路径
  basePath: {
    type: String,
    default: ''
  }
})

//计算当前菜单项的唯一显示子项
const onlyOneChild = computed(() => {
  //获取当前菜单项的子项数组, 如果没有子项就使用空数组
  const children = props.item.children || []

  //过滤出所有不需要隐藏的子项
  const showingChildren = children.filter(item => !item.hidden)

  //情况1: 如果只有一个需要显示的子项
  if (showingChildren.length === 1) {
    //返回这个唯一的子项
    return showingChildren[0]
  }

  //情况2: 如果没有需要显示的子项
  if (showingChildren.length === 0) {
    return {
      ...props.item, //复制父项的所有属性
      path: '', //路径设置为空
      noShowingChildren: true //标记没有显示的子项
    }
  }

  //情况3: 如果有多个需要显示的子项
  return null
})

//判断是否应该将当前菜单项显示为单个菜单项
const shouldShowSingleItem = computed(() => {
  //条件1: 存在onlyOneChild (有唯一的子项或者没有子项)
  //条件2: 这个唯一的子项没有子菜单, 或者标记了noShowingChildren
  //条件3: 父项没有设置显示为折叠菜单
  return onlyOneChild.value && (!onlyOneChild.value.children || onlyOneChild.value.noShowingChildren)
      && !props.item.alwaysShow
})

//计算单个菜单项点击后应该跳转的完整路径
const singleItemPath = computed(() => {
  return resolvePath(onlyOneChild.value.path)
})

//解析并拼接路由路径, 处理特殊情况
const resolvePath = (routePath) => {
  //拼接基础路径和相对路径
  const fullPath = props.basePath + '/' + routePath

  //如果路径为空, 直接返回
  if (!fullPath) return fullPath

  //处理特殊情况
  return fullPath.replace('//', '/')
      .replace(/\/$/, '')
}

</script>

<style scoped>

</style>
