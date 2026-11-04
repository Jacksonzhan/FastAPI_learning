<template>
  <div class="container">
    <el-pagination :layout="layout"
                   :total="total"
                   v-model:current-page="currentPage"
                   v-model:page-size="pageSize"
                   :page-sizes="pageSizes"
                   @size-change="handleSizeChange"
                   @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>

//当前页码
const currentPage = defineModel('page', {default: 1})

//每一页的条数
const pageSize = defineModel('limit', {default: 10})

//定义组件接收的参数
const props = defineProps({
  total: {type: Number, required: true},
  pageSizes: {type: Array, default: () => [10, 20, 30, 50]},
  layout: {type: String, default: 'total, prev, pager, next, jumper, sizes'}
})

//定义组件可以发出的事件
//这里定义了一个'pagination'事件, 当分页变化时触发
const emit = defineEmits(['pagination'])

//处理每页条数变化的函数
const handleSizeChange = (val) => {
  //检查特殊情况
  //如果改变每页条数后, 当前页码 * 新条数 > 总条数
  //说明当前页码已经超过了有效范围(没有那么多页了)
  if (currentPage.value * val > props.total) {
    //重置为第一页
    currentPage.value = 1
  }

  //向父组件发出pagination事件
  //携带两个参数: 当前页码和新的每页条数
  emit('pagination', {page: currentPage.value, limit: val})
}

//处理页码变化时的函数
const handleCurrentChange = (val) => {
  emit('pagination', {page: val, limit: pageSize.value})
}

</script>

<style scoped>
.container {
  padding: 30px 15px;
  display: flex;
  justify-content: flex-end;
}
</style>
