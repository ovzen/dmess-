import Vue from 'vue'
import Router from 'vue-router'
const Main = () => import('./components/Main')
const ChatUser = () => import('./components/ChatUser')
const UserProfile = () => import('./components/UserProfile')
const MyProfile = () => import('./components/MyProfile')
const Error500 = () => import('./components/Error500.vue')
const Error404 = () => import('./components/Error404.vue')
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
