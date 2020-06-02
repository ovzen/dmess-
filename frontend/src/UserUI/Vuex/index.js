import Vue from 'vue'
import Vuex from 'vuex'
import VueCookie from 'vue-cookie'
import users from './users'
import dialogs from './dialogs'

Vue.use(Vuex)
Vue.use(VueCookie)

export default new Vuex.Store({
  state: {
  },

  getters: {
    getUsersByDialog: state => dialog => {
      return state.users.users.filter(user => ((user.id === dialog.users[0] || user.id === dialog.users[1]) && user.id !== state.users.user_id))
    },
    getUsersByDialogId: state => id => {
      let dialog = state.dialogs.dialogs.find(dialog => dialog.id === id)
      if (typeof dialog === 'undefined') {
        return undefined
      }
      return state.users.users.filter(user => ((user.id === dialog.users[0] || user.id === dialog.users[1]) && user.id !== state.users.user_id))
    }
  },

  mutations: {
  },

  actions: {
  },

  modules: {
    users: users,
    dialogs: dialogs
  }
})
