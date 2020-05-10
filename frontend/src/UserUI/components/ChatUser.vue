<template>
  <div>
    <v-container
      v-for="(message, i) in messages"
      :key="i"
      py-2
    >
      <div
        v-if="isOwnMessage(message.user_detail.username)"
        class="text-left"
      >
        <v-card
          max-width="460px"
          class="float-right d-flex"
          style="border-radius: 20px;"
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
          v-if="!isOwnMessage(message.user_detail.username)"
          class="text-left"
        >
          <v-card
            style="border-radius: 20px;"
            max-width="460px"
            class="d-flex"
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
      </v-container>
    </v-container>
    <ChatInput />
  </div>
</template>

<script>
import ChatInput from './ChatInput'
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
  components: { ChatInput },
  data: () => ({
    messages: [],
    diailogId: 0
  }),
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['updateDialog']
  },
  mounted () {
    this.updateDialog()
    this.getMessage()
  },
  beforeDestroy () {
    this.$disconnect()
  },
  methods: {
    updateDialog () {
      this.$disconnect()
      this.messages = []
      this.diailogId = this.$route.params.id
      api.axios
        .get('/api/messages/', { params: { dialog: this.diailogId } })
        .then(response => {
          this.messages = this.messages.concat(response.data.results)
        })
      this.$connect((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/' + this.id + '/')
      api.axios.post('/api/dialog/' + this.id + '/read_messages/')
    },
    getMessage () {
      this.$options.sockets.onmessage = data => {
        this.messages.push({
          id: this.messages.length,
          text: JSON.parse(data.data).message,
          user_detail: { username: JSON.parse(data.data).author },
          create_date: JSON.parse(data.data).create_date.substring(1, JSON.parse(data.data).create_date.length - 1)
        })
        console.log(JSON.parse(data.data))
        api.axios.post('/api/dialog/' + this.id + '/read_messages/')       
      }
    },
    isOwnMessage (author) {
      return author === jwt.decode(this.$cookie.get('Authentication')).name
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
