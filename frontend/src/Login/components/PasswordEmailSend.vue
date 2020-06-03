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
                Password retrieval
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
                            ref="LoginPassword"
                            v-model="repeatpassword"
                            :error-messages="usernameError"
                            clearable
                            hint="Login specified during registration"
                            label="Login for reset"
                            required
                            outlined
                            name="LoginPassword"
                            @keyup.enter="send_reset_password_link(login)"
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
                    style="margin-top:-40px"
                    :disabled="password == '' || password != repeatpassword"
                    tile
                    outlined
                    color="purple darken-4"
                    class="mb-8"
                    @click="send_reset_password_link(login)"
                  >
                    Send an email
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
              <v-card-actions
                class="text-center"
                style="margin-bottom:-60px;margin-top:-30px"
              >
                <v-card-text class="text--secondary caption mb-10">
                  ALREADY HAVE AN ACCOUNT?
                  <router-link to="/login/">
                    <u
                      class="text--secondary"
                    >
                      SIGN IN!
                    </u>
                  </router-link>
                  <v-card-text>
                    <router-link to="/register/">
                      <u
                        class="text--secondary"
                        style="font-style: normal; font-family: Roboto;"
                      >
                        SIGN UP!
                      </u>
                    </router-link>
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
import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)
export default {
  name: 'Login',
  data: () => ({
    login: ''
  }),
  methods: {
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
