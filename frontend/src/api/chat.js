import request from '@/utils/request'

export function chatHistoryDir(data) {
  return request({
    url: '/ChatDirector',
    method: 'GET',
    params: data
  })
}

export function chatHistoryCon(data) {
  return request({
    url: '/ChatConsult',
    method: 'GET',
    params: data
  })
}
