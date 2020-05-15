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
              Name User
            </v-list-item-title>
            <v-list-item-subtitle>
              online/offline
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-toolbar-title>
      <v-spacer />

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
          <v-list-item
            :to="{ name: 'MyProfile', params: {} }"
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
                    NU
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
                    {{ ( contact.Contact.profile.is_online == true ? 'В сети' : 'Не в сети' ) }}
                  </span>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider
              v-if="contact.id != SortContacts[SortContacts.length-1].id"
              inset
            />
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
                      NU
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
                      {{ ( user.is_online == true ? 'В сети' : 'Не в сети' ) }}
                    </span>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-divider
                v-if="user.id !== findedUsers[findedUsers.length-1].id"
                inset
              />
            </div>
          </div>
        </div>
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
        <v-divider />
        <settings
          v-if="currentTab.name == 'mdi-settings'"
        />
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
            @click.stop="dialog = true"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-dialog
            v-model="dialog"
            max-width="290"
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
                  color="green darken-1"
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
                <span>
                  {{ tab.display_name }}
                </span>
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
import profiles from './components/profiles'
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
    display_name: 'dialogs',
    component: {
    }
  },
  {
    name: 'mdi-room-service',
    display_name: 'Notifications',
    component: {
    }
  },
  {
    name: 'mdi-settings',
    display_name: 'Settings',
    component: {
    }
  }
]

export default {
  new: '#dynamic-component',
  components: { SystemInfo, settings },
  data: () => ({
    login: '',
    button: 'Войти',
    chatName: '',
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
    currentTab: tabs[0],
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
    this.getContacts()
    this.getDialogsList()
    this.getUserData()
    setInterval(this.getUnreadMessagesQty, 2000)
    this.username = jwt.decode(this.$cookie.get('Authentication')).name
    if (this.Route.params.id) {
      this.getChatName()
    }
  },
  methods: {
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
            console.log('dialogsList:', response.data.results)
          }
        })
        .catch(error => console.log(error))
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
            if (response.data) {
              this.chatName = response.data.results[0].name
              console.log(response)
            }
          })
          .catch(error => console.log(error))
      } else {
        this.chatName = undefined
      }
    },
    getUserData () {
      api.axios
        .get('/api/users/' + this.user_id + '/')
        .then(res => {
          if (res.data) {
            console.log('user details: ', res)
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
      console.log(users)
      if (users.length > 1) {
        return this.getUserName(this.getContact(users))
      } else {
        return 'В диалоге нет других пользователей'
      }
    },
    getUnreadMessagesQty () {
      api.axios
        .get('/api/dialogs')
        .then(res => {
          if (res.data) {
            this.unread_messages_qty = res.data['unread_messages']
          }
        })
        .catch(error => console.log(error))
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
