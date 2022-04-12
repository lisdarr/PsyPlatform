import request from '@/utils/request'

export function chatHistory(data) {
  return request({
    url: '/ChatDirector',
    method: 'GET',
    params: data
  })
}
