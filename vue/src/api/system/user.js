import request from "@/utils/request";

//修改个人信息
export function updateProfile(data) {
    return request({
        url: '/system/user/profile',
        method: 'put',
        data: data
    })
}

//重置密码
export function updatePwd(data) {
    return request({
        url: '/system/user/profile/updatePwd',
        method: 'put',
        data: data
    })
}

//查询用户列表
export function selectUserList(query) {
    return request({
        url: '/system/user/selectUserList',
        method: 'get',
        params: query
    })
}

//新增用户
export function insertUser(data) {
    return request({
        url: '/system/user/insertUser',
        method: 'post',
        data: data
    })
}

//根据用户ID查询用户信息
export function selectUserByUserId(userId) {
    return request({
        url: '/system/user/selectUserByUserId/' + userId,
        method: 'get'
    })
}

//修改用户
export function updateUser(data) {
    return request({
        url: '/system/user/updateUser',
        method: 'put',
        data: data
    })
}

//删除用户
export function deleteUserByUserIds(userIds) {
    return request({
        url: '/system/user/deleteUserByUserIds/' + userIds,
        method: 'delete'
    })
}