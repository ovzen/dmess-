<template>
  <div style="height:100%;">
    <MessagesList
      v-if="messages.length > 0"
      :messages="messages"
      :get-time="getTime"
      :dialog-messages-length="dialogMessagesLength"
      :delete-message="deleteMessage"
      :message-update="messageUpdate"
      :decode-emoji-code="decodeEmojiCode"
      :is-own-message="isOwnMessage"
      :is-new-date="isNewDate"
      :get-day="getDay"
    />
    <NoMessages v-else />
    <span v-observe-visibility="visibilityChanged" />
    <v-btn
      color="warning"
      fixed
      class="basic_text"
      :style="'right:' + (scroll ? -60 : 5) +'px;transition: right 0.25s;bottom:60px;'"
      fab
      dark
      @click="toLastMessage()"
    >
      <v-icon>mdi-arrow-down</v-icon>
    </v-btn>
    <file-pond
      ref="pond"
      name="image"
      class="background_white black--text"
      :style="'position:fixed;width:450px;border-radius:.5em;left:' + this.$vuetify.application.left +'px;max-height:80%;transition-duration: .25s;bottom:' + (hide ? '20' : '-100') + 'px'"
      label-idle="Click to select a file or drop it here"
      :allow-multiple="false"
      :files="myFiles"
      :drop-on-page="true"
      :drop-on-element="false"
      server="/api/messages/image_upload/"
      @init="handleFilePondInit"
      @addfile="beforeupload"
      @processfile="afterupload"
    />
    <v-footer
      color="background_white"
      fixed
      inset
      app
      class="d-inline-flex"
      style="padding:5px;box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2), 0px 2px 2px rgba(0, 0, 0, 0.12), 0px 0px 2px rgba(0, 0, 0, 0.14);"
    >
      <v-btn
        icon
        color="#9f9f9f"
        class="align-self-sm-end"
        style="margin-bottom:5px"
        @click="hide=!hide"
      >
        <v-icon>
          mdi-paperclip
        </v-icon>
      </v-btn>
      <v-textarea
        ref="myTextArea"
        v-model="message"
        auto-grow
        autofocus
        rows="1"
        placeholder="Message"
        hide-details
        color="false"
        style="margin-top:-5px;margin-bottom:7px"
        @keydown.enter.prevent=""
        @keydown.ctrl.b="EasterEgg()"
        @keyup.enter="sendMessage()"
      />
      <Emoji
        class="background_white"
        style="padding-right: 28px; margin-left: 10px;"
        :open="smiles"
        @click="selectedEmoji"
      />
      <v-btn
        icon
        color="basic"
        :disabled="loading || !(message !== '' || imageUrl !== '')"
        class="align-self-sm-end"
        style="margin-bottom:5px"
        @click="sendMessage()"
      >
        <v-icon>
          mdi-send
        </v-icon>
      </v-btn>
    </v-footer>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { VueChatEmoji, emojis } from 'vue-chat-emoji'
import api from '../api'
import VueNativeSock from 'vue-native-websocket'
import VueCookie from 'vue-cookie'
import Vue from 'vue'
import jwt from 'jsonwebtoken'
import moment from 'moment'
import linkify from 'vue-linkify'
import vueFilePond from 'vue-filepond'
import './css/filepond.min.css'
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css'
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type'
import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
import FilePondPluginGetFile from 'filepond-plugin-get-file'
import './css/filepond-plugin-get-file.min.css'
import VueObserveVisibility from 'vue-observe-visibility'
const MessagesList = () => import('./MessagesList')
const NoMessages = () => import('./NoMessages')
let FilePond = vueFilePond(FilePondPluginFileValidateType, FilePondPluginImagePreview, FilePondPluginGetFile)
Vue.directive('linkified', linkify)
require('./css/vue-chat-emoji.css')
Vue.use(VueObserveVisibility)
Vue.use(VueCookie)
Vue.use(VueNativeSock, (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/messages/')
export default {
  name: 'ChatUser',
  components: {
    FilePond,
    Emoji: VueChatEmoji,
    MessagesList,
    NoMessages
  },
  data: () => ({
    messages: [],
    message: '',
    myFiles: [],
    hide: false,
    scroll: true,
    dialogMessagesLength: 0,
    dialogId: 0,
    imageUrl: '',
    loading: false,
    smiles: false,
    fileExtension: null,
    updateMessage: undefined
  }),
  computed: {
    ...mapGetters(['getUserId', 'getUsersByDialogId'])
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['updateDialog']
  },
  beforeMount () {
    setTimeout(this.GetOldMessages, 1500)
  },
  mounted () {
    let Vue = this
    this.updateDialog()
    this.getMessage()
    setTimeout(this.UpdateUserInDialog, 1000)
    this.$options.sockets.onopen = function () {
      this.$socket.send(
        JSON.stringify(
          {
            action: 'subscribe_to_messages_in_dialog',
            request_id: Vue.getUserId,
            dialog_id: Vue.$route.params.id
          }
        )
      )
    }
  },
  methods: {
    messageUpdate (message) {
      this.updateMessage = message
      this.message = this.decodeEmojiCode(message.text)
    },
    deleteMessage (id) {
      let Vue = this
      this.$socket.send(
        JSON.stringify(
          {
            'action': 'delete',
            'request_id': Vue.getUserId,
            'pk': id
          }
        )
      )
    },
    toLastMessage () {
      var Data = this
      Vue.nextTick(function () {
        Data.$vuetify.goTo(document.getElementById('Message_' + Data.messages[0].id), { duration: 450, offset: 0 })
      })
    },
    visibilityChanged (isVisible, entry) {
      this.scroll = isVisible
    },
    handleFilePondInit: function () {
      console.log('FilePond has initialized')
    },
    ...mapActions(['getDialogsData', 'getUserData']),
    beforeupload (file, progress) {
      console.log('beforeupload', file, progress)
      this.fileExtension = progress.fileExtension
      this.loading = true
      this.hide = true
    },
    afterupload (file, progress) {
      console.log('afterupload', file, progress)
      this.imageUrl = JSON.parse(progress.serverId).image_url
      this.loading = false
    },
    decodeEmojiCode (str) {
      return emojis.decodeEmoji(str)
    },
    selectedEmoji (args) {
      this.message += args.emoji
      this.smiles = true
      setTimeout(() => { this.smiles = false }, 25)
    },
    CheckIsVisible (el) {
      var rect = el.getBoundingClientRect()
      var elemTop = rect.top
      var elemBottom = rect.bottom
      var isVisible = (elemTop >= 0) && (elemBottom <= window.innerHeight)
      return isVisible
    },
    GetOldMessages () {
      if (this.dialogMessagesLength > 0 && this.messages.length > 0) {
        if (this.dialogMessagesLength > this.messages.length && this.CheckIsVisible(document.getElementById('Message_' + this.messages[this.messages.length - 1].id))) {
          console.log('visible')
          api.axios
            .get('/api/messages/', { params: { dialog: this.dialogId, limit: 30, offset: this.messages.length, ordering: '-create_date' } })
            .then(response => {
              if (response.status === 200) {
                if (response.data.count > 0) {
                  this.messages = this.messages.concat(response.data.results)
                }
              }
            })
        }
      }
      setTimeout(this.GetOldMessages, 1000)
    },
    EasterEgg () {
      this.$vuetify.theme.themes.dark.basic = this.message
      this.$vuetify.theme.themes.light.basic = this.message
      this.$vuetify.theme.themes.dark.basic_text = this.message
      this.$vuetify.theme.themes.light.basic_text = this.message
      this.$vuetify.theme.themes.light.background_user = this.message
    },
    sendMessage () {
      console.log(this.$refs)
      let Vue = this
      if (!this.loading && (this.message !== '' || this.imageUrl !== '') && typeof this.updateMessage === 'undefined') {
        console.log('messagetext: ', this.message)
        this.$socket.send(
          JSON.stringify({
            action: 'create',
            request_id: Vue.getUserId,
            data: {
              text: emojis.encodeEmoji(this.message),
              dialog: Vue.$route.params.id,
              image_url: Vue.imageUrl,
              user: Vue.getUserId
            }
          })
        )
        this.message = ''
        this.updateMessage = undefined
        this.myFiles = []
        this.imageUrl = ''
      }
      if (!this.loading && (this.message !== '' || this.imageUrl !== '') && typeof this.updateMessage !== 'undefined') {
        this.$socket.send(
          JSON.stringify(
            {
              pk: Vue.updateMessage.id,
              action: 'patch',
              request_id: Vue.getUserId,
              data: {
                id: Vue.updateMessage.id,
                text: Vue.message
              }
            }
          )
        )
        this.message = ''
        this.updateMessage = undefined
        this.myFiles = []
        this.imageUrl = ''
      }
    },
    updateDialog () {
      this.message = ''
      this.messages = []
      this.dialogId = this.$route.params.id
      api.axios.get('/api/messages/count/', { params: { dialog: this.dialogId } }).then(res => { this.dialogMessagesLength = res.data.count })
      api.axios
        .get('/api/messages/', { params: { dialog: this.dialogId, limit: 30, ordering: '-create_date' } })
        .then(response => {
          if (response.status === 200) {
            this.messages = this.messages.concat(response.data.results)
          }
        })
        .catch(error => console.log(error))
      api.axios.post('/api/dialog/' + this.dialogId + '/read_messages/').then(res => {
        if (res.status === 200) {
          this.getDialogsData()
        }
      })
    },
    getMessage () {
      this.$options.sockets.onmessage = event => {
        console.log(event)
        let vue = this
        let action = JSON.parse(event.data).action
        let status = JSON.parse(event.data).response_status
        let data = JSON.parse(event.data).data
        if (action === 'patch' || action === 'update') {
          console.log('PATCH!!!', vue.messages[0].id, data.id)
          vue.$set(vue.messages, vue.messages.findIndex(message => message.id === data.id), data)
        }
        if (action === 'create' && status !== 201) {
          this.messages.unshift({
            id: data.id,
            text: data.text,
            user: data.user,
            create_date: data.create_date,
            image_url: data.image_url,
            name: data.name,
            extension: data.extension
          })
          this.dialogMessagesLength += 1
          Vue.nextTick(function () {
            vue.$vuetify.goTo(document.getElementById('Message_' + data.id))
          })
          api.axios.post('/api/dialog/' + this.dialogId + '/read_messages/')
        }
        if (action === 'delete' && data !== null) {
          this.messages.splice(this.messages.findIndex(message => message.id === data.id), 1)
          this.dialogMessagesLength -= 1
        }
      }
    },
    UpdateUserInDialog () {
      if (typeof this.getUsersByDialogId(this.$route.params.id) !== 'undefined') {
        this.getUserData([this.getUsersByDialogId(this.$route.params.id)[0].id, true])
      }
    },
    isOwnMessage (author) {
      return author !== jwt.decode(this.$cookie.get('Authentication')).user_id
    },
    getTime (datetime) {
      if (datetime) {
        return moment(String(datetime)).format('HH:mm')
      }
    },
    getDay (datetime) {
      if (datetime) {
        if (moment(datetime).isSame(moment(), 'day')) {
          return 'Today'
        } else {
          return moment(String(datetime)).format('DD.MM.YYYY')
        }
      }
    },
    isNewDate (message, previousMessage) {
      if (message.id === this.messages[this.messages.length - 1].id) {
        return true
      } else if (previousMessage) {
        if (moment(message.create_date).isAfter(moment(previousMessage.create_date), 'day')) {
          return true
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  border-radius: 6px;
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
  background-color:rgba(0,0,0,0.7);
}
.container {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
