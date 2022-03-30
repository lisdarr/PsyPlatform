import request from '@/utils/request';

export function recordAdmin(data){
    return request({
        url: '/user/admin/record/',
        method: 'GET',
        params: data
    })
}
