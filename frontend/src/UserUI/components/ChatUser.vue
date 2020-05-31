<template>
  <div style="height:100%;">
    <v-row
      v-if="messages.length > 0"
      class="d-flex flex-column-reverse"
      style="padding-bottom:0px;height:100%;"
      align="end"
    >
      <v-container
        v-for="message in messages"
        :id="'Message_' + message.id"
        :key="message.id"
        py-2
      >
        <div
          v-if="isOwnMessage(message.user)"
          class="text-left"
        >
          <v-card
            style="border-radius: 20px;width:min-content"
            max-width="460px"
            class="d-flex align-content-start flex-wrap flex-shrink-1"
            flat
          >
            <v-container
              class="d-inline-flex align-content-center"
              pb-0
              mb-0
            >
              <v-img
                style="border-radius: 4px"
                :src="message.image_url"
                max-width="440px"
                min-width="200px"
                @click="dialog=true,link=message.image_url"
              />
            </v-container>
            <v-card-text
              style="padding-top: 3px"
            >
              <span
                class="font-weight-light message_color--text"
              >
                {{ decodeEmojiCode(message.text) }}
              </span>
              <span
                class="float-right ml-2"
              >
                {{ formatTime(message.create_date) }}
              </span>
            </v-card-text>
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
              style="border-radius: 20px;width:min-content"
              max-width="460px"
              class="d-flex align-content-start flex-wrap flex-shrink-1"
              color="background_pink"
              flat
            >
              <v-container
                class="d-inline-flex align-content-center"
                pb-0
                mb-0
              >
                <v-img
                  style="border-radius: 4px"
                  :src="message.image_url"
                  max-width="440px"
                  min-width="200px"
                  @click="dialog=true,link=message.image_url"
                />
              </v-container>
              <v-card-text
                style="padding-top: 3px"
              >
                <span
                  class="font-weight-light message_color--text"
                >
                  {{ decodeEmojiCode(message.text) }}
                </span>
                <span
                  class="float-right ml-2"
                >
                  {{ formatTime(message.create_date) }}
                </span>
              </v-card-text>
            </v-card>
          </div>
        </v-container>
      </v-container>
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
    <file-pond
      ref="pond2"
      name="image"
      :disabled="true"
      style="padding-bottom:120px;max-width=440px;min-width:200px"
      :files="['/media/index.js']"
      :instant-upload="false"
      :allow-download-by-url="true"
      label-idle="Drop files here..."
    />
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
    <file-pond
      ref="pond"
      name="image"
      :style="'position:fixed;width:450px;left:' + this.$vuetify.application.left +'px;max-height:80%;transition-duration: .25s;bottom:' + (hide ? '20' : '-100') + 'px'"
      label-idle="Drop files here..."
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
        @keyup.enter="sendMessage()"
      />
      <Emoji
        style="padding-right: 28px; margin-left: 10px;"
        @click="selectedEmoji"
      />

      <v-btn
        icon
        color="basic"
        :disabled="loading"
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
const FilePond = vueFilePond(FilePondPluginFileValidateType, FilePondPluginImagePreview, FilePondPluginGetFile)
Vue.directive('linkified', linkify)
require('./css/vue-chat-emoji.css')
Vue.use(VueCookie)
Vue.use(
  VueNativeSock,
  (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/' + window.location.search.slice(1, 99) + '/',
  {
    connectManually: true
  }
)
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
    dialogMessagesLength: 0,
    dialogId: 0,
    imageUrl: '',
    dialog: false,
    loading: false,
    fileExtension: null,
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
    this.updateDialog()
    this.getMessage()
    this.UpdateUserInDialog()
  },
  beforeDestroy () {
    this.$disconnect()
  },
  methods: {
    handleFilePondInit: function () {
      console.log('FilePond has initialized')
    },
    ...mapActions(['getDialogsData', 'getUserData']),
    beforeupload (file, progress) {
      console.log('beforeupload', file, progress)
      this.fileExtension = progress.fileExtension
      this.loading = true
      this.hide = true
      const pond = FilePond.create()
      pond.addFile('./ChatUser.vue')
    },
    afterupload (file, progress) {
      console.log('afterupload', file, progress)
      this.imageUrl = progress.serverId
      this.loading = false
    },
    decodeEmojiCode (str) {
      return emojis.decodeEmoji(str)
    },
    selectedEmoji (args) {
      this.message += args.emoji
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
    sendMessage () {
      console.log(this.$refs)
      if (!this.loading) {
        console.log('messagetext: ', this.message)
        if (this.imageUrl === '') {
          this.$socket.send(
            JSON.stringify({
              message: emojis.encodeEmoji(this.message),
              image_url: ''
            })
          )
        } else {
          this.$socket.send(
            JSON.stringify({
              message: emojis.encodeEmoji(this.message),
              image_url: JSON.parse(this.imageUrl).image_url
            })
          )
        }
      }
      this.myFiles = []
      this.imageUrl = ''
      this.hide = false
      this.message = ''
    },
    updateDialog () {
      this.$disconnect()
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
      this.$connect((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/' + this.dialogId + '/')
      api.axios.post('/api/dialog/' + this.dialogId + '/read_messages/').then(res => {
        if (res.status === 200) {
          this.getDialogsData()
        }
      })
    },
    getMessage () {
      this.$options.sockets.onmessage = data => {
        console.log(data)
        let computedMessageId = (this.messages[0].id || this.messages[this.messages.length + 1].id) + 1
        this.messages.unshift({
          id: computedMessageId,
          text: JSON.parse(data.data).message,
          user: JSON.parse(data.data).author,
          create_date: JSON.parse(data.data).create_date.substring(1, JSON.parse(data.data).create_date.length - 1),
          image_url: JSON.parse(data.data).image_url
        })
        this.getDialogsData()
        this.dialogMessagesLength += 1
        var Data = this
        Vue.nextTick(function () {
          Data.$vuetify.goTo(document.getElementById('Message_' + computedMessageId))
        })
        api.axios.post('/api/dialog/' + this.dialogId + '/read_messages/')
      }
    },
    UpdateUserInDialog () {
      if (typeof this.getUsersByDialogId(this.$route.params.id) !== 'undefined') {
        this.getUserData([this.getUsersByDialogId(this.$route.params.id)[0].id, true])
      }
      setTimeout(this.UpdateUserInDialog, 30000)
    },
    isOwnMessage (author) {
      console.log(author, jwt.decode(this.$cookie.get('Authentication')).user_id)
      return author !== jwt.decode(this.$cookie.get('Authentication')).user_id
    },
    formatTime (datetime) {
      if (datetime) {
        if (moment(datetime).isBefore(moment(), 'day')) {
          return moment(String(datetime)).format('DD.MM.YYYY')
        } else {
          return moment(String(datetime)).format('hh:mm')
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
.test{
  background: rgba(0, 0, 0, 0.1);
}
.filepond--item-panel{
  background: rgba(0, 0, 0, 0.1) !important
}
</style>
