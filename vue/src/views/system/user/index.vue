<template>
  <div class="app-container">
    <!-- 顶部查询 -->
    <el-form :model="query" ref="queryRef" label-width="70px" inline>
      <el-form-item label="用户名称" prop="userName">
        <el-input v-model="query.userName" placeholder="请输入用户名称"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 顶部按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleInsert">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" @click="">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" @click="">删除</el-button>
      </el-col>
    </el-row>

    <!-- 列表 -->
    <el-table :data="userList" style="width: 100%" border @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column prop="userId" label="用户编号" width="180" align="center"/>
      <el-table-column prop="userName" label="用户名" align="center"/>
      <el-table-column prop="sex" label="性别" align="center">
        <template #default="scope">
          <span v-if="scope.row.sex === 0">男</span>
          <span v-else-if="scope.row.sex === 1">女</span>
          <span v-else>未设置</span>
        </template>
      </el-table-column>
      <el-table-column prop="roleName" label="对应角色" align="center"/>
      <el-table-column prop="avatar" label="头像" align="center">
        <template #default="scope">
          <el-avatar :size="50" :src="scope.row.avatar ? baseUrl + scope.row.avatar : defaultAvatar"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="200">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button link type="danger" icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <pagination :total="total"
                v-model:page="query.pageNum"
                v-model:limit="query.pageSize"
                @pagination="getList"
    />

    <!--  新增或修改用户对话框  -->
    <vxe-modal :title="title" v-model="open" width="500px" showFooter show-maximize resize>
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
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" placeholder="请输入密码"/>
        </el-form-item>
        <el-form-item label="对应角色" prop="roleId">
          <el-select v-model="form.roleId" placeholder="请选择角色">
            <el-option v-for="role in roleList"
                       :key="role.roleId"
                       :label="role.roleName"
                       :value="role.roleId"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="open = false">取消</el-button>
        </div>
      </template>
    </vxe-modal>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import {insertUser, selectUserList, selectUserByUserId, updateUser} from "@/api/system/user.js";

//表单实例
const userRef = ref()

//对话框是否打开
const open = ref(false)

//对话框名称
const title = ref('')

//表单参数
const form = ref({
  userId: null,
  userName: null,
  sex: null,
  password: null,
  roleId: null
})

//表单校验
const rules = ref({
  userName: [
    {required: true, message: '请输入用户名', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'}
  ],
  roleId: [
    {required: true, message: '请选择对应角色', trigger: 'change'}
  ]
})

//新增按钮
const handleInsert = () => {
  form.value = {
    userId: null,
    userName: null,
    sex: null,
    password: null,
    roleId: null
  }
  open.value = true
  title.value = '新增用户'
}

//修改按钮
const handleUpdate = (row) => {
  const userId = row.userId || ids.value
  //先查询用户信息(回显到表单中)
  selectUserByUserId(userId).then(res => {
    form.value = res.data
    open.value = true
    title.value = '修改用户'
  })
}

//保存按钮
const submitForm = () => {
  userRef.value.validate(valid => {
    if (valid) {
      if (form.value.userId != null) {
        //调用修改api
        updateUser(form.value).then(res => {
          ElMessage.success('修改成功')
          open.value = false
          getList()
        })
      } else {
        //调用新增api
        insertUser(form.value).then(res => {
          ElMessage.success('新增成功')
          open.value = false
          getList()
        })
      }
    }
  })
}

//删除按钮
const handleDelete = (row) => {
  const userIds = row.userId || ids.value
  ElMessageBox.confirm(
      '是否确认删除用户?',
      '系统提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        //调用删除api
        deleteUserByUserIds(userIds).then(res => {
          ElMessage.success('删除成功')
          getList()
        })
      })
}

//默认头像
import defaultAvatar from '@/assets/images/profile.png'
import {ElMessage} from "element-plus";
import {selectAllRole} from "@/api/system/role.js";

//后端路径
const baseUrl = import.meta.env.VITE_APP_BASE_API

//顶部查询表单实例
const queryRef = ref()

//查询参数
const query = ref({
  pageNum: 1,
  pageSize: 10,
  userName: null,
})

//用户列表数据
const userList = ref([])

//当前是否未选中单行
const single = ref(true)

//当前是否未选中多行
const multple = ref(true)

//数据总数
const total = ref(0)

//查询数据
const getList = () => {
  selectUserList(query.value).then(res => {
    userList.value = res.rows
    total.value = res.total
  })
}

//已勾选的id数组
const ids = ref([])

//多选时的触发方法
const handleSelectionChange = (selection) => {
  ids.value = selection.map(item => item.userId)
  single.value = selection.length != 1
  multple.value = !selection.length
}

//搜索按钮
const handleQuery = () => {
  query.value.pageNum = 1
  getList()
}

//重置按钮
const resetQuery = () => {
  queryRef.value.resetFields()
  handleQuery()
}

//角色列表数据
const roleList = ref([])

//获取所有角色(只在页面组件挂载时执行一次, 填充下拉框)
const getRoleList = () => {
  selectAllRole().then(res => {
    roleList.value = res.data
  })
}

onMounted(() => {
  getList()
  getRoleList()
  //测试完之后删除

})
</script>

<style scoped>

</style>
