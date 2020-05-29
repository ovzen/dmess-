<template>
  <v-app>
    <v-app-bar
      v-if="Route.name != 'Main'"
      app
      height="80"
      color="background_white"
    >
      <v-toolbar-title
        v-if="Route.name === 'MyProfile'"
        @click="GoBack()"
      >
        <v-btn
          text
          small
          style="font-family: Roboto;
                font-style: normal;
                font-weight: 500;
                font-size: 10px;
                line-height: 16px;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                color: #757575;"
        >
          <v-icon> mdi-keyboard-backspace </v-icon>
          Back
        </v-btn>
      </v-toolbar-title>
      <!-- <v-app-bar-nav-icon @click="drawer = true" /> -->
      <v-toolbar-title
        v-if="Route.name === 'ChatUser'"
      >
        <v-list-item>
          <v-list-item-avatar v-if="ChatInfo.profile.avatar">
            <v-img
              :src="ChatInfo.profile.avatar"
            />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="title"
            >
              {{ ChatInfo.username }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ ChatInfo.profile.status }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-toolbar-title>
      <v-spacer />

      <v-menu
        v-if="Route.name === 'ChatUser'"
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
          <v-list-item
            to="/"
          >
            <v-list-item-title>
              Collapse chat
            </v-list-item-title>
          </v-list-item>
          <v-list-item
            :to="{ name: 'MyProfile'}"
          >
            <v-list-item-title>
              Profile
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      style=""
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
            <router-link
              to="/MyProfile"
            >
              <v-list-item-avatar v-if="avatar">
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
            </router-link>
          </v-list-item>
        </v-list>
      </v-card>

      <v-divider />
      <div
        id="dynamic-component"
      >
        <div v-if="currentTab.name == 'mdi-account-circle'">
          <v-divider />
          <v-col>
            <v-text-field
              v-model="userSearch"
              clearable
              solo
              background-color="grey lighten-2"
              dense
              flat
              color="basic"
              hide-details
              prepend-inner-icon="mdi-magnify"
              label="Search for users"
              style="border-radius:50px; max-width:450px;"
              @input="getUsersBySearch(userSearch)"
            />
          </v-col>
          <v-divider />
          <div
            v-if="contacts.length"
          >
            <div
              v-for="contact in (userSearch != '' ? SortContacts : contacts)"
              :key="contact.id"
            >
              <v-list-item
                :to="'/UserProfile/' + contact.Contact.id"
              >
                <v-list-item-avatar>
                  <v-avatar
                    size="36px"
                    color="basic"
                  >
                    <span
                      class="white--text"
                    >
                      {{ getUserAvatar(contact.Contact) }}
                    </span>
                  <!--<v-img
              src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
            />-->
                  </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ contact.Contact.username }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    <span
                      class="basic--text text--lighten"
                    >
                      {{ contact.Contact.profile.status }}
                    </span>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-divider
                inset
              />
            </div>
          </div>
          <div
            v-if="!userSearch && !contacts.length"
            class="d-flex flex-column justify-center align-center fill-height"
            style="height:75vh"
          >
            <div class="mt-12">
              <p class="display-2 text-center grey--text">
                ʕつ •ᴥ• ʔつ
              </p>
              <p class="overline text-center font-weight-medium text_second--text">
                ADD NEW CONTACTS!
                <br />
                THEY WILL BE DISPLAY HERE
              </p>
            </div>
          </div>
          <div
            v-if="userSearch"
          >
            <v-divider />
            <h1
              class="basic--text"
              style="font-family: Roboto;
                    font-style: normal;
                    font-weight: 500;
                    font-size: 16px;
                    line-height: 16px;
                    padding:16px"
            >
              Global Search
            </h1>
            <v-divider />
            <div
              v-if="findedUsers.length"
            >
              <div
                v-for="user in findedUsers"
                :key="user.id"
              >
                <v-list-item
                  :to="'/UserProfile/' + user.id"
                >
                  <v-list-item-avatar>
                    <v-avatar
                      size="36px"
                      color="basic"
                    >
                      <span
                        class="white--text"
                      >
                        {{ getUserAvatar(user) }}
                      </span>
                    </v-avatar>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ user.username }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      <span
                        class="basic--text text--lighten"
                      >
                        {{ user.status }}
                      </span>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider
                  inset
                />
              </div>
            </div>
            <div
              v-else
              class="d-flex flex-column justify-center align-center fill-height"
              style="height:69vh"
            >
              <div>
                <p class="display-2 text-center grey--text">
                  ( ͡° ʖ̯ ͡°)
                </p>
                <p class="overline text-center font-weight-medium text_second--text">
                  NO RESULTS
                </p>
              </div>
            </div>
          </div>
        </div>
        <div
          v-if="currentTab.name == 'mdi-message-text'"
        >
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
          <div
            v-if="dialogs.length"
          >
            <div
              v-for="(dialog, i) in dialogs"
              :key="i"
            >
              <v-list-item
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
                  <v-list-item-subtitle style="min-width:10px;min-height:18.67px;">
                    <span
                      style="color:#757575; font-size:115%;"
                    >
                      {{ (dialog.last_message ? dialog.last_message.text : '') }}
                    </span>
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-list-item-action-text v-if="dialog.last_message">
                    {{ formatTime(dialog.last_message.create_date) }}
                  </v-list-item-action-text>
                  <v-avatar
                    v-if="unread_messages_qty[i]"
                    color="basic"
                    class="subheading white--text"
                    size="24"
                    v-text="unread_messages_qty[i]"
                  />
                </v-list-item-action>
              </v-list-item>
              <v-divider
                inset
              />
            </div>
          </div>
          <div
            v-else
            class="d-flex flex-column justify-center align-center fill-height"
            style="height:75vh"
          >
            <div class="mt-12">
              <p class="display-2 text-center grey--text">
                ( つ ^‿^ )つ
              </p>
              <p class="overline text-center font-weight-medium text_second--text">
                START MESSAGING WITH SOMEONE
                <br />
                CHAT WILL BE DISPLAY HERE
              </p>
            </div>
          </div>
        </div>
        <settings
          v-if="currentTab.name == 'mdi-settings'"
        />
        <v-footer
          absolute
          padless
          style="height:56px; background :#ffffff;box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2), 0px 2px 2px rgba(0, 0, 0, 0.12), 0px 0px 2px rgba(0, 0, 0, 0.14);"
        >
          <v-btn
            fab
            color="basic"
            dark
            top
            right
            absolute
            @click.stop="dialog = true"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-dialog
            v-model="dialog"
            max-width="700"
          >
            <v-card>
              <v-card-title
                class="headline"
              >
                We're so sorry, but we haven't kept up to develop this feature.
              </v-card-title>

              <v-card-text>
                This button seems to us so beautiful and cute that we could not just remove it :)
              </v-card-text>

              <v-card-actions>
                <v-spacer />

                <v-btn
                  color="basic"
                  text
                  @click="dialog = false"
                >
                  Okay, I agree with you
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-card-actions>
            <v-btn
              v-for="tab in tabs"
              :key="tab.name"
              icon
              :class="['tab-button', { active: currentTab.name === tab.name }]"
              @click="currentTab = tab"
            >
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <v-icon
                    size="24px"
                    v-on="on"
                  >
                    {{ tab.name }}
                  </v-icon>
                </template>
                <span>{{ tab.display_name }}</span>
              </v-tooltip>
            </v-btn>
          </v-card-actions>
        </v-footer>
      </div>
    </v-navigation-drawer>

    <v-content
      class="background_main"
    >
      <router-view />
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
import settings from './components/settings'
import moment from 'moment'

Vue.use(VueCookie)
var tabs = [
  {
    name: 'mdi-account-circle',
    display_name: 'Contacts',
    component: {
    }
  },
  {
    name: 'mdi-message-text',
    display_name: 'Dialogs',
    component: {
    }
  },
  /*
 {
    name: 'mdi-room-service',
    display_name: 'Notifications',
    component: {
    }
  },
  */
  {
    name: 'mdi-settings',
    display_name: 'Settings',
    component: {
    }
  }
]
let ws = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/dialog_notifications/')
export default {
  new: '#dynamic-component',
  components: { SystemInfo, settings },
  data: () => ({
    login: '',
    button: 'Войти',
    ChatInfo: { username: 'Загрузка...', profile: { avatar: null, status: 'Загрузка...' } },
    password: '',
    data: '',
    userSearch: '',
    messages: [],
    dialog: false,
    id: 0,
    drawer: true,
    alwaysOnDisplay: false,
    expandOnHover: false,
    group: [],
    for_user: true,
    unread_messages_qty: [],
    username: 'Test',
    firstName: undefined,
    lastName: undefined,
    user_id: undefined,
    avatar: '',
    isOnline: false,
    currentTab: tabs[1],
    tabs: tabs,
    contacts: [],
    findedUsers: [],
    dialogs: []
  }),
  computed: {
    Route () {
      return this.$route
    },
    SortContacts () {
      return this.contacts.filter(contact => { return contact.Contact.username.toLowerCase().indexOf(this.userSearch.toLowerCase()) > -1 })
    }
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['disconnect', 'getChatInfo']
  },
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  mounted () {
    let Vue = this
    ws.onmessage = function (event) {
      let newDialog = JSON.parse(event.data).data
      for (let dialog in Vue.dialogs) {
        if (Vue.dialogs[dialog].id === newDialog.id) {
          Vue.dialogs[dialog] = newDialog
          console.log(newDialog)
          Vue.$forceUpdate()
        }
      }
    }
    document.addEventListener('keydown', function (event) {
      const key = event.key // Or const {key} = event; in ES6+
      if (key === 'Escape' && Vue.Route.fullPath !== '/') {
        Vue.$router.push('/')
      }
    })
    setInterval(this.updateToken, 1000)
    this.getContacts()
    this.getDialogsList()
    this.getUserData()
    this.username = jwt.decode(this.$cookie.get('Authentication')).name
    if (this.$route.name === 'ChatUser') {
      this.getChatInfo()
    }
  },
  methods: {
    GetUnreadMessages (dialog) {
      console.log(dialog.unread_messages[dialog.users[1]])
      if (typeof this.user_id !== 'undefined') {
        if (dialog.users[0] === this.user_id) {
          return dialog.unread_messages[dialog.users[0]]
        }
        return dialog.unread_messages[dialog.users[1]]
      }
      return ''
    },
    GoBack () {
      this.$router.go(-1)
    },
    getUserAvatar (UserProfile) {
      if (typeof UserProfile !== 'undefined') {
        if (UserProfile.first_name !== '' && UserProfile.last_name !== '') {
          return (UserProfile.first_name[0] + UserProfile.last_name[0]).toUpperCase()
        } else {
          return UserProfile.username[0].toUpperCase()
        }
      } return ''
    },
    getUsersBySearch () {
      api.axios.get('/api/users/', {
        params: {
          search: this.userSearch
        }
      }).then(res => {
        this.findedUsers = res.data.results.filter(user => {
          for (let contact in this.contacts) {
            if (user.username === this.contacts[contact].Contact.username) {
              return false
            }
          }
          return true
        })
      })
    },
    getContacts () {
      api.axios.get('/api/contacts/').then(res => { this.contacts = res.data.results })
    },
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
          if (response.data) {
            this.dialogs = response.data.results
          }
        })
        .catch(error => console.log(error))
    },
    openDialog (dialogId) {
      // console.log('Route ID:', this.$route.params.id)
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
    getChatInfo () {
      if (this.$route.name === 'ChatUser') {
        api.axios
          .get('/api/dialog/' + this.$route.params.id + '/')
          .then(response => {
            if (response.status === 200) {
              if (response.data.users_detail[0].username === this.username && typeof response.data.users_detail[1] !== 'undefined') {
                this.ChatInfo = response.data.users_detail[1]
              } else {
                if (response.data.users_detail[0].username !== this.username) {
                  this.ChatInfo = response.data.users_detail[0]
                } else {
                  this.ChatInfo = { username: 'Произошла ошибка', profile: { avatar: null, status: '' } }
                }
              }
            }
          })
          .catch(error => console.log(error))
      }
    },
    getUserData () {
      api.axios
        .get('/api/users/' + this.user_id + '/')
        .then(res => {
          if (res.data) {
            // console.log('user details: ', res)
            this.avatar = res.data.profile.avatar
            this.isOnline = res.data.profile.is_online
            this.firstName = res.data.first_name ? res.data.first_name : undefined
            this.lastName = res.data.last_name ? res.data.last_name : undefined
          }
        })
        .catch(error => console.log(error))
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
      // console.log(users)
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
