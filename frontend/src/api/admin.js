import request from '@/utils/request';

export function dashboardAdmin(token)
{
    return request({
        url: '/user/admin/dashboard/',
        method: 'GET',
        params: {token}
    })
}
export function recordAdmin(data){
    return request({
        url: '/user/admin/record/',
        method: 'GET',
        params: data
    })
}
export function consultantAdmin(data){
    return request({
        url: '/user/admin/consultant',
        method: 'GET',
        params: data
    })
}
export function monitorAdmin(data){
    return request({
        url: '/user/admin/monitor',
        method: 'GET',
        params: data
    })
}
export function userAdmin(data){
    return request({
        url: '/user/admin/user',
        method: 'GET',
        params: data
    })
}
