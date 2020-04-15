import Vue from 'vue'
import Router from 'vue-router'
import UserActivity from './components/UserActivity'
import DialogActivity from './components/DialogActivity'
import ServerMessage from './components/ServerMessage'
import Dashboard from './components/Dashboard.vue'
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
    },
    {
      path: '/DialogActivity/',
      name: 'DialogActivity',
      component: DialogActivity
    },
    {
      path: '/ServerMessage/',
      name: 'ServerMessage',
      component: ServerMessage
    },
    {
      path: '/Dashboard/',
      name: 'Dashboard',
      component: Dashboard
    }
  ]
})
