import request from '@/utils/request'

export function dashboardConsultant(token) {
  return request({
    url: '/user/dashboard/consultant/',
    method: 'GET',
    params: { token }
  })
}

export function recordConsultant(data) {
  return request({
    url: '/user/record/consultant',
    method: 'GET',
    params: data
  })
}


