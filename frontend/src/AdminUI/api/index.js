import axios from 'axios'

axios.interceptors.request.use(
  function (config) {
    if (localStorage.getItem('jwt')) {
      config.headers['Authorization'] = 'Bearer ' + localStorage.getItem('jwt')
    }
    return config
  }, function (error) {
    return Promise.reject(error)
  })
