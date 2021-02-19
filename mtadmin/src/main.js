import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import auth from './utils/auth'
import http from './utils/http'
import loading from './utils/loading'
import message from './utils/message'
import messageBox from './utils/message_box'

Vue.config.productionTip = false
Vue.prototype.$auth = auth
Vue.prototype.$http = http
Vue.prototype.$loading = loading
Vue.prototype.$message = message
Vue.prototype.$messageBox = messageBox

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
