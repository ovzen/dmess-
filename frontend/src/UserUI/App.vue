<template>
  <v-app>
    <v-app-bar
      v-if="Route.name != 'Main'"
      app
      height="80"
      color="background_white"
    >
      <!-- <v-app-bar-nav-icon @click="drawer = true" /> -->
      <v-toolbar-title
        v-if="Route.params.id"
      >
        <v-list-item>
          <v-list-item-avatar>
            <v-img
              src="https://cdn.vuetifyjs.com/images/cards/girl.jpg"
            />
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
      <v-btn
        icon
        disabled
      >
        <v-icon>
          mdi-magnify
        </v-icon>
      </v-btn>
      <v-btn
        icon
      >
        <v-icon>
          mdi-book-multiple
        </v-icon>
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
            <v-icon>
              mdi-dots-vertical
            </v-icon>
          </v-btn>
        </template>

        <v-list
          color="background_white"
        >
          <v-list-item>
            <v-list-item-title>
              Logout
            </v-list-item-title>
          </v-list-item>
          <v-list-item
            @click="goProfilePage()"
          >
            <v-list-item-title>
              Button 2
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              Button 3
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              Button 4
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :width="($vuetify.breakpoint.width * 0.225 > 600 ? 600 : $vuetify.breakpoint.width * 0.225)"
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
              <v-img
                :src="avatar"
              />
            </v-list-item-avatar>
            <v-list-item-avatar
              v-else
              color="#FFFFFF"
              class="justify-center indigo--text"
            >
              <span v-if="(firstName && lastName)">
                {{ firstName[0].toUpperCase() }}{{ lastName[0].toUpperCase() }}
              </span>
              <span v-else-if="(firstName)">
                {{ firstName[0].toUpperCase() }}
              </span>
              <span v-else-if="(lastName)">
                {{ lastName[0].toUpperCase() }}
              </span>
              <span v-else>
                {{ username[0].toUpperCase() }}
              </span>
            </v-list-item-avatar>
          </v-list-item>
        </v-list>
      </v-card>

      <v-divider />
      <div
        id="dynamic-component"
      >
        <profiles
          v-if="currentTab.name == 'mdi-account-circle'"
        />
        <div v-if="currentTab.name == 'mdi-message-text'">
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
            v-for="(dialog, i) in dialogs"
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
                {{ getContactName(dialog.users_detail) }}
              </v-list-item-title>
              <v-list-item-subtitle v-if="dialog.last_message">
                <span
                  style="color:#757575; font-size:115%;"
                >
                  {{ dialog.last_message.text }}
                </span>
              </v-list-item-subtitle>
              <v-list-item-subtitle v-else>
                <span
                  style="color:#757575; font-size:115%;"
                >
                  Тут пока ничего не написано
                </span>
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-list-item-action-text v-if="dialog.last_message">
                {{ formatTime(dialog.last_message.create_date) }}
              </v-list-item-action-text>
              <!-- Изменить v-if на другое условие: "если есть непрочитанные сообщения" -->
              <v-avatar
                v-if="dialog.last_message"
                color="basic"
                class="subheading white--text"
                size="24"
                v-text="1"
              />
            </v-list-item-action>
          </v-list-item>
        </div>
        <settings
          v-if="currentTab.name == 'mdi-settings'"
        />
        <v-divider />
        <v-footer
          absolute
          padless
          style="height:54px; background :#ffffff;"
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
              v-for="tab in tabs"
              :key="tab.name"
              icon
              :class="['tab-button', { active: currentTab.name === tab.name }]"
              @click="currentTab = tab"
            >
              <v-icon
                size="24px"
              >
                {{ tab.name }}
              </v-icon>
            </v-btn>
          </v-card-actions>
        </v-footer>
      </div>
    </v-navigation-drawer>

    <v-content
      class="background_main"
    >
      <v-container fluid>
        <router-view />
      </v-container>
    </v-content>
    <SystemInfo
      style="position: fixed; bottom: 0px; text-align: right;"
    />
  </v-app>
</template>

<script>
import Vue from 'vue'
import VueCookie from 'vue-cookie'
import api from './api'
import jwt from 'jsonwebtoken'
import SystemInfo from './components/SystemInfo'
import profiles from './components/profiles'
import settings from './components/settings'
import moment from 'moment'

Vue.use(VueCookie)
var tabs = [
  {
    name: 'mdi-account-circle',
    component: {
    }
  },
  {
    name: 'mdi-message-text',
    component: {
    }
  },
  {
    name: 'mdi-room-service',
    component: {
    }
  },
  {
    name: 'mdi-settings',
    component: {
    }
  }
]

export default {
  new: '#dynamic-component',
  components: { SystemInfo, profiles, settings },
  data: () => ({
    login: '',
    button: 'Войти',
    chatName: '',
    password: '',
    data: '',
    id: 0,
    drawer: true,
    alwaysOnDisplay: false,
    expandOnHover: false,
    group: [],
    for_user: true,
    username: 'Test',
    firstName: undefined,
    lastName: undefined,
    user_id: undefined,
    avatar: '',
    isOnline: false,
    currentTab: tabs[0],
    tabs: tabs,
    dialogs: []
  }),
  computed: {
    Route () {
      return this.$route
    }
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['disconnect', 'getChatName']
  },
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  mounted () {
    setInterval(this.updateToken, 1000)
    this.getDialogsList()
    this.getUserData(this.user_id)
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
    getDialogsList () {
      api.axios
        .get('/api/dialog/', { params: { users: this.user_id } })
        .then(response => {
          this.dialogs = response.data.results
          console.log('dialogsList:', response.data.results)
        })
    },
    openDialog (dialogId) {
      console.log('Route ID:', this.$route.params.id)
      if (this.$route.params.id !== dialogId) {
        this.$router.push({ name: 'ChatUser', params: { id: dialogId } })
      }
    },
    allusers () {
      this.$router.push({ name: 'allUser' })
    },
    goProfilePage () {
      this.$router.push({ name: 'Profile', params: { id: this.user_id } })
    },
    getChatName () {
      if (this.$route.name === 'ChatUser') {
        api.axios
          .get('/api/dialog/', {
            params: {
              id: this.$route.params.id
            }
          })
          .then(response => {
            this.chatName = response.data.results[0].name
            console.log(response)
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
    },
    formatTime (datetime) {
      if (datetime) {
        if (moment(datetime).isBefore(moment(), 'day')) {
          return moment(String(datetime)).format('DD.MM.YYYY')
        } else {
          return moment(String(datetime)).format('hh:mm')
        }
      }
    },
    getUserName (user) {
      if (user.first_name && user.last_name) {
        return (user.first_name + ' ' + user.last_name)
      } else if (user.first_name) {
        return user.first_name
      } else if (user.last_name) {
        return user.last_name
      } else {
        return user.username
      }
    },
    getContact (users) {
      return (users[0].id === this.user_id) ? users[1] : users[0]
    },
    getContactName (users) {
      console.log(users)
      if (users.length > 1) {
        return this.getUserName(this.getContact(users))
      } else {
        return 'В диалоге нет других пользователей'
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  color: #2c3e50;
  height: 100vh;
  .active {
  color: #6202EE
}
}
</style>
