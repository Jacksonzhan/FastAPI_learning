import request from "@/utils/request";

//登录方法
export function register(data){
    return request({
        url: 'register', //后端接口地址
        headers:{
            isToken:false //告诉拦截器，这个请求不需要token
        },
        method: 'post', //请求方法，请注意需严格遵守后端定义
        data: data //需要发送的数据
    })
}