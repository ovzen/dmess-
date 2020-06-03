import axios from 'axios'
import router from '../router'
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
axios.interceptors.response.use((response) => {
  return response
}, (error) => {
  if (error.response.status === 404) {
    router.push({ path: '/404' })
  }
  if (error.response.status === 500) {
    router.push({ path: '/500' })
  }
  return Promise.reject(error)
})
export default {
  urls: {
    news: '/news',
    chat: '/chat',
    store: '/store',
    users: '/users',
    login: '/auth/login',
    logout: '/auth/logout',
    uploads: '/uploads'
  },
  axios: axios
}
