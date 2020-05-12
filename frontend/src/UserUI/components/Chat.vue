<template>
  <v-container fluid>
    <v-dialog
      v-model="dialog"
      width="100%"
    >
      <v-card dark>
        <v-card-title
          class="blue lighten-1"
          primary-title
        >
          Ошибка
        </v-card-title>

        <div
          class="grey lighten-4"
          style="color:red;"
        >
          <h2 style="font-weight:400;text-align: center;color:red;">
            Вы не вошли!!!
          </h2>
        </div>
        <v-divider class="grey lighten-2" />
        <v-card-actions class="grey lighten-4">
          <v-spacer />
          <v-btn
            color="primary"
            text
            @click="GoAuth()"
          >
            Войти
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-list
      two-line
      max-height="65vh"
      style="overflow:auto"
    >
      <v-card
        v-for="message in messages"
        :key="message.id"
        color="blue lighten-1"
        dark
        style="margin-top:20px; margin-bottom:20px;"
        :style="isOwnMessage(message.user_detail.username) ? 'margin: 20px 20px 20px auto' : 'margin: 20px auto 20px 20px'"
        max-width="344"
      >
        <v-card-text class="headline text-left">
          {{ message.text }}
        </v-card-text>
        <div style="text-align: right; margin-right:10px; margin-top:-25px;">
          <span class="font-weight-light">
            От: {{ message.user_detail.username }}<br>
            {{ decodeTime(message.create_date) }}
          </span>
        </div>
      </v-card>
    </v-list>
    <v-flex
      xs12
      style="margin-top:-5px;margin-left:30px;margin-right:30px;margin-bottom:-10px"
    >
      <v-row>
        <v-text-field
          v-model="message_text"
          clearable
          style="margin:auto;"
          label="Сообщение"
          color="blue lighten-1"
          @keyup.enter="send(message_text)"
        />
        <v-btn
          class="ma-2"
          outlined
          color="primary"
          @click="send(message_text)"
        >
          Отправить
        </v-btn>
      </v-row>
    </v-flex>
    <v-btn
      width="99%"
      class="blue lighten-1 ma-2"
      dark
    >
      Сохранить в базу знаний
    </v-btn>
    <v-btn
      width="99%"
      class="blue lighten-1"
      dark
      @click="goBack()"
    >
      Назад
    </v-btn>
  </v-container>
</template>

<script>
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
  name: 'Chat',
  data: () => ({
    login: '',
    button: 'Войти',
    password: '',
    message_text: '',
    data: '',
    messages: [],
    dialog: false,
    id: 0,
    drawer: false,
    windowHeight: window.innerHeight - 160
  }),
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['Update']
  },
  mounted () {
    this.Update()
    this.get()
  },
  beforeDestroy () {
    this.$disconnect()
  },
  methods: {
    Update () {
      this.$disconnect()
      this.messages = []
      this.id = this.$route.params.id
      api.axios.get('/api/messages/', { params: { dialog: this.id } }).then(res => {
        this.messages = this.messages.concat(res.data.results)
      })
      this.$connect((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/' + this.id + '/')
      api.axios.post('/api/dialog/' + this.id + '/read_messages/')
    },
    goBack () {
      window.history.length > 1 ? this.$router.go(-1) : this.$router.push('/')
    },
    GoAuth () {
      window.location.reload()
    },
    get () {
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
    send (messagetext) {
      if (this.$cookie.get('Authentication')) {
        if (messagetext) {
          console.log('messagetext: ', messagetext)
          this.$socket.send(
            JSON.stringify({
              message: messagetext
            })
          )
          this.message_text = undefined
        }
      } else {
        this.dialog = true
      }
    },
    isOwnMessage (author) {
      return author === jwt.decode(this.$cookie.get('Authentication')).name
    },
    formatDate (date) {
      if (date) {
        moment.locale('ru')
        if (moment(date).isBefore(moment(), 'day')) {
          return moment(String(date)).format('DD.MM.YYYY')
        } else {
          return moment(String(date)).calendar()
        }
      }
    },
    decodeTime (datetime) {
      if (datetime) {
        moment.locale('ru')
        if (moment(datetime).isBefore(moment(), 'day')) {
          return moment(String(datetime)).format('DD.MM.YYYY')
        } else {
          return moment(String(datetime)).calendar()
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
  min-height: 10px;
  max-width: 100%;
  position: relative;
}
</style>
