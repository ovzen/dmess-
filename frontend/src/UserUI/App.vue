<template>
  <v-app>
    <v-app-bar
      v-if="Route.name != 'Main'"
      app
      height="80"
      color="background_white"
    >
      <v-toolbar-title
        v-if="Route.name === 'MyProfile' || Route.name === 'UserProfile'"
        @click="GoBack()"
      >
        <v-btn
          text
          small
          class="back_button--text"
          style="font-family: Roboto;
                font-style: normal;
                font-weight: 500;
                font-size: 10px;
                line-height: 16px;
                letter-spacing: 1.5px;
                text-transform: uppercase;"
        >
          <v-icon style="padding-bottom:2px">
            mdi-keyboard-backspace
          </v-icon>
          Back
        </v-btn>
      </v-toolbar-title>
      <!-- <v-app-bar-nav-icon @click="drawer = true" /> -->
      <v-toolbar-title
        v-if="Route.name === 'ChatUser'"
      >
        <v-list-item
          :to="'/UserProfile/' + DialogUser.id"
        >
          <v-list-item-avatar v-if="DialogUser.profile.avatar">
            <v-img
              :src="DialogUser.profile.avatar"
            />
          </v-list-item-avatar>
          <v-list-item-avatar
            v-else
            color="basic"
          >
            <v-avatar
              size="36px"
              color="basic"
            >
              <span
                class="white--text"
                style="padding-left:3.5px"
              >
                {{ getUserInitials(DialogUser) }}
              </span>
            </v-avatar>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="title"
            >
              {{ getUserName(DialogUser) }}
            </v-list-item-title>
            <v-list-item-subtitle>
              <span
                :class="(DialogUser.profile.status === 'online' ? 'basic--text text--lighten' : 'text_second--text')"
              >
                {{ DialogUser.profile.status }}
              </span>
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
            @click.stop="dialogForDeleteChat = true"
          >
            <v-list-item-title>
              Delete chat
            </v-list-item-title>
          </v-list-item>
          <v-dialog
            v-model="dialogForDeleteChat"
            max-width="400"
          >
            <v-card>
              <v-card-title class="headline">
                Delete chat
              </v-card-title>

              <v-card-text>
                Are you sure you want to delete this chat and all its messages?<br>
                This action cannot be undone.
              </v-card-text>

              <v-card-actions>
                <v-spacer />

                <v-btn
                  color="basic"
                  text
                  @click="dialogForDeleteChat = false"
                >
                  CANCEL
                </v-btn>

                <v-btn
                  color="red"
                  text
                  @click="deleteChat(),dialogForDeleteChat = false"
                >
                  DELETE CHAT
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
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
      style=""
      :width="($vuetify.breakpoint.width * 0.225 > 600 ? 600 : $vuetify.breakpoint.width * 0.225)"
      app
      color="background_white"
      permanent
    >
      <v-card tile>
        <v-list
          color="background_user"
          dark
          height="80"
          class="pt-1"
        >
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                class="title"
              >
                {{ getUserName(getClient) }}
              </v-list-item-title>
              <v-list-item-subtitle
                v-if="getClientProfile.is_online"
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
              style="text-decoration: none;"
              to="/MyProfile"
            >
              <v-list-item-avatar v-if="getClientProfile.avatar">
                <v-img
                  :src="getClientProfile.avatar"
                />
              </v-list-item-avatar>
              <v-list-item-avatar
                v-else
                color="background_white"
              >
                <span
                  class="basic--text"
                >
                  {{ MakeAvatar }}
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
        <ContactList v-if="currentTab.name == 'mdi-account-circle'" />
        <DialogsList v-if="currentTab.name == 'mdi-message-text'" />
        <settings
          v-if="currentTab.name == 'mdi-cog'"
        />
        <v-footer
          absolute
          padless
          class="background_white"
          style="height:56px;box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2), 0px 2px 2px rgba(0, 0, 0, 0.12), 0px 0px 2px rgba(0, 0, 0, 0.14);"
        >
          <v-btn
            fab
            color="basic"
            dark
            top
            right
            absolute
            @click.stop="dialogForPlusButton = true"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-dialog
            v-model="dialogForPlusButton"
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
                  @click="dialogForPlusButton = false"
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
              :class="['tab-button', { 'basic--text': currentTab.name === tab.name }]"
              @click="changeTab(tab)"
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
import ContactList from './components/ContactList'
import DialogsList from './components/DialogsList'
import { mapActions, mapGetters, mapMutations } from 'vuex'

let UpdateContants = new WebSocket(
  (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/users/'
)

Vue.use(VueCookie)
var tabs = [
  {
    id: 0,
    name: 'mdi-account-circle',
    display_name: 'Contacts',
    component: {
    }
  },
  {
    id: 1,
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
    id: 2,
    name: 'mdi-cog',
    display_name: 'Settings',
    component: {
    }
  }
]
export default {
  new: '#dynamic-component',
  components: { SystemInfo, settings, ContactList, DialogsList },
  data: () => ({
    userSearch: '',
    tabs: tabs,
    dialogForDeleteChat: false,
    currentTab: tabs[1],
    dialogForPlusButton: false
  }),
  computed: {
    ...mapGetters(['getUserId', 'getClient', 'getClientProfile', 'getDialogsList', 'getUsersByDialogId']),
    Route () {
      return this.$route
    },
    DialogUser () {
      if (typeof this.getUsersByDialogId(this.$route.params.id) !== 'undefined') {
        if (this.getUsersByDialogId(this.$route.params.id).length > 0) {
          return this.getUsersByDialogId(this.$route.params.id)[0]
        } else {
          return { username: 'Произошла ошибка', profile: { avatar: null, status: '' }
          }
        }
      }
      return { username: 'Загрузка...', profile: { avatar: null, status: 'Загрузка...' } }
    },
    MakeAvatar () {
      if (typeof this.getClient !== 'undefined') {
        if (this.getClient.first_name !== '' && this.getClient.last_name !== '') {
          return this.getClient.first_name[0].toUpperCase() + this.getClient.last_name[0].toUpperCase()
        }
        if (this.getClient.first_name !== '') {
          return this.getClient.first_name[0].toUpperCase()
        }
        if (this.getClient.last_name !== '') {
          return this.getClient.last_name[0].toUpperCase()
        }
        if (this.getClient.username !== '') {
          return this.getClient.username[0].toUpperCase()
        }
      }
      return '...'
    }
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['disconnect']
  },
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
    this.$vuetify.theme.dark = (localStorage.getItem('Dark') === 'true')
    if (this.tabs.find(tab => tab.id == localStorage.getItem('Tab'))) {
      this.currentTab = this.tabs[localStorage.getItem('Tab')]
    } else {
      this.currentTab = this.tabs[1]
    }
  },
  mounted () {
    let Vue = this
    document.addEventListener('keydown', function (event) {
      const key = event.key // Or const {key} = event; in ES6+
      if (key === 'Escape' && Vue.$route.fullPath !== '/') {
        Vue.$router.push('/')
      }
    })
    setInterval(this.updateToken, 1000)
    this.getUserData(this.getUserId)
    this.getContactsData()
    this.getDialogsData(this.getUserId)
    UpdateContants.onopen = function () {
      UpdateContants.send(
        JSON.stringify(
          {
            action: 'subscribe_to_contacts',
            request_id: Vue.getUserId
          }
        )
      )
    }
    UpdateContants.onmessage = function (event) {
      console.log(JSON.parse(event.data).data)
      if (JSON.parse(event.data).data) {
        Vue.addUser((JSON.parse(event.data).data))
      }
    }
  },
  methods: {
    ...mapActions(['getUserData', 'getContactsData', 'getDialogsData']),
    ...mapMutations(['addUser', 'DeleteDialog']),
    changeTab (tab) {
      this.currentTab = tab
      localStorage.setItem('Tab', tab.id)
    },
    getUserName (user) {
      if (typeof user !== 'undefined') {
        if (user.first_name && user.last_name) {
          return (user.first_name + ' ' + user.last_name)
        } else if (user.first_name) {
          return user.first_name
        } else if (user.last_name) {
          return user.last_name
        } else {
          return user.username
        }
      }
    },
    GetUnreadMessages (dialog) {
      console.log(dialog.unread_messages[dialog.users[1]])
      if (typeof this.user_id !== 'undefined') {
        if (dialog.users[0] === this.user_id) {
          return dialog.unread_messages[dialog.users[0]]
        }
        return dialog.unread_messages[dialog.users[1]]
      }
    },
    getUserInitials (user) {
      if (typeof user !== 'undefined') {
        if (user.first_name && user.last_name) {
          return (user.first_name[0] + user.last_name[0]).toUpperCase()
        } else if (user.first_name) {
          return user.first_name[0].toUpperCase()
        } else if (user.last_name) {
          return user.last_name[0].toUpperCase()
        } else {
          return user.username[0].toUpperCase()
        }
      } return ''
    },
    GoBack () {
      this.$router.go(-1)
    },
    disconnect () {
      this.$disconnect()
    },
    deleteChat () {
      api.axios.delete('/api/dialog/' + this.$route.params.id + '/').then()
      this.DeleteDialog(this.$route.params.id)
      this.$router.go(-1)
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
    goProfilePage () {
      this.$router.push({ name: 'Profile', params: { id: this.user_id } })
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
