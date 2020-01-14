<template>
  <v-app>
  <a href="/admin" style="text-decoration: none;"><v-btn class="ma-2" outlined color="indigo" >Комнатка админа</v-btn></a>
  <v-form>
    <v-container>
      <v-row>
          <v-text-field
            v-model="login"
            label="Login"
            clearable
            required
          ></v-text-field>

        <v-col
          cols="12"
          md="1"
        >
        </v-col>
          <v-text-field
            v-model="password"
            clearable
            label="Password"
            required
          ></v-text-field>
      </v-row>
      <div class="text-center">
      <v-btn class="ma-2" outlined color="indigo" v-text="button" @click="auth(login,password)" >Войти</v-btn>
      </div>
    </v-container>
    </v-form>
    <v-card>
          <v-toolbar color="blue lighten-1" dark>
            <v-toolbar-title style="font-weight:1;">Сообщения</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon>
              <v-icon></v-icon>
            </v-btn>
          </v-toolbar>
          <v-list two-line>
            <v-card color="blue lighten-1" dark class="mx-auto" style="margin-top:20px;margin-bottom:20px" max-width="344" v-for="message in messages" :key="message.id">
              <v-card-title>
                <span class="title font-weight-light">{{message.text}}</span>
              </v-card-title>
          </v-card>
            <v-flex xs12 style="margin-top:-5px;margin-left:30px;margin-right:30px;margin-bottom:-10px">
              <v-row>
              <v-text-field
                clearable
                style="margin:auto;"
                label="Сообщение"
                color="blue lighten-1"
                v-model="message_text"
              ></v-text-field>
            <v-btn class="ma-2" outlined color="indigo" @click="send(message_text)">Отправить</v-btn>
            </v-row>
            </v-flex>
          </v-list>
        </v-card>
  </v-app>
</template>

<script>
import api from '@/api';
import jwt from 'jsonwebtoken'
import VueNativeSock from 'vue-native-websocket'
import Vue from 'vue'
Vue.use(VueNativeSock, 'ws://' + window.location.host + '/ws/chat/',)
export default {
  name: 'App',
  data: () => ({
    login: "",
    button: "Войти",
    password: "",
    message_text: "",
    data: "",
    messages: [], 
  }),
  methods: {
    get() {
      this.$options.sockets.onmessage = (data) => {this.messages.push({'text': JSON.parse(data.data).message, 'id' : this.messages.length});console.log(JSON.parse(data.data).message)}
    },
    send(message_text) {
      if (message_text) {
            this.$socket.send(JSON.stringify({
                'message': message_text
            }))
        }
    },
    auth(username,password) {
      api.axios.post('/api/token/', {"username": username, "password": password}).then((res) => {
        console.log(res.data)
        localStorage.setItem('jwt', res.data.access)
        this.button="Приветствуем " + jwt.decode(localStorage.jwt).name
        console.log(jwt.decode(localStorage.jwt))
      })
    },
  },
  created() {
    this.get()
  }
}
</script>
