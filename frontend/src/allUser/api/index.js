import axios from 'axios'
import VueCookie from 'vue-cookie'

axios.interceptors.request.use(
  function (config) {
    if (VueCookie.get('Authentication')) {
      config.headers['Authorization'] = 'Bearer ' + VueCookie.get('Authentication')
    }
    return config
  }, function (error) {
    return Promise.reject(error)
  })
