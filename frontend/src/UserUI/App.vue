<template>
  <v-app>
    <v-app-bar
      app
      :value="!(AlwaysOnDisplay || ExpandOnHover)"
      collapse-on-scroll
      dark
      scroll-target="#scrolling-techniques-6"
    >
      <v-app-bar-nav-icon @click="drawer = true" />
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
      absolute
      :app="AlwaysOnDisplay"
      :expand-on-hover="ExpandOnHover"
      :temporary="!(AlwaysOnDisplay || ExpandOnHover)"
    >
      <v-row no-gutters>
        <v-navigation-drawer
          v-model="drawer"
          dark
          :app="ExpandOnHover"
          mini-variant
          mini-variant-width="56px"
          absolute
        >
          <v-list>
            <v-list-item>
              <v-list-item-action>
                <v-btn
                  icon
                  small
                  @click="$router.go(-1)"
                >
                  <v-icon>mdi-arrow-left-circle</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-list-item>
              <v-list-item-action>
                <v-icon>mdi-settings</v-icon>
              </v-list-item-action>
            </v-list-item>
            <v-divider />
            <v-list-item>
              <v-list-item-avatar>
                <v-img src="https://www.technistone.com/color-range/image-slab/deska_gobi_black_p.jpg" />
              </v-list-item-avatar>
            </v-list-item>
            <v-list-item>
              <v-list-item-avatar>
                <v-img src="https://www.technistone.com/color-range/image-slab/deska_gobi_black_p.jpg" />
              </v-list-item-avatar>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
        <v-list
          class="pa-9"
          nav
          dense
          style="padding-right: 0px !important;padding-left: 58px !important;"
        >
          <v-list-item-group
            v-model="group"
          >
            <v-list-item
              v-for="dialog in dialogs_for_user"
              :key="dialog.id"
              class="grow"
              @click="openDialog(dialog.id)"
            >
              <v-list-item-icon>
                <v-icon>mdi-chat</v-icon>
              </v-list-item-icon>
              <v-list-item-content>{{ dialog.name }}</v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <div style="position: absolute; top: 80%;">
          <v-switch
            v-model="AlwaysOnDisplay"
            label="Постоянное отображение меню"
            style="padding-right: 0px !important;padding-left: 58px !important;"
            :disabled="ExpandOnHover"
          />
          <v-switch
            v-model="ExpandOnHover"
            label="Мини версия меню"
            style="padding-right: 0px !important;padding-left: 58px !important;"
            :disabled="AlwaysOnDisplay"
          />
        </div>
      </v-row>
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
    drawer: false,
    AlwaysOnDisplay: false,
    ExpandOnHover: false,
    group: [],
    for_user: true,
    dialogs_for_user: [],
    username: 'Test',
    user_id: undefined
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
