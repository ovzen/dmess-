import Vue from 'vue'
import jwt, { verify } from 'jsonwebtoken'
import VueCookie from 'vue-cookie'
import api from '../api'

Vue.use(VueCookie)

export default ({
  state: {
    user_id: jwt.decode(VueCookie.get('Authentication')).user_id,
    contacts: [],
    users: []
  },

  getters: {
    getUserId: state => {
      return state.user_id
    },
    getClient: state => {
      return state.users[0]
    },
    getClientProfile: state => {
      if (typeof state.users[0] !== 'undefined') {
        return state.users[0].profile
      }
      return { is_online: true, avatar: undefined }
    },
    getContacts: state => {
      return state.users.filter(user => user.is_contact === true)
    },
    getContactsId: state => {
      return state.contacts
    },
    getUsers: state => {
      return state.users.filter(user => typeof user.is_contact === 'undefined' && typeof user.is_client === 'undefined')
    },
    checkUserById: state => id => {
      return state.users.filter(user => user.id === parseInt(id)).length !== 0
    },
    getUserById: state => id => {
      return state.users.find(user => user.id === parseInt(id))
    },
    getUsersByName: state => username => {
      return state.users.filter(user => user.username.toLowerCase().indexOf(username.toLowerCase()) > -1 && typeof user.is_contact === 'undefined' && typeof user.is_client === 'undefined')
    }
  },

  mutations: {
    addUser: (state, payload) => {
      let index = state.users.findIndex(user => user.id === payload.id)
      for (let contact in state.contacts) {
        if (state.contacts[contact].contact === payload.id) {
          payload.is_contact = true
        }
      }
      if (payload.id === state.user_id) {
        payload.is_client = true
      }
      if (index > -1) {
        Vue.set(state.users, parseInt(index), payload)
      } else {
        if (typeof payload.is_client === 'undefined') {
          state.users.push(payload)
        } else {
          state.users.unshift(payload)
        }
      }
    },
    makeContact: (state, payload) => {
      state.contacts = payload
    },
    addContact: (state, payload) => {
      let User = state.users.find(user => user.id === parseInt(payload))
      User.is_contact = true
      Vue.set(state.users, state.users.findIndex(user => user.id === parseInt(payload)), User)
    }
  },

  actions: {
    getUserData (context, payload) {
      if (Array.isArray(payload)) {
        var ignore = true
        payload = payload[0]
      }
      if (context.state.users.filter(user => user.id === payload).length === 0 || typeof ignore !== 'undefined') {
        api.axios
          .get('/api/users/' + payload + '/')
          .then(res => {
            if (res.status === 200) {
              context.commit('addUser', res.data)
            }
          })
          .catch(error => console.log(error))
      }
    },
    getContactsData (context) {
      api.axios.get('/api/contacts/').then(res => {
        if (res.status === 200) {
          context.commit('makeContact', res.data.results)
          for (let contact in res.data.results) {
            api.axios
              .get('/api/users/' + res.data.results[contact].contact + '/')
              .then(ress => {
                if (ress.status === 200) {
                  context.commit('addUser', ress.data)
                }
              })
              .catch(error => console.log(error))
          }
        }
      })
    },
    add_Сontact (context, payload) {
      api.axios.post('/api/users/' + payload + '/add_contact/').then(res => {
        if (res.status === 201) {
          context.commit('addContact', payload)
        }
      })
    }
  }
})
