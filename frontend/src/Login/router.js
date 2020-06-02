import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login'
import Register from './components/Register'
import Verification from './components/Verification'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/auth/',
  routes: [
    { path: '/', redirect: '/login/' },
    {
      path: '/login/',
      name: 'Login',
      component: Login
    },
    {
      path: '/register/',
      name: 'Register',
      component: Register
    },
    {
      path: '/register/:registercode/',
      name: 'Register',
      component: Register
    },
    {
      path: '/verify/',
      name: 'Verification',
      component: Verification
    }
  ]
})
