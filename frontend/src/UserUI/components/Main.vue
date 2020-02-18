<template>
  <v-app>
    <a
      href="django_admin/"
      style="text-decoration: none;"
    >
      <v-btn
        class="ma-2"
        outlined
        color="indigo"
      >
        Комнатка админа
      </v-btn>
    </a>
    <a
      href="/admin"
      style="text-decoration: none;"
    >
      <v-btn
        class="ma-2"
        outlined
        color="indigo"
      >
        Комнатка модератора
      </v-btn>
    </a>
    <v-form>
      <v-container>
        <v-row>
          <v-text-field
            v-model="login"
            label="Login"
            clearable
            required
          />
          <v-col
            cols="12"
            md="1"
          />
          <v-text-field
            v-model="password"
            clearable
            label="Password"
            required
          />
        </v-row>
        <div class="text-center">
          <v-btn
            class="ma-2"
            outlined
            color="primary"
            @click="auth(login, password)"
            v-text="button"
          >
            Войти
          </v-btn>
          <v-btn
            class="ma-2"
            outlined
            color="primary"
            @click="Register(login, password)"
          >
            Регистрация
          </v-btn>
          <v-btn
            class="ma-2"
            outlined
            color="primary"
            @click="Exit()"
          >
            Выйти
          </v-btn>
        </div>
      </v-container>
    </v-form>
    <v-form>
      <v-container>
        <v-row>
          <v-text-field
            v-model="ChatId"
            clearable
            label="Chat id"
            required
          />
          <v-btn
            class="ma-2"
            outlined
            color="primary"
            @click="FindChat(ChatId)"
          >
            Перейти в чат
          </v-btn>
        </v-row>
      </v-container>
    </v-form>
    <router-link to="/chat/1">Перейти к chat</router-link>
  </v-app>
</template>

<script>
import api from '../api'
import jwt from 'jsonwebtoken'
import VueCookie from 'vue-cookie'
import Vue from 'vue'
Vue.use(VueCookie)
export default {
  name: 'App',
  data: () => ({
    login: '',
    ChatId: null,
    button: 'Войти',
    password: '',
    message_text: '',
    data: ''
  }),
  methods: {
    FindChat (id) {
      if (id) {
        this.$router.push('chat/' + id)
      }
    },
    Exit () {
      localStorage.removeItem('jwt')
      this.$cookie.delete('Authentication')
      location.reload()
    },
    Register (username, password) {
      if (username && password) {
        api.axios
          .post('/api/register/', {
            username: username,
            password: password
          })
          .catch(error => {
            if (error.response.status === 400) {
              alert('Пользователь с таким именем уже существует')
            }
          })
      }
    },
    auth (username, password) {
      api.axios
        .post('/api/token/', {
          username: username,
          password: password
        })
        .then(res => {
          console.log(res.data)
          localStorage.setItem('jwt', res.data.access)
          this.$cookie.set('Authentication', res.data.access, {
            expires: '5m'
          })
          this.button = 'Приветствуем ' + jwt.decode(localStorage.jwt).name
          console.log(jwt.decode(localStorage.jwt))
        })
        .catch(error => {
          if (error.response.status === 401) {
            this.button = 'Ошибка неправильное имя пользователя или пароль'
          }
          console.log(error.response.status)
        })
    }
  }
}
</script>
