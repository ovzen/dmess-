import Vue from 'vue'
import Router from 'vue-router'
import UserActivity from './components/UserActivity'
import DialogActivity from './components/DialogActivity'
import ServerMessage from './components/ServerMessage'
import Dashboard from './components/Dashboard.vue'
import Invites from './components/Invites'
Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: '/admin/',
  routes: [
    { path: '/', redirect: '/Dashboard/' },
    {
      path: '/UserActivity/',
      name: 'UserActivity',
      component: UserActivity,
      meta: { title: 'User Activity' }
    },
    {
      path: '/DialogActivity/',
      name: 'DialogActivity',
      component: DialogActivity,
      meta: { title: 'Dialog Activity' }
    },
    {
      path: '/ServerMessage/',
      name: 'ServerMessage',
      component: ServerMessage,
      meta: { title: 'Server Message' }
    },
    {
      path: '/Dashboard/',
      name: 'Dashboard',
      component: Dashboard,
      meta: { title: 'Dashboard' }
    },
    {
      path: '/Invites/',
      name: 'Invites',
      component: Invites,
      meta: { title: 'Invites' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Dmess admin'
  next()
})

export default router
