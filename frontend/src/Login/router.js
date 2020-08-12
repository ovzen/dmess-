import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login'
import Register from './components/Register'
import Verification from './components/Verification'
import PasswordEmailSend from './components/PasswordEmailSend'
import PasswordReset from './components/PasswordReset'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/auth/',
  routes: [
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
    },
    {
      path: '/reset/',
      name: 'PasswordEmailSend',
      component: PasswordEmailSend
    },
    {
      path: '/reset-password/',
      name: 'PasswordReset',
      component: PasswordReset
    },
    { path: '*', redirect: '/login/' }
  ]
})
