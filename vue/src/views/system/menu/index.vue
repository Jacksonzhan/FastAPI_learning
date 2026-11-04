<template>
  <div class="app-container">
    <!-- 顶部查询 -->
    <el-form :model="query" ref="queryRef" label-width="70px" inline>
      <el-form-item label="菜单名称" prop="menuName">
        <el-input v-model="query.menuName" placeholder="请输入菜单名称"/>
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
    </el-row>

    <!-- 列表 -->
    <el-table :data="menuList" style="width: 100%" border
              row-key="menuId" :tree-props="{ children: 'children', hasChildren: 'hasChildren' }">
      <el-table-column prop="menuName" label="菜单名称" align="center"/>
      <el-table-column prop="icon" label="图标" align="center" width="100">
        <template #default="scope">
          <svg-icon :icon-class="scope.row.icon"/>
        </template>
      </el-table-column>
      <el-table-column prop="menuSort" label="排序" align="center" width="100"/>
      <el-table-column prop="component" label="组件路径" align="center"/>
      <el-table-column label="操作" align="center" width="200">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button link type="danger" icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加或修改菜单对话框 -->
    <vxe-modal :title="title" v-model="open" width="40%" showFooter show-maximize resize>
      <el-form ref="menuRef" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="上级菜单">
              <el-tree-select v-model="form.parentId"
                              :data="menuOptions"
                              :props="{ value: 'menuId', label: 'menuName', children: 'children' }"
                              check-strictly
                              value-key="menuId"
                              placeholder="选择上级菜单"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单类型" prop="menuType">
              <el-radio-group v-model="form.menuType">
                <el-radio value="M">目录</el-radio>
                <el-radio value="C">菜单</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="菜单图标" prop="icon">
              <el-popover
                  placement="bottom-start"
                  :width="550"
                  trigger="click"
              >
                <template #reference>
                  <el-input v-model="form.icon" placeholder="点击选择图标" @blur="">
                    <template #prefix>
                      <!-- 已选图标: 显示图标本体; 未选: 显示搜索图标 -->
                      <svg-icon :icon-class="form.icon" v-if="form.icon" style="height: 32px;width: 16px;"/>
                      <el-icon v-else>
                        <Search/>
                      </el-icon>
                    </template>
                  </el-input>
                </template>
                <icon-select ref="iconSelectRef" @selected="selectedIcon"/>
              </el-popover>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="显示排序" prop="menuSort">
              <el-input-number v-model="form.menuSort" :min="0"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="菜单名称" prop="menuName">
              <el-input v-model="form.menuName" placeholder="请输入菜单名称"/>
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="form.menuType === 'C'">
            <el-form-item label="路由地址" prop="path">
              <el-input v-model="form.path" placeholder="请输入路由地址"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12" v-if="form.menuType === 'C'">
            <el-form-item label="组件路径" prop="component">
              <el-input v-model="form.component" placeholder="请输入组件路径"/>
            </el-form-item>
          </el-col>
        </el-row>
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
import {insertMenu, selectMenuByMenuId, selectMenuList, updateMenu, deleteMenuByMenuId} from "@/api/system/menu.js";
import {ElMessage, ElTreeSelect, ElMessageBox} from "element-plus";
import SvgIcon from "@/components/SvgIcon/index.vue";
import {Search} from "@element-plus/icons-vue";
import IconSelect from "@/components/IconSelect/index.vue";

//图标选择器实例
const iconSelectRef = ref()

//菜单列表
const menuList = ref([])

//顶部查询表单实例
const queryRef = ref()

//查询参数
const query = ref({
  menuName: null
})

//对话框是否打开
const open = ref(false)

//对话框title
const title = ref('')

//表单参数
const form = ref({
  menuId: null,
  parentId: null,
  menuName: null,
  icon: null,
  menuType: "M",
  menuSort: null,
  path: null,
  component: null
})

//表单校验
const rules = ref({
  menuName: [
    {required: true, message: '请输入菜单名称', trigger: 'blur'}
  ],
  menuSort: [
    {required: true, message: '请输入菜单顺序', trigger: 'blur'}
  ],
  path: [
    {required: true, message: '请输入路由顺序', trigger: 'blur'}
  ],
  component: [
    {required: true, message: '请输入组件路径', trigger: 'blur'}
  ],
})

//新增按钮
const handleInsert = () => {
  form.value = {
    menuId: null,
    parentId: null,
    menuName: null,
    icon: null,
    menuType: "M",
    menuSort: null,
    path: null,
    component: null
  }
  getTreeSelect()
  open.value = true
  title.value = '新增菜单'
}

//修改按钮
const handleUpdate = (row) => {
  //先查询菜单信息回显到表单
  selectMenuByMenuId(row.menuId).then(res => {
    form.value = res.data
    getTreeSelect()
    open.value = true
    title.value = '修改菜单'
  })
}

//删除按钮
const handleDelete = (row) => {
  const menuId = row.menuId
  ElMessageBox.confirm(
      '是否确认删除菜单?',
      '系统提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        deleteMenuByMenuId(menuId).then(res => {
          ElMessage.success('删除成功')
          getList()
        })
      })
}

//菜单下拉数据
const menuOptions = ref([])

//查询菜单下拉树结构
const getTreeSelect = () => {
  selectMenuList().then(res => {
    const menu = {menuId: 0, menuName: '主层级', children: []}
    menu.children = buildTree(res.data, 0)
    menuOptions.value = [menu]
  })
}

//搜索按钮
const handleQuery = () => {
  getList()
}

//重置按钮
const resetQuery = () => {
  queryRef.value.resetFields()
  handleQuery()
}

//查询数据
const getList = () => {
  selectMenuList(query.value).then(res => {
    if (query.value.menuName != null) {
      //如果有查询参数(根据菜单名称条件查询), 直接平铺数据
      menuList.value = res.data
    } else {
      //没有查询参数, 构建树形结构展示
      menuList.value = buildTree(res.data, 0)
    }
  })
}

//构建树形结构数据
const buildTree = (data, parentId) => {
  //存放当前层级的所有菜单项
  const result = []
  //遍历所有菜单数据
  for (const item of data) {
    //如果当前菜单的父ID等于传入的parentId, 说明它是当前层级的菜单
    if (item.parentId === parentId) {
      //递归查找当前菜单的所有子菜单
      const children = buildTree(data, item.menuId)
      //如果找到了子菜单
      if (children.length > 0) {
        //将子菜单的数组挂载到当前菜单的children数组属性下
        item.children = children
      }
      //将处理好的菜单项加入到结果数组中
      result.push(item)
    }
  }
  //返回当前层级的所有菜单
  return result
}

//选择图标回调事件
const selectedIcon = (name) => {
  form.value.icon = name
}

//表单实例
const menuRef = ref()

//保存按钮
const submitForm = () => {
  menuRef.value.validate(valid => {
    if (valid) {
      if (form.value.menuId != null) {
        //修改
        updateMenu(form.value).then(res => {
          ElMessage.success('修改成功')
          open.value = false
          getList()
        })
      } else {
        //新增
        insertMenu(form.value).then(res => {
          ElMessage.success('新增成功')
          open.value = false
          getList()
        })
      }
    }
  })
}

onMounted(() => {
  getList()
})
</script>

<style scoped>

</style>
