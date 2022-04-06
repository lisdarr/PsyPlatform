import request from '@/utils/request'

export function dashboardDirector(token) {
  return request({
    url: '/director/dashboard/',
    method: 'GET',
    params: { token }
  })
}

export function recordDirector(data) {
  return request({
    url: '/director/record',
    method: 'GET',
    params: data
  })
}
