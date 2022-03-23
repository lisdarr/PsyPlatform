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
axios.defaults.baseURL = 'http://127.0.0.1:8000/api'
Vue.prototype.$axios = axios
// set ElementUI lang to EN
Vue.use(ElementUI, { locale })

Vue.use(VueResource)

Vue.prototype.goeasy = GoEasy.getInstance({
  host: 'hangzhou.goeasy.io',
  appkey: 'BC-51b5a52577df4ba8ae017cd70fb83835',
  modules: ['im']
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
