import Vue from 'vue'
import '../plugins/axios'
import App from './App.vue'
import vuetify from '../plugins/vuetify'
import router from './router.js'
import store from './Vuex'
Vue.config.productionTip = false

new Vue({
  vuetify,
  store: store,
  router,
  render: h => h(App)
}).$mount('#app')
