import request from '@/utils/request'

export function login(data) {
  // console.log('开始登录')
  return request({
    url: '/admin/login/',
    method: 'POST',
    data: data
  })
}

export function getInfo(token) {
  return request({
    url: '/admin/info/',
    method: 'GET',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/admin/logout/',
    method: 'post'
  })
}

