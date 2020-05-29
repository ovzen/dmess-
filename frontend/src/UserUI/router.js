import Vue from 'vue'
import Router from 'vue-router'
import Chat from './components/Chat'
import Main from './components/Main'
import Profile from './components/Profile'
import AllUsers from './components/AllUsers'
import KnowledgeBase from './components/KnowledgeBase'
import ChatUser from './components/ChatUser'
import UserProfile from './components/UserProfile'
import MyProfile from './components/MyProfile'
import Error500 from './components/Error500.vue'
import Error404 from './components/Error404.vue'
Vue.use(Router)

const router = new Router({
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
    },
    {
      path: '/UserProfile/:Userid',
      name: 'UserProfile',
      component: UserProfile
    },
    {
      path: '/MyProfile',
      name: 'MyProfile',
      component: MyProfile
    },
    {
      path: '/404',
      name: 'Error404',
      component: Error404
    },
    {
      path: '/500',
      name: 'Error500',
      component: Error500
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})

export default router
