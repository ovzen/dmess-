<template>
  <v-app>
    <v-app-bar
      app
      height="80"
      color="background_white"
    >
      <!-- <v-app-bar-nav-icon @click="drawer = true" /> -->
      <v-toolbar-title v-if="Route.params.id">
          <v-list-item>
            <v-list-item-avatar>
              <v-img src="https://cdn.vuetifyjs.com/images/cards/girl.jpg"></v-img>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                class="title"
              >
                 {{ chatName }}
              </v-list-item-title>
              <v-list-item-subtitle>
                online/offline
              </v-list-item-subtitle>
            </v-list-item-content>

          </v-list-item>
      </v-toolbar-title>
      <v-spacer />
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon class="material-icons">collections_bookmark</v-icon>
      </v-btn>

      <v-menu
        offset-y
        min-width="128"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            icon
            v-on="on"
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list color="background_white">
          <v-list-item>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
          <v-list-item @click="goProfilePage()">
            <v-list-item-title>My profile</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>Button 3</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>Button 4</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :width="($vuetify.breakpoint.width * 0.20 > 600 ? 600 : $vuetify.breakpoint.width * 0.20)"
      app
      color="background_white"
      permanent
    >
      <v-card tile>
        <v-list
          color="basic"
          dark
          height="80"
          class="pt-1"
        >
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                v-if="(firstName || lastName)"
                class="title"
              >
                {{ firstName }} {{ lastName }}
              </v-list-item-title>
              <v-list-item-title
                v-else
                class="title"
              >
                {{ username }}
              </v-list-item-title>
              <v-list-item-subtitle
                v-if="isOnline"
              >
                online
              </v-list-item-subtitle>
              <v-list-item-subtitle
                v-else
              >
                offline
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-avatar
              v-if="avatar"
            >
              <v-img :src="avatar"></v-img>
            </v-list-item-avatar>
            <v-list-item-avatar
              v-else
              color="#FFFFFF"
              class="justify-center"
            >
              <span class="indigo--text">
                {{ firstName[0] }}{{ lastName[0] }}
              </span>
            </v-list-item-avatar>

          </v-list-item>
        </v-list>
      </v-card>

      <v-divider />
      <v-subheader>
        <a>
          <u>
            ALL CHATS
          </u>
        </a>
      </v-subheader>
      <v-divider />
      <v-list-item
        to="/ChatUser"
        active-class="background_pink"
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
            <!--<v-img
              src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
            />-->
          </v-avatar>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title style="color: #1F1E21">
            Name User
          </v-list-item-title>
          <v-list-item-subtitle class="black_second--text">
            Text Message
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-list-item-action-text>
            18:00
          </v-list-item-action-text>
          <v-avatar
            color="basic"
            class="subheading white--text"
            size="24"
            v-text="1"
          />
        </v-list-item-action>
      </v-list-item>
      <v-divider />
      <v-footer
        absolute
        padless
        style="height:54px"
      >
        <v-btn
          fab
          color="basic"
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

    <v-content class="background_main">
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>
    <SystemInfo style="position: fixed; bottom: 0px; text-align: right;" />
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
    firstName: undefined,
    lastName: undefined,
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
    $route: ['getDialogs', 'disconnect', 'getChatName']
  },
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  beforeCreate () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = this.$cookie.get('Authentication').user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  mounted () {
    setInterval(this.updateToken, 1000)
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
            this.chatName = response.data.results[0].name
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
          this.firstName = res.data['user'].first_name
          this.lastName = res.data['user'].last_name
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
