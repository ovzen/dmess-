<template>
  <div style="height:100%;">
    <v-row
      v-if="messages.length > 0"
      class="d-flex flex-column-reverse"
      style="padding-bottom:56px;height:100%;"
      align="end"
    >
      <v-container
        v-for="message in messages"
        :id="'Message_' + message.id"
        :key="message.id"
        py-2
      >
        <div
          v-if="!isOwnMessage(message.user)"
          class="text-left"
        >
          <v-card
            max-width="460px"
            class="float-right d-flex"
            style="border-radius: 20px;"
            color="background_pink"
            flat
          >
            <v-card-text>
              <span
                class="font-weight-light message_color--text"
              >
                {{ message.text }}
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
          class="d-flex"
          py-0
        >
          <div
            v-if="isOwnMessage(message.user)"
            class="text-left"
          >
            <v-card
              style="border-radius: 20px;"
              max-width="460px"
              class="d-flex"
              flat
            >
              <v-card-text>
                <span
                  class="font-weight-light message_color--text"
                >
                  {{ message.text }}
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
    <v-footer
      color="background_white"
      style="position:fixed;bottom:-12px;width:100%;box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2), 0px 2px 2px rgba(0, 0, 0, 0.12), 0px 0px 2px rgba(0, 0, 0, 0.14);"
    >
      <v-form
        class="d-inline-flex"
        style="padding-left:10px;padding:10px;padding-bottom:13px;padding-top:0px;margin-top:-5px"
      >
        <v-textarea
          ref="myTextArea"
          v-model="message"
          auto-grow
          autofocus
          rows="1"
          placeholder="Message"
          hide-details
          color="false"
          @keydown.enter.prevent=""
          @keyup.enter="sendMessage()"
        />
        <v-btn
          icon
          color="basic"
          class="align-self-sm-end"
          style="padding:5px;"
          @click="sendMessage()"
        >
          <v-icon>
            mdi-send
          </v-icon>
        </v-btn>
      </v-form>
    </v-footer>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import api from '../api'
import VueNativeSock from 'vue-native-websocket'
import VueCookie from 'vue-cookie'
import Vue from 'vue'
import jwt from 'jsonwebtoken'
import moment from 'moment'

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
  data: () => ({
    messages: [],
    message: '',
    dialogMessagesLength: 0,
    diailogId: 0
  }),
  computed: {
    ...mapGetters(['getUserId'])
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
  },
  beforeDestroy () {
    this.$disconnect()
  },
  methods: {
    ...mapActions(['getDialogsData']),
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
            .get('/api/messages/', { params: { dialog: this.diailogId, limit: 30, offset: this.messages.length, ordering: '-create_date' } })
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
      if (this.message) {
        console.log('messagetext: ', this.message)
        this.$socket.send(
          JSON.stringify({
            message: this.message
          })
        )
      }
      this.message = ''
    },
    updateDialog () {
      this.$disconnect()
      this.message = ''
      this.messages = []
      this.diailogId = this.$route.params.id
      api.axios.get('/api/messages/count/', { params: { dialog: this.diailogId } }).then(res => { this.dialogMessagesLength = res.data.count })
      api.axios
        .get('/api/messages/', { params: { dialog: this.diailogId, limit: 30, ordering: '-create_date' } })
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
      this.$connect((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/' + this.diailogId + '/')
      api.axios.post('/api/dialog/' + this.diailogId + '/read_messages/').then(res => {
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
          user_detail: { username: JSON.parse(data.data).author },
          create_date: JSON.parse(data.data).create_date.substring(1, JSON.parse(data.data).create_date.length - 1)
        })
        this.getDialogsData()
        this.dialogMessagesLength += 1
        var Data = this
        Vue.nextTick(function () {
          Data.$vuetify.goTo(document.getElementById('Message_' + computedMessageId))
        })
        api.axios.post('/api/dialog/' + this.diailogId + '/read_messages/')
      }
    },
    isOwnMessage (author) {
      return author === this.getUserId
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
</style>
