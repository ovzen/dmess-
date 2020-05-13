<template>
  <div>
    <v-divider />
    <v-col>
      <v-text-field
        clearable
        solo
        color="basic"
        background-color="grey lighten-2"
        dense
        flat
        hide-details
        prepend-inner-icon="mdi-magnify"
        label="Search for dialogs"
        style="border-radius:50px; max-width:450px;"
      />
    </v-col>
    <v-divider />
    <v-list-item
      v-for="(dialog, i) in dialogsForUser"
      :key="i"
      @click="openDialog(dialog.id)"
    >
      <v-list-item-avatar>
        <v-avatar
          size="36px"
          color="basic"
        >
          <span
            class="white--text"
          >
            NU
          </span>
        </v-avatar>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
          Имя пользователя
        </v-list-item-title>
        <v-list-item-subtitle>
          <span
            style="color:#757575; font-size:115%;"
          >
            {{ dialog.last_message.text }}
          </span>
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-action>
        <v-list-item-action-text>
          {{ dialog.last_message.created_date }}
        </v-list-item-action-text>
        <v-avatar
          color="basic"
          class="subheading white--text"
          size="24"
          v-text="1"
        />
      </v-list-item-action>
    </v-list-item>
  </div>
</template>

<script>
import Vue from 'vue'
import VueCookie from 'vue-cookie'
import api from '../api'
import jwt from 'jsonwebtoken'
Vue.use(VueCookie)

export default {
  name: 'Chats',
  data: () => ({
    dialogsForUser: [],
    user_id: undefined
  }),
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['getDialogs']
  },
  mounted () {
    this.getDialogs()
    this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
  },
  methods: {
    getDialogs () {
      api.axios
        .get('/api/dialog/', {
          params: {
            users: this.user_id
          }
        })
        .then(response => {
          this.dialogsForUser = response.data.results
          console.log('response:', response)
          console.log(this.dialogsForUser)
        })
    },
    openDialog (dialogId) {
      this.$router.push({ name: 'ChatUser', params: { id: dialogId } })
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
