<template>
  <v-app>
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
        </div>
      </v-container>
    </v-form>
  </v-app>
</template>

<script>
import api from './api'
import jwt from 'jsonwebtoken'
import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)
export default {
  name: 'Login',
  data: () => ({
    login: '',
    ChatId: null,
    button: 'Войти',
    password: '',
    message_text: '',
    next: ''
  }),
  created () {
    this.next = 'http://' + window.location.host + window.location.search.slice(6, 99)
  },
  methods: {
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
          window.location.href = this.next
        })
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
