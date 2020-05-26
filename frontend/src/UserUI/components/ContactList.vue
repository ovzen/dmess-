<template>
  <div>
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
    <v-divider v-if="(userSearch != '' ? SortContacts : getContacts).length > 0" />
    <div
      v-for="contact in (userSearch != '' ? SortContacts : getContacts)"
      :key="contact.id"
    >
      <v-list-item
        :to="'/UserProfile/' + contact.id"
      >
        <v-list-item-avatar>
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
          <v-list-item-title>
            {{ contact.username }}
          </v-list-item-title>
          <v-list-item-subtitle>
            <span
              class="basic--text text--lighten"
            >
              {{ contact.profile.status }}
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
      <v-divider v-if="getUsersByName(userSearch).length > 0" />
      <div
        v-for="user in getUsersByName(userSearch)"
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
                {{ MakeAvatar(user) }}
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
          v-if="user.id !== getUsersByName(userSearch)[getUsersByName(userSearch).length-1].id"
          inset
        />
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'Example',
  data: () => ({
    userSearch: '',
    findedUsers: ''
  }),
  computed: {
    ...mapGetters(['getUserId', 'getContacts', 'getContactsId', 'getClient', 'getClientProfile', 'getUsersByName']),
    SortContacts () {
      return this.getContacts.filter(contact => { return contact.username.toLowerCase().indexOf(this.userSearch.toLowerCase()) > -1 })
    }
  },
  methods: {
    ...mapActions(['getUserData']),
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
