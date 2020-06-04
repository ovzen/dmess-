<template>
  <v-app>
    <v-content class="background_main">
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
import Vue from 'vue'
import VueCookie from 'vue-cookie'
import api from './api'
Vue.use(VueCookie)
export default {
  name: 'Auth',
  data: () => ({
    login: '',
    name: '',
    secondname: '',
    email: ''
  }),
  created () {
    if (localStorage.getItem('UpdateKey')) {
      api.axios.post('/api/token/refresh/', { refresh: localStorage.getItem('UpdateKey') }).then(res => {
        this.$cookie.set('Authentication', res.data.access, {
          expires: '5m'
        })
        window.location.href = 'http://' + window.location.host + this.$route.query.next
      }
      )
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
