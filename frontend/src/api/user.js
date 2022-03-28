import request from '@/utils/request'

export function login(data) {
  // console.log('开始登录')
  return request({
    url: '/user/login/',
    method: 'POST',
    data: data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info/',
    method: 'GET',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
