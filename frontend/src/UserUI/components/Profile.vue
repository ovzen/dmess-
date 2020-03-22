<template>
  <v-container fluid>
    <v-card
      class="mx-auto"
      max-width="500"
    >
      <v-list-item>
        <v-list-item-content>
          <div class="overline mb-4">
            Профиль пользователя
          </div>
          <v-list-item-title class="headline mb-1 indigo--text">
            Имя пользователя: {{ username }}
          </v-list-item-title>
          <v-list-item-subtitle>User ID: {{ id }}</v-list-item-subtitle>
          <v-list-item-subtitle>Статус пользователя: {{ status }}</v-list-item-subtitle>
          <!-- <v-list-item-subtitle>Дата регистрации: {{ createdDate }}</v-list-item-subtitle> -->
        </v-list-item-content>

        <v-list-item-avatar
          size="120"

        >
          <v-img :src="avatar"></v-img>
        </v-list-item-avatar>
      </v-list-item>
    </v-card>
  </v-container>
</template>

<script>
import api from '../api'

export default {
  name: 'Profile',
  data: () => ({
    id: '',
    username: '',
    avatar: '',
    status: '',
    createdDate: '',
    message: ''

  }),

  methods: {
    get_data () {
      api.axios
        .get('/api/users/2')
        .then(res => {
          this.id = res.data['user'].id
          this.username = res.data['user'].username
          this.avatar = res.data['avatar']
          this.status = res.data.bio
        })
        .catch(error => {
          if (error.response.status === 401) {
            this.message = 'Ошибка авторизации'
          }
        })
    }
  },

  created () {
    this.get_data()
  }

}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
