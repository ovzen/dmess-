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
        style="font-style: normal;
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
        style="padding-top: 140px;"
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
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'ContactList',
  data: () => ({
    userSearch: ''
  }),
  computed: {
    ...mapGetters(['getUserId', 'getContacts', 'getContactsId', 'getClient', 'getClientProfile', 'getUsersByName', 'getContactsByName'])
  },
  methods: {
    ...mapActions(['getUserData']),
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
      clearTimeout(this._timerId)
      this._timerId = setTimeout(() => {
        if (this.userSearch) {
          api.axios.get('/api/users/', {
            params: {
              search: this.userSearch
            }
          }).then(res => {
            for (let user in res.data.results) {
              this.getUserData(res.data.results[user].id)
            }
          })
        }
      }, 500)
    },
    clearSearch () {
      this.userSearch = ''
    },
    MakeAvatar (UserProfile) {
      if (typeof UserProfile !== 'undefined') {
        if (UserProfile.first_name !== '' && UserProfile.last_name !== '') {
          return UserProfile.first_name[0].toUpperCase() + UserProfile.last_name[0].toUpperCase()
        }
        if (UserProfile.first_name !== '') {
          return UserProfile.first_name[0].toUpperCase()
        }
        if (UserProfile.last_name !== '') {
          return UserProfile.last_name[0].toUpperCase()
        }
        if (UserProfile.username !== '') {
          return UserProfile.username[0].toUpperCase()
        }
      }
      return '...'
    }
  }
}
</script>
