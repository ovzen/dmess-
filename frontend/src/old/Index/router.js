import Vue from 'vue'
import Router from 'vue-router'
import Chat from '../Chat/App.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ch',
      name: 'Chat',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Chat
    }
  ]
})
