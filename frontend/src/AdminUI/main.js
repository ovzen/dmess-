import Vue from 'vue'
import '../plugins/axios'
import App from './App.vue'
import vuetify from '../plugins/vuetify'
import router from './router.js'
Vue.config.productionTip = false;
Vue.config.devtools = false;
Vue.config.debug = false;
Vue.config.silent = true;

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
