import request from "@/utils/request";

//查询所有角色列表(用于新增/修改用户时的角色下拉框)
export function selectAllRole() {
    return request({
        url: '/system/role/selectAllRole',
        method: 'get'
    })
}

//查询角色列表(分页)
export function selectRoleList(query) {
    return request({
        url: '/system/role/selectRoleList',
        method: 'get',
        params: query
    })
}

//根据角色ID查询角色信息
export function selectRoleByRoleId(roleId) {
    return request({
        url: '/system/role/selectRoleByRoleId/' + roleId,
        method: 'get'
    })
}

//新增角色(同时新增角色菜单关联)
export function insertRole(data) {
    return request({
        url: '/system/role/insertRole',
        method: 'post',
        data: data
    })
}

//修改角色(同时修改角色菜单关联)
export function updateRole(data) {
    return request({
        url: '/system/role/updateRole',
        method: 'put',
        data: data
    })
}

//删除角色
export function deleteRoleByRoleIds(roleIds) {
    return request({
        url: '/system/role/deleteRoleByRoleIds/' + roleIds,
        method: 'delete'
    })
}