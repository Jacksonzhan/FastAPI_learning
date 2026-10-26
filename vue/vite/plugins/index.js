/**
 * 整个前端项目的插件工厂，用于统一管理项目的所有vite插件
 */
//导入vue的vite插件
import vue from "@vitejs/plugin-vue";
import createSvgIcons from "./svg--icon";

export default function createVitePlugins(viteEnv, isBuild = false){
    //1.创建插件数组，初始化包含vue插件
    const vitePlugins = [vue()]

    //2.添加自动导入插件
    vitePlugins.push(createSvgIcons())

    //3.返回插件数组
    return vitePlugins
}