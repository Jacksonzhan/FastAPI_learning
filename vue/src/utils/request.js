import axios from "axios";
import {ElMessage, ElMessageBox} from "element-plus";
import {getToken} from '@/utils/auth'
import useUserStore from '@/stores/modules/userStore'

/* 第一部分: 全局设置 */

//是否显示重新登录的弹窗(防止重复弹出多个)
//想象成是一个正在处理登录过期的标志牌
export let isReLogin = { show: false }

//告诉axios我们的默认请求格式是JSON
axios.defaults.headers['Content-Type'] = 'application/json;charset=utf-8'

//创建一个定制版的axios实例 (就像顺丰给你分配了一个专属的快递员)
const service = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API, //服务器地址(从配置文件中读取)
  timeout: 30000, //30秒之内没有收到回复就认为请求失败了
})

/* 第二部分: 处理重新登录的函数 */

const handleReLogin = () => {
  //如果已经显示登录弹窗, 就别再弹一个了(避免重复弹窗)
  if (isReLogin.show) return

  //打开弹窗
  isReLogin.show = true

  //弹出确认框问用户怎么办
  ElMessageBox.confirm(
      '登录状态已过期,您可以继续留在当前页面,或者重新登录',
      '系统提示',
      {
        confirmButtonText: '重新登录',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        //用户点击了重新登录
        isReLogin.show = false
        useUserStore().logOut().then(() =>{
            //退出后跳转到登录页面(重新登录)
            location.href = '/login' //相当于在浏览器地址栏中输入这个地址
        })
      })
      .catch(() => {
        //用户点击了取消
        isReLogin.show = false
      })
}

/* 第三部分: 请求拦截器(发送请求前要干的事情) */

service.interceptors.request.use(
    config => {
      //1.检查是否需要添加token (有些请求不需要身份认证)
      const isToken = config.headers?.isToken !== false
      const isRepeatSubmit = config.headers?.repeatSubmit !== false

      //如果有token并且这个请求需要token
      if (getToken() && isToken) {
        //在请求头里面加上token
        config.headers['Authorization'] = 'Bearer ' + getToken()
      }

      //2.防止重复提交
      if (!isRepeatSubmit && ['post', 'put'].includes(config.method)) {
        //创建当前请求的身份证
        const requestObj = {
          url: config.url,
          data: typeof config.data === 'object' ? JSON.stringify(config.data) : config.data,
          time: new Date().getTime()
        }

        //从浏览器临时存储中取出上一次的请求记录
        const sessionValue = sessionStorage.getItem('sessionObj')
        const sessionObj = sessionValue ? JSON.parse(sessionValue) : null

        //如果上次有请求记录
        if (sessionObj) {
          //解构出上次请求的信息
          const { url: s_url, data: s_data, time: s_time } = sessionObj
          const interval = 1000

          //检查是否重复提交
          if (s_data === requestObj.data && requestObj.time - s_time < interval && s_url === requestObj.url ) {
            //如果是重复提交, 就拒绝这次请求
            const message = '请勿重复点击'
            ElMessage.error(message)
          }
        }

        //不是重复提交, 就保存这次请求记录(用于下次比较)
        sessionStorage.setItem('sessionObj', JSON.stringify(requestObj))
      }
      //处理完所有请求, 放行请求
      return config;
    },
    error => {
      ElMessage.error(error)
    }
)

/* 第四部分: 响应拦截器(收到响应后要干的事情) */
service.interceptors.response.use(
    res => {
      if (['blob'].includes(res.request.responseType)) {
        //直接返回原始数据(不需要进行下面的业务逻辑处理)
        return res.data
      }

      //从响应数据中取出业务状态码和提示消息
      const code = res.data.code || 200
      const msg = res.data.msg || '操作失败'

      //根据不同的状态码进行不同的处理
      if (code === 401) {
        handleReLogin()
        return Promise.reject('登录已过期, 请重新登录')
      }

      //如果不是200
      if (code !== 200) {
        ElMessage.error(msg)
        return Promise.reject(new Error(msg))
      }
      //一切正常, 返回数据部分
      return res.data
    },
    error => {
      //这里处理网络HTTP错误(比如500,404等等)
      let { message, response } = error

      //1.如果是401错误
      if (response?.status === 401) {
        handleReLogin()
        return Promise.reject('登录已过期, 请重新登录')
      }

      //2.错误信息翻译
      const errMap = {
        'Network Error': '后端接口连接异常', //网络断了
        'timeout': '系统接口请求超时',
        'Request failed with status code': '系统接口' + message.substr(message.length - 3) + '异常'
      }

      //3.遍历错误映射表, 匹配错误信息
      Object.keys(errMap).forEach(key => {
        //如果错误信息包含关键词, 就替换成翻译信息
        if (message.includes(key)) {
          message = errMap[key]
        }
      })

      //4.显示错误提示
      ElMessage.error(message)

      //5.把错误传递下去
      return Promise.reject(error)
    }
)

//导出这个定制版的axios实例
export default service
