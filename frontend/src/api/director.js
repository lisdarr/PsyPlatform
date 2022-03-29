import request from '@/utils/request'

export function dashboardDirector(token) {
  return request({
    url: '/user/dashboard/director/',
    method: 'GET',
    params: { token }
  })
}

export function recordDirector(data) {
  return request({
    url: '/user/record/director/',
    method: 'GET',
    params: data
  })
}
