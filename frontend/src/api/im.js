import request from '@/utils/request'

export function getDetails(data) {
  return request({
    url: '/im/details/',
    method: 'GET',
    params: { id: data }
  })
}

export function getUserList() {
  return request({
    url: '/im/getUserList/',
    method: 'GET'
  })
}

export function SendCurrentRecord(data) {
  return request({
    url: '/im/sendCurrentRecord/',
    method: 'POST',
    data: data
  })
}

export function SendDirRecord(data) {
  return request({
    url: '/im/sendDirRecord/',
    method: 'POST',
    data: data
  })
}

export function SaveCurrentRecord(data) {
  return request({
    url: '/im/saveCurrentRecord/',
    method: 'POST',
    data: data
  })
}

// 这个id是咨询师的id
export function askForDir(id) {
  return request({
    url: '/im/askForDir/',
    method: 'GET',
    data: { id: id }
  })
}

export function SaveDirRecord(data) {
  return request({
    url: '/im/saveDirRecord/',
    method: 'POST',
    data: data
  })
}
