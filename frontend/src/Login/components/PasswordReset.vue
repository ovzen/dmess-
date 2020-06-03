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
              style="background: linear-gradient(324.48deg, #EE9002 0%, #CE54FC 81.58%);"
            />
            <v-container>
              <v-toolbar-title class="text-center pt-7 text--secondary">
                Password Reset
              </v-toolbar-title>
              <div>
                <v-window>
                  <v-window-item>
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
                            label="Your new password"
                            hint="Password must contain letters and numbers"
                            required
                            outlined
                            name="password"
                            :rules="passwordRules"
                            @click:append="vanish = !vanish"
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
                            @keyup.enter="reset_password(password, repeatpassword)"
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
                    :disabled="password == '' || password != repeatpassword"
                    tile
                    outlined
                    color="purple darken-4"
                    class="mb-8"
                    @click="reset_password(password, repeatpassword)"
                  >
                    submit new password
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
            </v-container>
          </v-layout>
        </v-card>
      </v-col>
    </v-flex>
  </v-container>
</template>
    <template v-else>
      <v-container class="fill-height">
        <v-flex
          d-flex
          justify-center
        >
          <v-container class="pa-12">
            <p class="text-center display-2 font-weight-light">
              your email
            </p>
            <v-card-text class="text-center subtitle-1 text--secondary">
              You will need to verify your email to complete registration.
            </v-card-text>
            <v-container>
              <v-flex
                d-flex
                justify-center
              >
                <pre>
 __________________________________________________
|\                                                /|
| \                                              / |
|  \                                            /  |
|   \                                          /   |
|    \________________________________________/    |
|                                                  |
|                                                  |
|                                                  |
|                                                  |
|__________________________________________________|
            </pre>
              </v-flex>
            </v-container>
            <v-card-text class="text-center text--secondary subtitle-1 pa-5">
              A verification mail has been sent to <span class="font-weight-bold">vasya@yandex.ru</span> with a link to verify your account.<br>
              If you have not received the email after a few minutes, please check your spam folder.
            </v-card-text>
          </v-container>
        </v-flex>
      </v-container>
    </template>
  </v-container>
</template>

<script>
import api from '../api'
import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)
export default {
  name: 'PasswordReset',
  data: () => ({
    vanish: false,
    usernameError: null,
    multiLine: true,
    snackbar: false,
    notificationErrors: null,
    user_id: '',
    timestamp: '',
    signature: '',
    reset_mode: false,
    password: '',
    repeatpassword: ''
  }),
  computed: {
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
    if (Object.keys(this.$route.query).length !== 0) {
      this.reset_mode = true
    }
  },
  methods: {
    validateField () {
      if (this.$refs.passwords) {
        this.$refs.passwords.validate()
      }
    },
    reset_password (password, repeatpassword) {
      this.user_id = this.$route.query.user_id
      this.timestamp = this.$route.query.timestamp
      this.signature = this.$route.query.signature
      if (this.user_id && this.timestamp && this.signature && password == repeatpassword) {
        api.axios
          .post('/api/accounts/reset-password/', {
            password: password,
            user_id: this.user_id,
            timestamp: this.timestamp,
            signature: this.signature
          })
          .catch(error => {
            if (error.response.status === 400) {
              this.notificationErrors = error.response.data[Object.keys(error.response.data)[0]].join(' ')
              this.snackbar = (error)
              Object.values(error.response.data).forEach(error => {
                if (error.length) {
                  this.usernameError = (error)
                  setTimeout(() => { this.usernameError = null }, 3000)
                }
              })
            }
          })
          .then(data => {
            if (data && data.status === 200) {
              this.$router.push('/login/')
            }
          })
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: "Roboto", Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
