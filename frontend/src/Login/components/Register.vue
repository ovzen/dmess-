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
            <v-img
              src="/static/reg.JPG"
            />
            <v-container>
              <v-toolbar-title class="text-center pt-7 text--secondary">
                {{ RegTitle }}
              </v-toolbar-title>
              <div>
                <v-window v-model="step">
                  <v-window-item :value="1">
                    <v-card-text>
                      <v-row justify="center">
                        <v-col
                          md="9"
                          lg="10"
                          xl="9"
                        >
                          <v-text-field
                            v-model="email"
                            clearable
                            label="E-mail"
                            hint="Email specified during registration"
                            :rules="emailRules"
                            name="email"
                            outlined
                            @keyup.enter="FocusOn('login')"
                          />

                          <v-text-field
                            ref="login"
                            v-model="login"
                            label="Username"
                            hint="Your personal username"
                            clearable
                            required
                            name="username"
                            :rules="loginRules"
                            outlined
                            @keyup.enter="step++"
                          />
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-window-item>

                  <v-window-item :value="2">
                    <v-card-text>
                      <v-row justify="center">
                        <v-col
                          md="7"
                          lg="10"
                          xl="9"
                        >
                          <v-text-field
                            v-model="name"
                            clearable
                            label="First Name"
                            hint="Your first name"
                            name="first_name"
                            outlined
                            @keyup.enter="FocusOn('secondname')"
                          />

                          <v-text-field
                            ref="secondname"
                            v-model="secondname"
                            clearable
                            label="Last Name"
                            hint="Your last name"
                            name="last_name"
                            outlined
                            @keyup.enter="step++"
                          />
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-window-item>

                  <v-window-item :value="3">
                    <v-card-text>
                      <v-row justify="center">
                        <v-col
                          md="9"
                          lg="10"
                          xl="9"
                        >
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
                            @keyup.enter="FocusOn('repeatpassword')"
                          />

                          <v-text-field
                            ref="repeatpassword"
                            v-model="repeatpassword"
                            :error-messages="usernameError"
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
                            @keyup.enter="Register(login, password, repeatpassword, name, secondname, email)"
                          />
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-window-item>
                </v-window>
              </div>
              <v-card-actions>
                <v-row justify="space-around">
                  <v-btn
                    fab
                    small
                    color="purple darken-4"
                    :disabled="step === 1"
                    @click="step--"
                  >
                    <v-icon class="text-center headline white--text">
                      mdi-arrow-left
                    </v-icon>
                  </v-btn>

                  <v-btn
                    :disabled="step <= 2"
                    tile
                    outlined
                    color="purple darken-4"
                    @click="Register(login, password, repeatpassword, name, secondname, email)"
                  >
                    SIGN UP
                  </v-btn>
                  <v-btn
                    fab
                    small
                    :disabled="step === 3"
                    color="purple darken-4"
                    @click="step++"
                  >
                    <v-icon class="text-center headline white--text">
                      mdi-arrow-right
                    </v-icon>
                  </v-btn>
                </v-row>
              </v-card-actions>
              <v-snackbar
                v-model="snackbar"
                :multi-line="multiLine"
              >
                {{ notificationErrors }}
                <v-btn
                  color="red"
                  text
                  @click="snackbar = false"
                >
                  Close
                </v-btn>
              </v-snackbar>
              <v-card-actions class="text-center">
                <v-card-text class="text--secondary caption mb-10">
                  ALREADY HAVE AN ACCOUNT?
                  <a>
                    <u
                      class="text--secondary"
                      @click="GoToLogin()"
                    >
                      SIGN IN!
                    </u>
                  </a>
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
    usernameError: null,
    multiLine: true,
    snackbar: false,
    notificationErrors: null,
    loginRules: [
      v => !!v || 'Login is required',
      v => (v || '').length >= 2 || `Minimal length of username is 2 symbols`
    ],
    emailRules: [
      v => /.+@.+\..+/.test(v) || v.length <= 0 || 'E-mail must be valid'
    ]
  }),
  computed: {
    RegTitle () {
      switch (this.step) {
        case 1:
          return 'Sign Up'
        case 2:
          return 'Sign Up'
        default:
          return 'Sign Up'
      }
    },
    repeatpasswordRules () {
      const rules = []
      rules.push(v => !!v || ' Repeat password is required')
      rules.push(v => (!!v && v) === this.password || 'Values do not match')
      return rules
    },
    passwordRules () {
      const rules = []
      rules.push(v => !!v || ' Password is required')
      return rules
    }
  },
  watch: {
    repeatpassword: 'validateField',
    password: 'validateField'
  },
  created () {
    console.log(this.$route.params.registercode)
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
      if (this.$refs.passwords) {
        this.$refs.passwords.validate();
      }
    },
    GoToLogin () {
      this.$root.$children[0].login = this.login
      this.$root.$children[0].name = this.name
      this.$root.$children[0].secondname = this.secondname
      this.$root.$children[0].email = this.email
      this.$router.push('/login/')
    },
    Register (username, password, repeatpassword, name, secondname, email) {
      let invitecode = this.$route.params.registercode
      console.log()
      if (username && password && password === repeatpassword) {
        api.axios
          .post('/api/accounts/register/', {
            username: username,
            password: password,
            first_name: name,
            last_name: secondname,
            email: email },
          { params: {
            invite_code: invitecode
          }
          })
          .catch(error => {
            if (error.response.status === 400) {
              this.notificationErrors = error.response.data[Object.keys(error.response.data)[0]].join(' ');
              this.snackbar = (error);
              Object.values(error.response.data).forEach(error => {
                if (error.length) {
                  this.usernameError = (error);
                  setTimeout(() => { this.usernameError = null }, 3000);
                }
              });
            }
          })
          .then(data => {
            if (data && data.status === 201) {
              this.$router.push('/verify/')
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
