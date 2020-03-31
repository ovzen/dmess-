<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        cols="12"
        sm="8"
        md="4"
      >
        <v-card
          class="elevation-12"
        >
          <v-toolbar-title
            class="text-center pt-7 text--secondary"
          >
            {{ RegTitle }}
          </v-toolbar-title>

          <v-window v-model="step">
            <v-window-item :value="1">
              <v-card-text>
                <v-text-field
                  v-model="email"
                  clearable
                  label="E-mail"
                  hint="Email specified during registration"
                  :rules="emailRules"
                  name="email"
                  outlined
                />

                <v-text-field
                  v-model="login"
                  label="Username"
                  hint="Your personal username"
                  clearable
                  required
                  name="username"
                  :rules="loginRules"
                  outlined
                />
              </v-card-text>
            </v-window-item>

            <v-window-item :value="2">
              <v-card-text>
                <v-text-field
                  v-model="name"
                  clearable
                  label="First Name"
                  hint="Your first name"
                  name="first_name"
                  outlined
                />

                <v-text-field
                  v-model="secondname"
                  clearable
                  label="Last Name"
                  hint="Your last name"
                  name="last_name"
                  outlined
                />
              </v-card-text>
            </v-window-item>

            <v-window-item :value="3">
              <v-card-text>
                <v-text-field
                  v-model="password"
                  :append-icon="vanish ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="vanish ? 'text' : 'password'"
                  clearable
                  label="Password"
                  hint="Password must contain letters and numbers"
                  required
                  outlined
                  name="password"
                  :rules="passwordRules"
                  @click:append="vanish = !vanish"
                />

                <v-text-field
                  v-model="repeatpassword"
                  :append-icon="vanish ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="vanish ? 'text' : 'password'"
                  clearable
                  label="Repeat Password"
                  hint="Repeat your password"
                  required
                  outlined
                  name="Repeat_password"
                  :rules="repeatpasswordRules"
                  @click:append="vanish = !vanish"
                />
              </v-card-text>
            </v-window-item>
          </v-window>

          <v-card-actions>
            <v-btn
              fab
              mr="3"
              color="indigo"
              :disabled="step === 1"
              @click="step--"
            >
              <v-card-center class="headline font-weight-thin">
                &larr;
              </v-card-center>
            </v-btn>
            <v-spacer />

            <v-btn
              class="ma-2"
              :disabled="step <= 2"
              tile
              outlined
              color="indigo"
              @click="Register(login, password, repeatpassword, name, secondname, email)"
            >
              SIGN UP
            </v-btn>
            <v-spacer />
            <v-btn
              ml="3"
              fab
              :disabled="step === 3"
              color="indigo"
              @click="step++"
            >
              <v-card-center class="center headline">
                →
              </v-card-center>
            </v-btn>
          </v-card-actions>

          <v-card-actions>
            <v-spacer />
            <v-card-center class="text--secondary caption mb-7">
              DON`T HAVE ACCOUNT? <a>
                <u
                  class="text--secondary"
                  @click="GoToLogin()"
                >
                  SIGN UP!
                </u>
              </a>
            </v-card-center>
            <v-spacer />
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '../api'
import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)
export default {
  name: 'Register',
  data: () => ({
    login: '',
    password: '',
    name: '',
    repeatpassword: '',
    secondname: '',
    email: '',
    ChatId: null,
    button: 'Войти',
    message_text: '',
    next: '',
    vanish: false,
    step: 1,
    loginRules: [
      v => !!v || 'Введите логин',
      v => (v || '').length >= 2 ||
              `Minimal length of username is 2 symbols`
    ],
    emailRules: [
      v => /.+@.+\..+/.test(v) || v.length <= 0 || 'Электронная почта должна быть действительной'
    ]
  }),
  computed: {
    RegTitle () {
      switch (this.step) {
        case 1: return 'Sign Up'
        case 2: return 'Sign Up'
        default: return 'Sign Up'
      }
    },
    repeatpasswordRules () {
      const rules = []
      rules.push(v => !!v || 'Повторите пароль')
      rules.push(v => (!!v && v) === this.password ||
              'Пароли не совпадают')
      return rules
    },
    passwordRules () {
      const rules = []
      rules.push(v => !!v || 'Введите пароль')
      return rules
    }
  },
  watch: {
    repeatpassword: 'validateField',
    password: 'validateField'
  },
  created () {
    if (this.$route.query.next) {
      this.next = 'http://' + window.location.host + this.$route.query.next
    } else {
      this.next = 'http://' + window.location.host
    }
    this.login = this.$root.$children[0].login
    this.name = this.$root.$children[0].name
    this.secondname = this.$root.$children[0].secondname
    this.email = this.$root.$children[0].email
  },
  methods: {
    validateField () {
      this.$refs.passwords.validate()
    },
    GoToLogin () {
      this.$root.$children[0].login = this.login
      this.$root.$children[0].name = this.name
      this.$root.$children[0].secondname = this.secondname
      this.$root.$children[0].email = this.email
      this.$router.push('/login/')
    },
    Register (username, password, repeatpassword, name, secondname, email) {
      if ((username && password) && (password === repeatpassword)) {
        api.axios
          .post('/api/register/', {
            username: username,
            password: password,
            first_name: name,
            last_name: secondname,
            email: email
          })
          .catch(error => {
            console.log(error)
            if (error.response.status === 400) {
              alert('Пользователь с таким именем уже существует.')
            }
          }).then(data => {
            if (data.status === 201) {
              api.axios.post('/api/token/', {
                username: username,
                password: password
              }).then(res => {
                console.log(res.data)
                this.$cookie.set('Authentication', res.data.access, {
                  expires: '5m'
                })
                window.location.href = this.next
              })
            }
          })
      }
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