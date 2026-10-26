import request from "@/utils/request";

//登录方法
export function login(data){
    return request({
        url: 'login', //后端接口地址
        headers:{
            isToken:false //告诉拦截器，这个请求不需要token
        },
        method: 'post', //请求方法，请注意需严格遵守后端定义
        data: data //需要发送的数据
    })
}

//获取当前用户信息
export function getInfo(data){
    return request({
        url: 'getInfo', //后端接口地址
        method: 'get', //请求方法，请注意需严格遵守后端定义
    })
}

