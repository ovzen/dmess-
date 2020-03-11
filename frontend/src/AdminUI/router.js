import Vue from 'vue'
import Router from 'vue-router'
import UserActivity from './components/UserActivity'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/admin/',
  routes: [
    { path: '/', redirect: '/UserActivity/' },
    {
      path: '/UserActivity/',
      name: 'UserActivity',
      component: UserActivity
    }
  ]
})
