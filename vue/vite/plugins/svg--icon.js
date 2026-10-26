//导入插件的创建函数
import {createSvgIconsPlugin} from "vite-plugin-svg-icons";
//导入path模块，用于处理文件路径
import path from 'path'

export default function createSvgIcons(){
    return createSvgIconsPlugin({
        //图标文件夹的路径配置
        iconDirs:[path.resolve(process.cwd(),'src/assets/icons/svg')],
        //图标的id命名规则
        symbolId:'icon-[dir]-[name]'
    })
}