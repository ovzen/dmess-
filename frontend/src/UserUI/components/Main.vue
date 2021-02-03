<template>
  <v-container
    fluid
  >
    <div class="main">
      <h1 class="main_smile smile_color--text">
        ¯\_(^ ‿ ^)\
      </h1>
      <span class="main_smile_text smile_color--text">
        select a dialog to start messaging
      </span>
    </div>
  </v-container>
</template>

<script>
import jwt from 'jsonwebtoken'
import VueCookie from 'vue-cookie'
import Vue from 'vue'
Vue.use(VueCookie)
export default {
  name: 'Main',
  data: () => ({
    login: '',
    ChatName: null,
    button: 'Войти',
    password: '',
    message_text: '',
    data: '',
    user_id: undefined
  }),
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  }
}
</script>
<style lang="scss">
.main {
  margin:auto;
  position: fixed;
  top:44%;
  left:50%;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
}
.main_smile {
  margin-bottom: 32px;
  margin-left: -36px;
  font-style: normal;
  font-weight: 300;
  font-size: 96px;
  line-height: 112px;
  /* identical to box height */
  letter-spacing: -1.5px;
}
.main_smile_text {
  margin-top: 32px;
  font-style: normal;
  font-weight: 500;
  font-size: 14px;
  line-height: 16px;
  letter-spacing: 0.75px;
  text-transform: uppercase;
}
</style>
