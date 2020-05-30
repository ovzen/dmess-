import Vue from 'vue'
import jwt from 'jsonwebtoken'
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
      if (state.users.filter(user => user.id === payload.id).length === 0) {
        if (payload.id === state.user_id) {
          payload.is_client = true
          if (typeof state.users[0] !== 'undefined') {
            if (state.users[0].id !== state.user_id) {
              state.users.unshift(payload)
            } else {
              state.users[0] = payload
            }
          } else {
            state.users[0] = payload
          }
        } else {
          for (let contact in state.contacts) {
            console.log('log', state.contacts[contact].contact)
            if (state.contacts[contact].contact === payload.id || state.contacts[contact].user === payload.id) {
              payload.is_contact = true
              state.users.push(payload)
              return 0
            }
          }
          state.users.push(payload)
        }
      }
    },
    addContact: (state, payload) => {
      state.contacts = payload
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
          context.commit('addContact', res.data.results)
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
    }
  }
})
