import request from '@/utils/request';

export function dashboardAdmin(token)
{
    return request({
        url: '/admin/dashboard/',
        method: 'GET',
        params: {token}
    })
}
export function record(data){
    return request({
        url: '/visitor/record/',
        method: 'GET',
        params: data
    })
}
export function scheduleInfo(token){
    return request({
        url: '/admin/schedule/info/',
        method: 'GET',
        params: {token}
    })
}
export function scheduleQuery(data){
    return request({
        url: '/admin/schedule/query/',
        method: 'GET',
        params: data
    })
}
export function addSchedule(data){
    return request({
        url: '/admin/schedule/add/',
        method: 'POST',
        data: data
    })
}
export function con_info(data){
    return request({
        url: '/consultant/info/',
        method: 'GET',
        params: data
    })
}
export function con_add(data){
    return request({
        url: '/consultant/add/',
        method: 'POST',
        data: data
    })
}
export function con_edit(data){
    return request({
        url: '/consultant/edit/',
        method: 'POST',
        data: data
    })
}
export function dir_info(data){
    return request({
        url: '/director/info/',
        method: 'GET',
        params: data
    })
}
export function dir_add(data){
    return request({
        url: '/director/add/',
        method: 'POST',
        data: data
    })
}
export function dir_edit(data){
    return request({
        url: '/director/edit/',
        method: 'POST',
        data: data
    })
}
export function visitor_info(data){
    console.log("Test")
    return request({
        url: '/visitor/info/',
        method: 'GET',
        params: data
    })
}
export function visitor_ban(data){
    return request({
        url: '/visitor/ban/',
        method: 'POST',
        data: data
    })
}
