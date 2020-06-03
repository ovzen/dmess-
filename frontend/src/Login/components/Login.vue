<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-flex
      justify-center
      d-flex
    >
      <v-col
        md="7"
        lg="8"
        xl="5"
        justify-center
      >
        <v-card class="elevation-12">
          <v-layout>
            <v-footer
              width="60vh"
              style="background: linear-gradient(324.48deg, #4402EE 0%, #CE54FC 81.58%);"
            />
            <v-container>
              <v-toolbar-title class="text-center pt-7 text--secondary">
                Sign in
              </v-toolbar-title>
              <div>
                <v-card-text>
                  <v-row justify="center">
                    <v-col
                      md="9"
                      lg="10"
                      xl="9"
                    >
                      <v-text-field
                        v-model="login"
                        label="Login"
                        hint="Email specified during registration"
                        clearable
                        required
                        outlined
                        :error-messages="error_text"
                        @keyup.enter="FocusOn('password')"
                      />

                      <v-text-field
                        ref="password"
                        v-model="password"
                        :append-icon="vanish ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="vanish ? 'text' : 'password'"
                        clearable
                        label="Password"
                        hint="Your password"
                        required
                        outlined
                        @click:append="vanish = !vanish"
                        @keyup.enter="auth(login, password)"
                      />
                    </v-col>
                  </v-row>
                </v-card-text>
              </div>
              <v-card-actions>
                <v-row justify="space-around">
                  <v-btn
                    tile
                    outlined
                    color="purple darken-4"
                    @click="auth(login, password)"
                  >
                    SIGN IN
                  </v-btn>
                </v-row>
              </v-card-actions>

              <v-card-actions class="text-center">
                <v-card-text class="text--secondary caption ">
                  DON`T HAVE AN ACCOUNT?
                  <a>
                    <u
                      class="text--secondary"
                      style="font-style: normal; font-family: Roboto;"
                      @click="GoToRegister()"
                    >
                      SIGN UP!
                    </u>
                  </a>
                  <v-card-text>
                    <a>
                      <u
                        class="text--secondary caption"
                        style="font-style: normal; font-family: Roboto;"
                        @click="send_reset_password_link(login)"
                      >
                        FORGOT PASSWORD?
                      </u>
                    </a>
                  </v-card-text>
                </v-card-text>
              </v-card-actions>
            </v-container>
          </v-layout>
        </v-card>
      </v-col>
    </v-flex>
  </v-container>
</template>

<script>
import api from '../api'
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
    next: '',
    vanish: false,
    error_text: ''
  }),

  created () {
    if (this.$route.query.next) {
      this.next = 'http://' + window.location.host + this.$route.query.next
    } else {
      this.next = 'http://' + window.location.host
      this.login = this.$root.$children[0].login
    }
  },
  methods: {
    GoToRegister () {
      this.$root.$children[0].login = this.login
      this.$router.push('/register/')
    },
    auth (username, password) {
      api.axios
        .post('/api/token/', {
          username: username,
          password: password
        })
        .catch(err => {
          if (err !== 0) {
            this.error_text = 'Invalid Login or Password'
            console.log(err)
          } else if (err === 0) {
            this.error_text = ''
          }
        })
        .then(res => {
          if (res) {
            console.log(res.data)
            this.$cookie.set('Authentication', res.data.access, {
              expires: '5m'
            })
            localStorage.setItem('UpdateKey', res.data.refresh)
            this.button =
              'Приветствуем ' +
              jwt.decode(this.$cookie.get('Authentication')).name
            console.log(jwt.decode(this.$cookie.get('Authentication')))
            window.location.href = this.next
        }
        })
    },
    send_reset_password_link (login) {
      if (login.length) {
        api.axios
        .post('/api/accounts/send-reset-password-link/', {
          login: login
        })
        .catch(err => {
          if (err !== 0) {
            this.error_text = 'Unknown or invalid login'
            console.log(err)
          } else if (err === 0) {
            this.error_text = ''
          }
        })
        .then(res => {
          if (res && res.status === 200) {
            this.$router.push('/reset-password/')
          }
        })
      }
    },
    FocusOn (value) {
      this.$nextTick(() => {
        this.$refs[value].focus()
      })
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
