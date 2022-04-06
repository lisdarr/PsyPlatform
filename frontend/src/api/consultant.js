import request from '@/utils/request'

export function dashboardConsultant(token) {
  return request({
    url: '/consultant/dashboard/',
    method: 'GET',
    params: { token }
  })
}

export function recordConsultant(data) {
  return request({
    url: '/consultant/record',
    method: 'GET',
    params: data
  })
}


