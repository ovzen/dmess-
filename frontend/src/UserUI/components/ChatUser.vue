<template>
  <div style="height:100%;">
    <v-row
      v-if="messages.length > 0"
      class="d-flex flex-column-reverse"
      style="padding-bottom:0px;height:100%;"
      align="end"
    >
      <v-container
        v-for="(message, i) in messages"
        :id="'Message_' + message.id"
        :key="message.id"
        py-2
      >
        <v-card
          v-if="isNewDate(message, messages[i+1])"
          style="border-radius: 15px;width:min-content"
          class="d-inline-flex align-content-center"
          color="background_white"
        >
          <v-card-text
            style="padding: 8px"
          >
            <span
              class="message_color--text message"
            >
              {{ getDay(message.create_date) }}
            </span>
          </v-card-text>
        </v-card>
        <div
          v-if="isOwnMessage(message.user)"
          class="text-left message-hover"
        >
          <v-card
            style="border-radius: 20px;"
            max-width="460px"
            class="d-flex align-content-start flex-wrap flex-shrink-1"
            flat
            min-width="200px"
          >
            <v-container
              class="d-inline-flex align-content-center"
              pb-0
              mb-0
            >
              <v-img
                v-if="message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg'"
                :src="message.image_url"
                max-width="440px"
                min-width="200px"
                @click="dialog=true,link=message.image_url"
              /><file-pond
                v-if="!(message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg') && message.image_url !== '' && message.image_url !== 'False'"
                ref="pond2"
                name="image"
                :disabled="true"
                style="max-width=440px;min-width:400px;border-radius:.5em;"
                :files="[message.image_url]"
                class-name="123"
                :instant-upload="false"
                :allow-download-by-url="true"
                label-idle="Drop files here..."
              />
            </v-container>
            <v-card-text
              style="padding-top: 3px; padding-bottom: 0px"
            >
              <span
                class="message_color--text message"
              >
                {{ decodeEmojiCode(message.text) }}
              </span>
            </v-card-text>
            <v-card-actions style="padding-top: 0px; margin-left: auto">
              <span
                class="float-right overline"
              >
                {{ getTime(message.create_date) }}
              </span>
            </v-card-actions>
          </v-card>
        </div>
        <v-container
          class="d-flex flex-row-reverse"
          py-0
        >
          <div
            v-if="!isOwnMessage(message.user)"
            class="text-left"
          >
            <v-card
              style="border-radius: 20px;"
              max-width="460px"
              class="d-flex align-content-start flex-wrap flex-shrink-1"
              color="background_pink"
              flat
              min-width="200px"
            >
              <v-container
                class="d-inline-flex align-content-center"
                pb-0
                mb-0
              >
                <v-img
                  v-if="message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg'"
                  :src="message.image_url"
                  max-width="440px"
                  min-width="200px"
                  @click="dialog=true,link=message.image_url"
                /><file-pond
                  v-if="!(message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg') && message.image_url !== '' && message.image_url !== 'False'"
                  ref="pond2"
                  name="image"
                  :disabled="true"
                  style="max-width=440px;min-width:400px;border-radius:.5em;"
                  :files="[message.image_url]"
                  class-name="123"
                  :instant-upload="false"
                  :allow-download-by-url="true"
                  label-idle="Drop files here..."
                />
              </v-container>
              <v-card-text
                style="padding-top: 3px; padding-bottom: 0px"
              >
                <div
                  class="d-flex flex-column-reverse"
                >
                  <div class="message-hover">
                    <span
                      class="message_color--text message"
                    >
                      {{ decodeEmojiCode(message.text) }}
                    </span>
                  </div>
                  <div class="menu-hover mt-n7">
                    <div class="rounded-menu d-flex flex-row-reverse">
                      <div class="rounded-menu flex-row-reverse elevation-6">
                        <v-tooltip top>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              icon
                              style="width:23px; height:20px;"
                              v-on="on"
                              @click="messageUpdate(message)"
                            >
                              <v-icon
                                style="font-size:18px;"
                                color="black"
                              >
                                mdi-pencil
                              </v-icon>
                            </v-btn>
                          </template>
                          <span>Edit message</span>
                        </v-tooltip>
                        <v-tooltip top>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              icon
                              style="width:23px; height:20px;"
                              v-on="on"
                              @click="deleteMessage(message.id)"
                            >
                              <v-icon
                                style="font-size:18px;"
                                color="black"
                              >
                                mdi-delete-forever
                              </v-icon>
                            </v-btn>
                          </template>
                          <span>Delete message</span>
                        </v-tooltip>
                        <v-tooltip top>
                          <template
                            v-slot:activator="{ on }"
                            class="white"
                          >
                            <v-btn
                              icon
                              style="width:23px; height:20px;"
                              v-on="on"
                            >
                              <v-icon
                                style="font-size:18px;"
                                color="black"
                              >
                                mdi-dots-vertical
                              </v-icon>
                            </v-btn>
                          </template>
                          <span>Something more</span>
                        </v-tooltip>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card-text>
              <v-card-actions style="padding-top: 0px; margin-left: auto">
                <span
                  class="float-right overline"
                >
                  {{ getTime(message.create_date) }}
                </span>
              </v-card-actions>
            </v-card>
          </div>
        </v-container>
      </v-container>
      <v-progress-circular
        v-if="messages.length < dialogMessagesLength"
        indeterminate
        size="36"
        style="position: relative; right:50%;margin-top: 25px;margin-bottom: 25px;"
        color="basic"
      />
    </v-row>
    <v-row
      v-else
      align="center"
      justify="center"
      style="padding-bottom:56px;height:100%;"
    >
      <div class="d-flex flex-column">
        <span
          v-if="messages.length === 0"
          style="font-weight: 300;
              font-size: 96px;
              line-height: 112px;
              text-align: center;
              letter-spacing: -1.5px;"
          class="smile_color--text"
        >
          ¯\_(ツ)_/¯
        </span>
        <span
          v-if="messages.length === 0"
          style="font-family: Roboto;
              font-style: normal;
              font-weight: 500;
              font-size: 14px;
              line-height: 16px;
              text-align: center;
              letter-spacing: 0.75px;
              text-transform: uppercase;
              padding-top:15px"
          class="smile_color--text"
        >
          there are no messages yet
        </span>
      </div>
    </v-row>
    <span v-observe-visibility="visibilityChanged" />
    <v-dialog
      v-model="dialog"
      content-class="elevation-0"
    >
      <v-img
        contain
        style="box-shadow: none !important"
        max-height="85vh"
        :src="link"
        @click="dialog=false"
      />
    </v-dialog>
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
const FilePond = vueFilePond(FilePondPluginFileValidateType, FilePondPluginImagePreview, FilePondPluginGetFile)
Vue.directive('linkified', linkify)
require('./css/vue-chat-emoji.css')
Vue.use(VueObserveVisibility)
Vue.use(VueCookie)
Vue.use(VueNativeSock, (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/messages/')
export default {
  name: 'ChatUser',
  components: {
    FilePond,
    Emoji: VueChatEmoji
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
    dialog: false,
    loading: false,
    smiles: false,
    fileExtension: null,
    updateMessage: undefined,
    link: ''
  }),
  computed: {
    ...mapGetters(['getUserId', 'getUsersByDialogId'])
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['updateDialog']
  },
  beforeMount () {
    setTimeout(this.GetOldMessages, 1000)
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
  beforeDestroy () {
    this.$socket.send(
      JSON.stringify(
        {
          action: 'unsubscribe_to_messages_in_dialog',
          request_id: Vue.getUserId,
          dialog_id: Vue.$route.params.id
        }
      )
    )
  },
  methods: {
    messageUpdate (message) {
      this.updateMessage = message
      this.message = message.text
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
                  let length = this.messages.length
                  this.messages = this.messages.concat(response.data.results)
                  var Data = this
                  Vue.nextTick(function () {
                    Data.$vuetify.goTo(document.getElementById('Message_' + Data.messages[length].id), { duration: 0 })
                  })
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
      }
      this.message = ''
      this.updateMessage = undefined
      this.myFiles = []
      this.imageUrl = ''
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
            if (response.data.count > 0) {
              var Data = this
              Vue.nextTick(function () {
                Data.$vuetify.goTo(document.getElementById('Message_' + Data.messages[0].id), { duration: 0 })
              })
            }
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

.menu-hover {
  opacity: 0;
  visibility: hidden;
  transition-duration: 0.2s;
}

.menu-hover:hover {
  opacity: 1;
  visibility: visible;
}

.message-hover:hover + .menu-hover {
  opacity: 1;
  visibility: visible;
}
.rounded-menu {
  border-radius: 10px;
}
.rounded-card{
    border-radius:50px;
}
.text{
  font-style: normal;
  font-weight: bolder;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
}
.container {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.v-application--wrap {
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  position: relative;
}
.composer-popover.active {
  bottom: -100px !important;
  left:200px !important;
}
.filepond--root {
  background-color: #fff;
}
.v-image__image{
  width:100%;
  height:100%;
}
.message {
  font-family: Roboto;
  font-style: normal;
  font-weight: normal;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
  }
.time-text {
  font-family: Roboto;
  font-style: normal;
  font-weight: 500;
  font-size: 10px;
  letter-spacing: 1.5px;
}

</style>
