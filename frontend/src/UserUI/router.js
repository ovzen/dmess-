import Vue from 'vue'
import Router from 'vue-router'
import Chat from './components/Chat'
import Main from './components/Main'
import Profile from './components/Profile'
import allUser from './components/allUser'
import Страница from './components/knowledgebase'
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
      path: '/all_User',
      name: 'allUser',
      component: allUser
    },
    {
      path: '/knowledgebase',
      name: 'knowledgebase',
      component: knowledgebase
    }
  ]
})
