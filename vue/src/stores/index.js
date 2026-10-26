import {createPinia} from "pinia";

/**
 * 创建一个全局的状态管理仓库
 * 作用：整个应用共享的状态管理中心
 * 就像公司的“总档案库”，所有部门都在这里存储共享信息
 */

const store = createPinia()

//导出仓库实例
export default store