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
            <v-img src="/static/log.JPG" />
            <v-container>
              <v-toolbar-title class="text-center pt-7 text--secondary">
                Final step
              </v-toolbar-title>
              <v-card-actions>
                <v-row justify="space-around">
                  <v-card-text class="">
                    Check your e-mail inbox and verify your account!
                  </v-card-text>
                </v-row>
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
  name: 'Verification',
  data: () => ({
    user_id: '',
    timestamp: '',
    signature: '',
  }),
  created () {
    if (Object.keys(this.$route.query).length) this.verify()

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
          signature: this.signature})
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
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
