<template>
    <v-app>
        <a href="/admin" style="text-decoration: none;">
            <v-btn class="ma-2" outlined color="indigo">Комнатка админа</v-btn>
        </a>
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
                    <v-btn class="ma-2" outlined color="indigo" v-text="button" @click="auth(login,password)">Войти
                    </v-btn>
                    <v-btn class="ma-2" outlined color="indigo" @click="Register(login,password)">Регистрация</v-btn>
                    <v-btn class="ma-2" outlined color="indigo" @click="Check()">Проверить</v-btn>
                    <v-btn class="ma-2" outlined color="indigo" @click="Exit()">Выйти</v-btn>
                </div>
            </v-container>
        </v-form>
        <v-card>
            <v-dialog v-model="dialog" width="500">
                <v-card dark>
                    <v-card-title
                            class="blue lighten-1"
                            primary-title
                    >
                        Ошибка
                    </v-card-title>

                    <div class="grey lighten-4" style="color:red;">
                        <h2 style="font-weight:400;text-align: center;color:red;">Вы не вошли!!!</h2>
                    </div>
                    <v-divider class="grey lighten-2"></v-divider>
                    <v-card-actions class="grey lighten-4">
                        <v-spacer></v-spacer>
                        <v-btn
                                color="primary"
                                text
                                @click="dialog = false"
                        >
                            Войти
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-toolbar color="blue lighten-1" dark>
                <v-toolbar-title style="font-weight:1;">Сообщения</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn icon>
                    <v-icon></v-icon>
                </v-btn>
            </v-toolbar>
            <v-list two-line>
                <v-card color="blue lighten-1" dark class="mx-auto" style="margin-top:20px;margin-bottom:20px"
                        max-width="344" v-for="message in messages" :key="message.id">
                    <v-card-title>
                        <span class="title font-weight-light">{{message.text}}</span>
                    </v-card-title>
                    <div style="text-align: right; margin-right:10px;margin-top:-25px;">
                        <span class="font-weight-light">От: {{message.author}}</span>
                    </div>
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
import VueCookie from 'vue-cookie'
import Vue from 'vue'
Vue.use(VueCookie)
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
    dialog: false, 
  }),
  methods: {
    get() {
      this.$options.sockets.onmessage = (data) => {this.messages.push({'id' : this.messages.length, 'text': JSON.parse(data.data).message, 'author' : JSON.parse(data.data).author});console.log(JSON.parse(data.data))}
    },
    send(message_text) {
      if (localStorage.jwt){
      if (message_text) {
            this.$socket.send(JSON.stringify({
                'message': message_text,
                'author' : jwt.decode(localStorage.jwt).name
            }))
        }}
        else {
          this.dialog=true
        }
    },
    Check() {
      api.axios.get('/hello/').then((res) => {
        console.log(res.data)
      })
    },
    Exit() {
      localStorage.removeItem('jwt')
    },
    Register(username,password) {
      api.axios.post('/api/register/', {"username": username, "password": password}).then((res) => {
        console.log(res.data)
        localStorage.setItem('jwt', res.data.access)
        this.button="Приветствуем " + jwt.decode(localStorage.jwt).name
        console.log(jwt.decode(localStorage.jwt))
      }).catch(error => {
        if (error.response.status===401) {
          this.button='Ошибка неправильное имя пользователя или пароль'
        }
    console.log(error.response.status)
    })
    },
    auth(username,password) {
      api.axios.post('/api/token/', {"username": username, "password": password}).then((res) => {
        console.log(res.data)
        localStorage.setItem('jwt', res.data.access)
        this.$cookie.set('Authentication', res.data.access , {expires: '5m'});
        this.button="Приветствуем " + jwt.decode(localStorage.jwt).name
        console.log(jwt.decode(localStorage.jwt))
      }).catch(error => {
        if (error.response.status===401) {
          this.button='Ошибка неправильное имя пользователя или пароль'
        }
    console.log(error.response.status)
});
    },
  },
  created() {
    this.get()
  }
}



</script>
