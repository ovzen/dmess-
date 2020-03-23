import Vue from 'vue'
import Router from 'vue-router'
import Chat from './components/Chat'
import Main from './components/Main'
import Profile from './components/Profile'
import AllUsers from './components/AllUsers'
import KnowledgeBase from './components/KnowledgeBase'
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
      path: '/profile',
      name: 'Профиль',
      component: Profile
    },
    {
      path: '/AllUsers',
      name: 'AllUsers',
      component: AllUsers
    },
    {
      path: '/KnowledgeBase',
      name: 'KnowledgeBase',
      component: KnowledgeBase
    }
  ]
})
