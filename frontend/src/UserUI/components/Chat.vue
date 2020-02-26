<template>
  <v-app>
    <div class="Chat">
      <v-card class="overflow-hidden">
        <v-app-bar
          absolute
          dark
          scroll-target="#scrolling-techniques"
        >
          <v-app-bar-nav-icon @click="drawer = true" />

          <v-toolbar-title>Диалог</v-toolbar-title>

          <v-spacer />
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-app-bar>
        <v-container>
          <v-navigation-drawer
            v-model="drawer"
            absolute
            temporary
          >
            <v-row no-gutters>
              <v-navigation-drawer
                v-model="drawer"
                dark
                mini-variant
                mini-variant-width="58px"
                absolute
              >
                <v-list>
                  <v-list-item>
                    <v-list-item-action>
                      <v-icon>mdi-chat</v-icon>
                    </v-list-item-action>
                  </v-list-item>

                  <v-divider />

                  <v-list-item>
                    <v-list-item-avatar>
                      <v-img src="https://www.technistone.com/color-range/image-slab/deska_gobi_black_p.jpg" />
                    </v-list-item-avatar>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-avatar>
                      <v-img src="https://www.technistone.com/color-range/image-slab/deska_gobi_black_p.jpg" />
                    </v-list-item-avatar>
                  </v-list-item>
                </v-list>
              </v-navigation-drawer>
              <v-list
                class="pa-9"
                nav
                dense
              >
                <v-list-item-group
                  v-model="group"
                >
                  <v-list-item class="grow">
                    <v-list-item-icon>
                      <v-icon>mdi-chat</v-icon>
                    </v-list-item-icon>
                    <v-list-item-text>Другой диалог</v-list-item-text>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-chat</v-icon>
                    </v-list-item-icon>
                    <v-list-item-text>Другой диалог</v-list-item-text>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-chat</v-icon>
                    </v-list-item-icon>
                    <v-list-item-text>Другой диалог</v-list-item-text>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-row>
          </v-navigation-drawer>
        </v-container>
        <v-sheet
          id="scrolling-techniques"
          class="overflow-y-auto"
          :height="windowHeight"
        >
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
          <v-list two-line>
            <v-card
              v-for="message in messages"
              :key="message.id"
              color="blue lighten-1"
              dark
              class="mx-auto"
              style="margin-top:20px;margin-bottom:20px"
              max-width="344"
            >
              <v-card-title>
                <span class="title font-weight-light">
                  {{ message.text }}
                </span>
              </v-card-title>
              <div style="text-align: right; margin-right:10px;margin-top:-25px;">
                <span class="font-weight-light">
                  От: {{ message.author }}
                </span>
              </div>
            </v-card>
          </v-list>
        </v-sheet>
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
          class="blue lighten-1"
          dark
          @click="goBack()"
        >
          Назад
        </v-btn>
      </v-card>
    </div>
  </v-app>
</template>

<script>
import jwt from 'jsonwebtoken'
import VueNativeSock from 'vue-native-websocket'
import VueCookie from 'vue-cookie'
import Vue from 'vue'
Vue.use(VueCookie)
Vue.use(
  VueNativeSock,
  'ws://' + window.location.host + '/ws/chat/' + '1' + '/',
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
  created () {
    this.id = window.location.search.slice(1, 99)
    console.log(window.location.host)
    this.$connect('ws://' + window.location.host + '/ws/chat/' + this.id + '/')
    this.get()
  },
  methods: {
    goBack () {
      window.history.length > 1 ? this.$router.go(-1) : this.$router.push('/')
    },
    GoAuth () {
      window.location.href = '/'
    },
    get () {
      this.$options.sockets.onmessage = data => {
        this.messages.push({
          id: this.messages.length,
          text: JSON.parse(data.data).message,
          author: JSON.parse(data.data).author
        })
        console.log(JSON.parse(data.data))
      }
    },
    send (messagetext) {
      if (localStorage.jwt) {
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
    }
  }
}
</script>

<style lang="scss">
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
.Chat {
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
