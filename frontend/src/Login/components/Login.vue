<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-flex
      justify-center
      d-flex
    >
      <v-card
        class="elevation-12"
      >
        <v-layout>
          <v-img src="/static/log.JPG" />
          <v-row
            align="center"
            justify="center"
          >
            <v-toolbar-title class="text-center pt-7 text--secondary">
              Sign in
            </v-toolbar-title>

            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="login"
                  label="Login"
                  hint="Email specified during registration"
                  clearable
                  required
                  outlined
                />

                <v-text-field
                  v-model="password"
                  :append-icon="vanish ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="vanish ? 'text' : 'password'"
                  clearable
                  label="Password"
                  hint="Your password"
                  required
                  outlined
                  @click:append="vanish = !vanish"
                />
              </v-form>
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn
                class="ma-2"
                tile
                outlined
                color="indigo"
                @click="auth(login, password)"
              >
                SIGN IN
              </v-btn>
              <v-spacer />
            </v-card-actions>

            <v-card-actions>
              <v-spacer />
              <v-card-center class="text--secondary caption mb-7">
                DON`T HAVE AN ACCOUNT? <a>
                  <u
                    class="text--secondary"
                    @click="GoToRegister()"
                  >
                    SIGN UP
                  </u>
                </a>
              </v-card-center>
              <v-spacer />
            </v-card-actions>
          </v-row>
        </v-layout>
      </v-card>
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
    vanish: false
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
        .then(res => {
          console.log(res.data)
          this.$cookie.set('Authentication', res.data.access, {
            expires: '5m'
          })
          localStorage.setItem('UpdateKey', res.data.refresh)
          this.button = 'Приветствуем ' + jwt.decode(this.$cookie.get('Authentication')).name
          console.log(jwt.decode(this.$cookie.get('Authentication')))
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
