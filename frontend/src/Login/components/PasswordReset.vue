<template v-if="this.login_required === true">
  <v-container class="fill-height">
    <v-flex
      d-flex
      justify-center
    >
      <v-container class="pa-12">
        <p>To be continued...</p>
      </v-container>
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
          Verify your email
        </p>
        <v-card-text class="text-center">
          You will need to verify your email to reset your password
        </v-card-text>
        <v-container>
          <v-flex
            d-flex
            justify-center
          >
            <pre>
___________________________________________________
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
        <v-card-text class="text-center pa-12">
          An email has been sent to <strong> user_email@abc.com</strong> with a link to reset your account password.<br>
          If you have not received the mail after a few minutes, please check your spam folder.
        </v-card-text>
      </v-container>
    </v-flex>
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
    user_id: '',
    timestamp: '',
    signature: '',
    login_required: true,
    boole: true
  }),
  created () {
    console.log(Object.keys(this.$route.query).length === 0)
    if (Object.keys(this.$route.query).length === 0) {
      this.send_reset_password_link()
    } else {
      this.login_required = false
      this.reset_password()
    }
  },
  methods: {
    send_reset_password_link () {
      // api query on api/account/send-reset-password-link/
    },
    reset_password () {
      // api query on api/account/reset-password/
      this.login_required = false
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
