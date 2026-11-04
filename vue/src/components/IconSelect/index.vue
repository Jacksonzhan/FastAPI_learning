<template>
  <!--
    外层容器，固定高度200像素。
    为什么要固定高度？因为这个选择器通常会作为弹窗或下拉框的内容区域，
    固定高度可以防止它无限扩张，同时内容超出时会自动出现滚动条。
  -->
  <div style="height: 200px;">
    <!--
      Flex布局容器：
      display: flex -> 启用弹性布局，子元素会排成一行
      flex-wrap: wrap -> 允许子元素换行，当一行放不下时会自动换到下一行
      这个容器将负责排列所有的图标项目
    -->
    <div style="display: flex; flex-wrap: wrap;">
      <!--
        v-for循环：遍历iconList数组，为每个图标创建一个div
        item: 当前遍历的图标名称（如"home"、"user"）
        @click="selectedIcon(item)": 点击图标时调用selectedIcon函数
      -->
      <div
          v-for="(item, index) in iconList"
          class="icon-item-wrapper"
          :key="index"
          @click="selectedIcon(item)"
      >
        <!-- 图标内容容器：图标本身 + 图标名称文字 -->
        <div class="icon-item">
          <!-- 自定义svg图标组件, 根据名称显示对应svg -->
          <svg-icon :icon-class="item" style="height: 25px; width: 16px;"/>
          <!-- 显示图标名称, 方便识别 -->
          <span>{{ item }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// 动态导入所有SVG图标
/*
  问题：我们有很多SVG图标文件，怎么自动获取所有图标？
  解决：使用Vite的import.meta.glob功能

  什么是import.meta.glob？
  - 这是Vite构建工具提供的功能（Webpack也有类似功能）
  - 它可以批量导入匹配特定模式的文件
  - 返回一个对象，键是文件路径，值是一个异步导入函数

  示例：
  假设icons文件夹下有: home.svg, user.svg, settings.svg
  那么modules对象会是：
  {
    '@/assets/icons/svg/home.svg': () => import('@/assets/icons/svg/home.svg'),
    '@/assets/icons/svg/user.svg': () => import('@/assets/icons/svg/user.svg'),
    ...
  }
*/
const modules = import.meta.glob('@/assets/icons/svg/*.svg');

// 处理图标路径，提取纯名称
/*
  步骤拆解：
  1. Object.keys(modules) -> 获取所有文件路径的数组
  2. path.split('assets/icons/svg/')[1] -> 'home.svg'
  3. .split('.svg')[0] -> 'home'

  最终icons是一个字符串数组：['home', 'user', 'settings', ...]
*/
const icons = Object.keys(modules).map(path =>
    path.split('assets/icons/svg/')[1].split('.svg')[0]
);

// 图标列表
const iconList = ref(icons);

/*
  定义这个组件可以触发什么事件
  子组件通过emit('事件名', 参数)通知父组件
  父组件监听: <icon-select @selected="handleSelected" />
*/
const emit = defineEmits(['selected']);

/*
  图标点击处理函数
  1. 触发'selected'事件，把图标名称传给父组件
  2. document.body.click(): 模拟点击body, 触发el-popover的关闭逻辑
*/
const selectedIcon = (name) => {
  // 通知父组件：用户选择了哪个图标
  emit('selected', name);

  // 模拟点击body，用于关闭下拉框
  document.body.click();
};
</script>

<style scoped>
/* 每个图标容器：占1/3宽度，固定高度 */
.icon-item-wrapper {
  width: calc(100% / 3);  /* 一行显示3个图标 */
  height: 25px;           /* 固定高度 */
  line-height: 25px;      /* 文字垂直居中 */
  cursor: pointer;        /* 鼠标指针变为手型 */
  display: flex;          /* 内部使用flex布局 */
}

/* 图标内容区域 */
.icon-item {
  display: flex;          /* 图标和文字水平排列 */
  max-width: 100%;        /* 防止内容溢出 */
  height: 100%;           /* 继承父容器高度 */
  padding: 0 5px;         /* 左右内边距 */
}

/* 鼠标悬停效果 */
.icon-item:hover {
  background: #ececec;    /* 浅灰色背景 */
}
</style>
