<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Dialog Activity
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        />
      </v-card-title>
      <v-data-table
        :loading="loading"
        loading-text="Loading... Please wait"
        :headers="headers"
        :items="Dialogs"
        :search="search"
        :sort-desc="[false, true]"
        multi-sort
        :custom-filter="filter"
        class="elevation-1"
      >
        <template v-slot:item.users="{ item }">
          {{ formatUsers(item.users) }}
        </template>
        <template v-slot:item.create_date="{ item }">
          {{ formatTime(item.create_date) }}
        </template>
        <template v-slot:item.check_dialog="{ item }">
          <v-btn
            color="succes"
            small
            @click="GoToChat(item)"
          >
            To the chat
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import api from '../api'
import moment from 'moment'
export default {
  name: 'DialogActivity',
  data: () => ({
    search: '',
    loading: true,
    dialog: false,
    users: [],
    Dialogs: []
  }),
  computed: {
    headers () {
      return [
        {
          text: 'ID',
          value: 'id',
          sortable: false
        },
        {
          text: 'Users',
          value: 'users',
          sortable: false,
          align: 'center'
        },
        { text: 'Created',
          value: 'create_date',
          align: 'center',
          sortable: true,
          sort: (a, b) => {
            if (moment(a) < moment(b)) {
              return 1
            }
            if (moment(a) > moment(b)) {
              return -1
            } return 0
          }
        },
        { text: 'Actions',
          value: 'check_dialog',
          sortable: false,
          align: 'center'
        }
      ]
    }
  },
  mounted () {
    this.update()
  },
  methods: {
    filter: (value, search, item) => {
      console.log(moment(value).format('DD.MM.YYYY hh:mm').indexOf(search))
      return (item.id.indexOf(search) > -1) || (moment(item.create_date).format('DD.MM.YYYY hh:mm').indexOf(search) > -1)
    },
    update () {
      api.axios.get('/api/dialog/').then(res => {
        this.Dialogs = res.data.results
        this.loading = false
        for (let dialog in this.Dialogs) {
          for (let user in this.Dialogs[dialog].users) {
            api.axios.get('/api/users/' + this.Dialogs[dialog].users[user] + '/').then(res => {
              if (this.users.filter(us => us.id === this.Dialogs[dialog].users[user]).length === 0) { this.users.push(res.data) }
            })
          }
        }
      })
    },
    formatTime (datetime) {
      if (datetime) {
        return moment(String(datetime)).format('DD.MM.YYYY hh:mm')
      }
    },
    formatUsers (users) {
      let str = ''
      for (let user in users) {
        if (typeof this.users.find(us => us.id === users[user]) !== 'undefined') {
          str = str + this.users.find(us => us.id === users[user]).username + ' '
        }
      }
      return str
    },
    GoToChat (item) {
      window.location.pathname = '/ChatUser/' + item.id + '/'
    }
  }
}
</script>

<style lang="scss" scoped>
.v-card {
  margin:20px
}
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
