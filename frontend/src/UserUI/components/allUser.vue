<template>
  <v-app>
    <v-layout row>
      <v-flex
        xs12
        sm6
        offset-sm3
      >
        <h1 class="text--secondary mb-3">
          Список пользователей
        </h1>
        <v-list-item
            v-for="user in Users"
            :key="user"
            class="grow"
          >
          <v-card>
              <v-layout rodtnw>
                <v-flex
                  xs4
                >
                Пользователь: {{ user.username }}
                </v-flex>
                <v-flex xs8>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="info">
                      Открыть
                    </v-btn>
                  </v-card-actions>
                </v-flex>
              </v-layout>
          </v-card>
        </v-list-item>
      </v-flex>
    </v-layout>
  </v-app>
</template>

<script>
import Vue from 'vue'
import VueCookie from 'vue-cookie'
import api from '../api'
Vue.use(VueCookie)
export default {
  name: 'App',
  data: () => ({
    Users: [],
    userslist: true,
    usersDialogId: ''
  }),
  mounted () {
    this.getUsers()
  },
  methods: {
    getUsers (dialogid) {
      api.axios.get('/api/dialog/', {
        params: {
          userslist: this.userslist
        }
      })
        .then(res => {
          this.Users = res.data['users']
          console.log(this.Users)
        })
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
