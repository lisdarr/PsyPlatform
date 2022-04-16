import request from '@/utils/request'

export function getDetails(data) {
  return request({
    url: '/im/details/',
    method: 'GET',
    params: { id: data }
  })
}

export function AllDir() {
  return request({
    url: 'im/getDir',
    method: 'GET'
  })
}

export function AllUser() {
  return request({
    url: 'im/getUser',
    method: 'GET'
  })
}
