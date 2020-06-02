<template>
  <div>
    <v-divider />
    <v-col>
      <v-text-field
        v-model="userSearch"
        clearable
        solo
        background-color="search"
        dense
        flat
        color="basic"
        hide-details
        prepend-inner-icon="mdi-magnify"
        label="Search for users"
        style="border-radius:50px; max-width:450px;"
        @input="getUsersBySearch(userSearch)"
        @click:clear="clearSearch()"
      />
    </v-col>
    <v-divider />
    <div
      v-if="getContacts.length"
    >
      <div
        v-for="contact in (userSearch ? getContactsByName(userSearch) : getContacts)"
        :key="contact.id"
      >
        <v-list-item
          color="sidebar_select"
          :to="'/UserProfile/' + contact.id"
        >
          <v-list-item-avatar v-if="contact.profile.avatar">
            <v-img
              :src="contact.profile.avatar"
            />
          </v-list-item-avatar>
          <v-list-item-avatar
            v-else
          >
            <v-avatar
              size="36px"
              color="basic"
            >
              <span
                class="white--text"
              >
                {{ MakeAvatar(contact) }}
              </span>
              <!--<v-img
              src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
            />-->
            </v-avatar>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="black--text"
            >
              {{ getUserName(contact) }}
            </v-list-item-title>
            <v-list-item-subtitle>
              <span
                :class="(contact.profile.status === 'online' ? 'basic_text--text text--lighten' : 'text_second--text')"
              >
                {{ contact.profile.status }}
              </span>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-divider
          v-if="!(getContactsByName(userSearch)[getContactsByName(userSearch).length-1].id == contact.id) || !userSearch"
          inset
        />
      </div>
    </div>
    <div
      v-if="!userSearch && !getContacts.length"
      class="d-flex flex-column justify-center align-center fill-height"
      style="height:75vh"
    >
      <div class="mt-12">
        <p class="display-2 text-center grey--text">
          ʕつ •ᴥ• ʔつ
        </p>
        <p class="overline text-center font-weight-medium text_second--text">
          ADD NEW CONTACTS!
          <br>
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
        v-if="getUsersByName(userSearch).length"
      >
        <div
          v-for="user in getUsersByName(userSearch)"
          :key="user.id"
        >
          <v-list-item
            :to="'/UserProfile/' + user.id"
          >
            <v-list-item-avatar v-if="user.profile.avatar">
              <v-img
                :src="user.profile.avatar"
              />
            </v-list-item-avatar>
            <v-list-item-avatar
              v-else
            >
              <v-avatar
                size="36px"
                color="basic"
              >
                <span
                  class="white--text"
                >
                  {{ MakeAvatar(user) }}
                </span>
              </v-avatar>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                {{ getUserName(user) }}
              </v-list-item-title>
              <v-list-item-subtitle>
                <span
                  :class="(user.profile.status === 'online' ? 'basic--text text--lighten' : 'text_second--text')"
                >
                  {{ user.profile.status }}
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
</template>

<script>
import api from '../api'
import { mapActions, mapGetters, mapMutations } from 'vuex'

let UpdateContants = new WebSocket(
  (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/users/'
)

export default {
  name: 'ContactList',
  data: () => ({
    userSearch: ''
  }),
  computed: {
    ...mapGetters(['getUserId', 'getContacts', 'getContactsId', 'getClient', 'getClientProfile', 'getUsersByName', 'getContactsByName'])
  },
  mounted () {
    let Vue = this
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
      if (JSON.parse(event.data).data) {
        Vue.addUser((JSON.parse(event.data).data))
      }
    }
  },
  methods: {
    ...mapActions(['getUserData']),
    ...mapMutations(['addUser']),
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
    getUsersBySearch () {
      api.axios.get('/api/users/', {
        params: {
          search: this.userSearch
        }
      }).then(res => {
        for (let user in res.data.results) {
          this.getUserData(res.data.results[user].id)
        }
      })
    },
    clearSearch () {
      this.userSearch = ''
    },
    MakeAvatar (UserProfile) {
      if (typeof UserProfile !== 'undefined') {
        if (UserProfile.first_name !== '' && UserProfile.last_name !== '') {
          return UserProfile.first_name[0] + UserProfile.last_name[0]
        }
        if (UserProfile.first_name !== '') {
          return UserProfile.first_name[0]
        }
        if (UserProfile.last_name !== '') {
          return UserProfile.last_name[0]
        }
        if (UserProfile.username !== '') {
          return UserProfile.username[0]
        }
      }
      return '...'
    }
  }
}
</script>
