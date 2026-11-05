import {getRouters} from "@/api/system/menu.js";

//导入布局组件
import Layout from '@/views/layout/index.vue'

import {defineStore} from "pinia";
import {constantRouters} from "@/router/index.js";

const modules = import.meta.glob('./../../views/**/*.vue')

const useRouteStore = defineStore(
    'permission', //这里必须全局唯一
    {
        state: () => ({
            routes: [], //存储所有路由(固定路由 + 用户专属路由)
            sidebarRouters: [], //存储侧边栏菜单路由 (用于显示菜单)
        }),
        actions: {
            //设置用户专属路由
            setRouters(routers) {
                this.sidebarRouters = routers
            },
            //设置侧边栏路由(固定路由 + 用户专属路由, 侧边栏显示用)
            setSidebarRouters(routers) {
                this.sidebarRouters = routers
            },
            //核心方法: 生成用户的专属路由
            generateRouters() {
                return new Promise(resolve => {
                    //调用API从后端获取路由数据
                    getRouters().then(res => {
                        //深拷贝一份数据, 避免修改原始数据
                        const routerData = JSON.parse(JSON.stringify(res.data))

                        //转换数据格式: 把后端的数据编程前端路由能用的格式
                        const sidebarRouters = convertToRouters(routerData)

                        //保存到仓库
                        this.setRouters(sidebarRouters)
                        //侧边栏显示: 固定路由 + 用户数据
                        this.setSidebarRouters(constantRouters.concat(sidebarRouters))

                        //告诉调用者: 我处理完了, 这是处理好的路由数据
                        resolve(sidebarRouters)
                    })
                })
            },
        }
    }
)

/**
 * 数据转换: 把后端的数据变成前端的路由能用的格式
 */
const convertToRouters = (routers) => {
    //对每个路由进行处理
    return routers.map(route => {
        //1.把字符串转换成真正的组件
        if (route.component) {
            if (route.component === 'Layout') {
                //如果是Layout, 就用导入的主布局组件
                route.component = Layout
            } else {
                //如果是页面组件, 就动态加载
                route.component = loadView(route.component)
            }
        }

        //2.递归处理子路由
        if (route.children && route.children.length) {
            route.children = convertToRouters(route.children)
        } else {
            //如果没有子路由, 就删除children属性
            delete route.children
        }
        return route
    })
}

/**
 * 动态加载视图组件
 */
const loadView = (view) => {
    for (const path in modules) {
        //从完整的路径郑提取相对路径
        const dir = path.split('views/')[1].split('.vue')[0]

        //如果找到了匹配的路径
        if (dir === view) {
            return () => modules[path]()
        }
    }
    //如果找不到对应的组件, 直接返回null
    return null
}

//导出这个状态管理, 其他地方可以导入使用了
export default useRouteStore