import { defineStore } from 'pinia'
import {getToken,removeToken,setToken} from "@/utils/auth.js";
import {getInfo,login} from "@/api/login.js";
import defaultAvatar from "@/assets/images/profile.png";



const useUserStore = defineStore(
    'user',//这里必须全局唯一
    {
        //第一部分：状态定义(存储的数据)
        state:() => ({
            token:getToken(),//用户登录后的token
            id:'',//用户id
            name:'',//用户名
            avatar:''//用户的头像文件地址
        }),

        //第二部分：操作方法(处理这些数据的函数)
        actions: {
            /**
             * 登录方法
             * 作用：发送登录请求，保持登录凭证
             */
            login(userInfo){
                //异步操作
                return new Promise((resolve,reject) => {
                    //调用登录接口
                    login(userInfo).then(res => {
                        //登录成功
                        //1.保存token到本地存储(这样一来刷新页面后也不会消失)
                        setToken(res.token)

                        //2.更新store中的token
                        this.token = res.token

                        //3.告诉调用者；成功了！
                        resolve()
                    }).catch(error => {
                        //登录失败
                        reject(error)
                    })
                })
            },
            /**
             * 获取用户详细信息
             * 作用：获取id name avatar
             */
            getInfo(){
                return new Promise((resolve,reject) => {
                    //调用获取用户信息的接口
                    getInfo().then(res => {
                        //1.从相应数据中获取
                        const user = res.data

                        //处理头像地址
                        let avatar = user.avatar || ""

                        //判断头像地址是否完整
                        if(avatar.indexOf('http://') === -1 && avatar.indexOf('https://') === -1)
                            //如果头像地址不完整(是相对路径)
                            if (avatar) {
                                avatar = import.meta.env.VITE_APP_BASE_API + avatar
                            } else {
                                //如果没有头像就使用默认头像
                                avatar = defaultAvatar
                            }
                        //2.更新用户信息
                        this.id = user.userId
                        this.name = user.userName
                        this.avatar = avatar

                        //3.告诉调用者；成功了！
                        resolve(res)
                    }).catch(error => {
                        //登录失败
                        reject(error)
                    })
                })
            },
            /**
             * 用户退出登录
             * 知识点：JWT是“无状态的”，服务器不保存登录状态，token就在前端手里
             * 所以退出登录不需要后端接口，前端把token删掉就算退出了
             */
            logOut(){
                return new Promise((resolve) => {
                    //1.清空store中的token
                    this.token=''

                    //2.删除本地存储的token
                    removeToken()

                    //3.告诉调用者：成功了
                    resolve()
                })
            }
        }
    }
)
//导出这个状态管理，其他地方可以导入使用
export default useUserStore