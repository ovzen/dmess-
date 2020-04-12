<template>
  <v-app>
    <v-app-bar
      app
      :value="!(alwaysOnDisplay || expandOnHover)"
      collapse-on-scroll
      dark
      scroll-target="#scrolling-techniques-6"
    >
      <!-- <v-app-bar-nav-icon @click="drawer = true" /> -->
      <v-toolbar-title v-if="Route.params.id">
        {{ chatName }}
      </v-toolbar-title>
      <v-spacer />
      <v-btn
        class="ma-2"
        outlined
        color="#90CAF9"
        @click="goProfilePage()"
      >
        {{ username }}
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :width="$vuetify.breakpoint.width * 0.25"
      app
      permanent
    >
      <v-card tile>
        <v-list
          color="#6202EE"
          dark
          height=80
          class="pt-1"
        >
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="title">{{ username }}</v-list-item-title>
              <v-list-item-subtitle v-if="isOnline">online</v-list-item-subtitle>
              <v-list-item-subtitle v-else>offline</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar>
              <v-img :src="avatar"></v-img>
            </v-list-item-avatar>
          </v-list-item>
        </v-list>
      </v-card>

      <v-divider></v-divider>
      <v-list>
        Тут будет наполнение сайдбара
      </v-list>

      <v-divider></v-divider>
      <v-footer
        absolute
        padless
      >
        <v-btn
          fab
          color="#6202EE"
          dark
          top
          right
          absolute
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-card-actions>
          <v-btn
            v-for="icon in iconsFooter"
            :key="icon"
            icon
          >
            <v-icon size="24px">
              {{ icon }}
            </v-icon>
          </v-btn>
        </v-card-actions>
      </v-footer>
    </v-navigation-drawer>

    <v-sheet
      id="scrolling-techniques-6"
      class="overflow-y-auto"
      max-height="100vh"
    >
      <v-content>
        <router-view />
        <SystemInfo style="position: fixed; bottom: 0px; text-align: right;" />
      </v-content>
    </v-sheet>
  </v-app>
</template>

<script>
import Vue from 'vue'
import VueCookie from 'vue-cookie'
import api from './api'
import jwt from 'jsonwebtoken'
import SystemInfo from './components/SystemInfo'
Vue.use(VueCookie)
export default {
  name: 'App',
  components: { SystemInfo },
  data: () => ({
    login: '',
    button: 'Войти',
    chatName: '',
    password: '',
    message_text: '',
    data: '',
    messages: [],
    dialog: false,
    id: 0,
    drawer: true,
    alwaysOnDisplay: false,
    expandOnHover: false,
    group: [],
    for_user: true,
    dialogs_for_user: [],
    username: 'Test',
    user_id: undefined,
    avatar: '',
    isOnline: false,
    iconsFooter: [
      'mdi-account-circle',
      'mdi-message-text',
      'mdi-room-service',
      'mdi-settings'
    ]
  }),
  computed: {
    Route () {
      return this.$route
    }
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['updateToken', 'getDialogs', 'disconnect', 'getChatName']
  },
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  mounted () {
    this.getDialogs()
    this.getUserData()
    this.username = jwt.decode(this.$cookie.get('Authentication')).name
    if (this.Route.params.id) {
      this.getChatName()
    }
  },
  methods: {
    disconnect () {
      this.$disconnect()
    },
    updateToken () {
      if (localStorage.getItem('UpdateKey') && !this.$cookie.get('Authentication')) {
        api.axios.post('/api/token/refresh/', { refresh: localStorage.getItem('UpdateKey') }).then(res => {
          this.$cookie.set('Authentication', res.data.access, {
            expires: '5m'
          })
        }
        )
      }
    },
    getDialogs () {
      api.axios.get('/api/dialog/', {
        params: {
          users: this.user_id
        }
      })
        .then(res => {
          this.dialogs_for_user = res.data
          console.log(this.dialogs_for_user)
        })
    },
    openDialog (dialogId) {
      this.$router.push({ name: 'Chat', params: { id: dialogId } })
    },
    allusers () {
      this.$router.push({ name: 'allUser' })
    },
    goProfilePage () {
      this.$router.push({ name: 'Profile', params: { id: this.user_id } })
    },
    getChatName () {
      if (this.$route.name === 'Chat') {
        api.axios
          .get('/api/dialog/', {
            params: {
              id: this.$route.params.id
            }
          })
          .then(response => {
            this.chatName = response.data[0].name
          })
      } else {
        this.chatName = undefined
      }
    },
    getUserData () {
      api.axios
        .get('/api/users/' + this.user_id)
        .then(res => {
          this.avatar = res.data['avatar']
          this.isOnline = res.data.is_online
        })
    }
  }
}
</script>

<style lang="scss">
#app {
  color: #2c3e50;
  height: 100vh;
}
</style>
