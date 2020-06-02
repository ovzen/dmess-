<template>
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
          You will need to verify your email to complete registration
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
          An email has been sent to <strong> user_email@abc.com</strong> with a link to verify your account.<br>
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
  name: 'Verification',
  data: () => ({
    user_id: '',
    timestamp: '',
    signature: ''
  }),
  created () {
    if (Object.keys(this.$route.query).length) {
      this.verify()
    }
  },
  methods: {
    verify () {
      this.user_id = this.$route.query.user_id
      this.timestamp = this.$route.query.timestamp
      this.signature = this.$route.query.signature
      api.axios
        .post('/api/accounts/verify-registration/', {
          user_id: this.user_id,
          timestamp: this.timestamp,
          signature: this.signature
        })
        .catch(error => {
          console.log(error)
        })
        .then(data => {
          console.log(data.status)
          if (data && data.status === 200) {
            this.$router.push('/login/')
          }
        })
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
