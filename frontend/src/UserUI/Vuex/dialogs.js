import api from '../api'

export default ({
  state: {
    dialogs_dowloaded: false,
    dialogs: []
  },

  getters: {
    isDialogDownloaded: state => {
      return state.dialogs_dowloaded
    },
    getDialogById: state => id => {
      return state.dialogs.find(dialog => dialog.id === toString(id))
    },
    getDialogsList: state => {
      return state.dialogs
    }
  },

  mutations: {
    PushDialogs: (state, payload) => {
      state.dialogs = payload
      state.dialogs_dowloaded = true
    },
    UpdateDialogByWs: (state, payload) => {
      let dialogsArr = state.dialogs
      let dialogIndex = dialogsArr.findIndex(dialog => dialog.id === payload.id)
      dialogsArr[dialogIndex].unread_messages = payload.unread_messages
      dialogsArr[dialogIndex].last_message = payload.last_message
    }
  },

  actions: {
    getDialogsData (context, payload) {
      api.axios
        .get('/api/dialog/', { params: { users: payload } })
        .then(response => {
          if (response.status === 200) {
            context.commit('PushDialogs', response.data.results)
          }
        })
        .catch(error => console.log(error))
    }
  }
})
