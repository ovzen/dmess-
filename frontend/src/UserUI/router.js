import Vue from 'vue'
import Router from 'vue-router'
import Chat from './components/Chat'
import Main from './components/Main'
import Profile from './components/Profile'
import AllUsers from './components/AllUsers'
import KnowledgeBase from './components/KnowledgeBase'
import ChatUser from './components/ChatUser'
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
      path: '/profile/:id',
      name: 'Profile',
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
    },
    {
      path: '/ChatUser/:id',
      name: 'ChatUser',
      component: ChatUser
    }
  ]
})
