import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import '@/styles/index.scss' // global css
import App from './App'
import store from './store'
import router from './router'
import '@/icons' // icon
import '@/permission' // permission control
// 如果想要中文版 element-ui，按如下方式声明
// Vue.use(ElementUI)
import GoEasy from 'goeasy'
import VueResource from 'vue-resource'
import IMService from '@/views/ChatConsult/imservice'
/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../frontend/mock')
  mockXHR()
}
var axios = require('axios')
// axios.defaults.baseURL = 'http://127.0.0.1:8000/'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
Vue.prototype.$axios = axios
// set ElementUI lang to EN
Vue.use(ElementUI, { locale })

Vue.use(VueResource)

const goEasy = GoEasy.getInstance({
  host: 'hangzhou.goeasy.io', // 应用所在的区域地址: [hangzhou.goeasy.io, 新加坡暂不支持IM，敬请期待]
  appkey: 'BC-a9e0b1b27564446d942734742f8cbf07', // common key
  modules: ['im']
})

Vue.prototype.GoEasy = GoEasy
Vue.prototype.goEasy = goEasy
Vue.prototype.service = new IMService(goEasy, GoEasy)

Vue.config.productionTip = false
Vue.prototype.formatDate = function(t) {
  t = t || Date.now()
  const time = new Date(t)
  let str = time.getMonth() < 9 ? ('0' + (time.getMonth() + 1)) : (time.getMonth() + 1)
  str += '-'
  str += time.getDate() < 10 ? ('0' + time.getDate()) : time.getDate()
  str += ' '
  str += time.getHours()
  str += ':'
  str += time.getMinutes() < 10 ? ('0' + time.getMinutes()) : time.getMinutes()
  return str
}

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
