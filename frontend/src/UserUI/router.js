import Vue from 'vue'
import Router from 'vue-router'
import Chat from './components/Chat'
import Main from './components/Main'
import Profile from './components/Profile'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/chat/:id',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/profile/:id',
      name: 'Профиль',
      component: Profile
    }
  ]
})
