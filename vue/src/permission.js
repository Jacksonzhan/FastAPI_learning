//定义路由守卫
//导入路由实例
import router from "./router";
import {isReLogin} from "@/utils/request.js";
import useUserStore from '@/stores/modules/userStore';
import {ElMessage} from "element-plus";
import {getToken} from "@/utils/auth.js";

//设置白名单：定义不需要登录就可以访问的路由地址
const whiteList = ["/login", "/register"];

//判断路径是否在白名单中
const isWhiteList = (path) => {
    return whiteList.includes(path);
}

//全局路由守卫 每次路由跳转前都会执行这个函数
router.beforeEach((to, form, next) => {
    //先检查用户是否有token(相当于山姆超市入门时检查有无会员卡)
    if (getToken()){
        //情况1:用户有token

        //情况1.1 用户已登录，但是要去登陆页
        if (to.path === '/login' || to.path === '/register'){
            //已经登陆了还要去登陆页？我直接让你跳转到首页
            next({path:'/'})
        }
        //情况1.2 用户已登陆，访问白名单页面
        else if (isWhiteList(to.path)){
            //在白名单中，就直接放行
            next()
        }

        //情况1.3 用户已登陆，但想访问需要权限的页面
        else{
            //检查store中是否有用户信息
            if (useUserStore().name === ''){
                //设置“正在重新登陆的标志”
                isReLogin.show = true

                //调用获取用户信息的方法
                useUserStore().getInfo().then(() => {
                    //清除标志
                    isReLogin.show = false

                    //跳转到首页(或者原本要去的页面)
                    next({path: to.path})
                }).catch(err => {
                    //获取用户信息失败(token可能过期了)
                    //调用退出登录的办法
                    useUserStore().logOut().then(() => {
                        //显示错误信息
                        ElMessage.error(err)

                        //跳转到登陆页
                        next({path:'/login'})
                    })
                })
            }else{
                //有用户信息，说明有权限，直接放行
                next()
            }
        }
    }else {
        //没有token的情况
        if (isWhiteList(to.path)){
            //在白名单中，直接进入
            next()
        }else{
            //不在白名单中，重定向到登陆页
            next("/login")
        }
    }
})
