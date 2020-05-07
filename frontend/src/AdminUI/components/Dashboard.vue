<template>
  <v-container
    id="Container"
    justify-center
    my-6
    liquid
    class="d-flex align-content-space-between justify-space-between flex-wrap"
  >
    <div
      id="FirstGroup"
      :class="'flex-grow-1 d-flex justify-space-between ' + ((ContainerWidth <= 900 || ContainerWidth > 1200 ) ? 'flex-column' : '' ) "
    >
      <v-card
        class="pa-2"
        min-width="120"
        outlined
        elevation="12"
      >
        <v-list-item three-line>
          <v-list-item-content>
            <div
              class="overline black--text"
            >
              DAILY SIGN UPS
            </div>
            <v-list-item-title
              class="headline basic--text mb-1"
            >
              {{ dashboardStats.todayRegistrations }}
            </v-list-item-title>
            <v-list-item-subtitle>
              last updated {{ minutes_went }}
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-avatar
            tile
            size="80"
            color="basic"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-account-plus-outline
            </v-icon>
          </v-list-item-avatar>
        </v-list-item>
      </v-card>
      <v-card
        class="pa-2"
        outlined
        elevation="12"
      >
        <v-list-item three-line>
          <v-list-item-content>
            <div
              class="overline black--text"
            >
              DAILY MESSAGES
            </div>

            <v-list-item-title
              class="headline basic--text mb-1"
            >
              {{ dashboardStats.todayMessages }}
            </v-list-item-title>
            <v-list-item-subtitle>
              last updated {{ minutes_went }}
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-avatar
            tile
            size="80"
            color="basic"
            elevation="12"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-message-text-outline
            </v-icon>
          </v-list-item-avatar>
        </v-list-item>
      </v-card>
      <v-card
        class="pa-2"
        outlined
        elevation="12"
      >
        <v-list-item three-line>
          <v-list-item-content>
            <div
              class="overline black--text"
            >
              ONLINE RIGHT NOW
            </div>
            <v-list-item-title
              class="headline basic--text mb-1"
            >
              {{ dashboardStats.currentlyOnline }}
            </v-list-item-title>
            <v-list-item-subtitle>
              last updated {{ minutes_went }}
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-avatar
            tile
            size="80"
            color="basic"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-account-multiple-outline
            </v-icon>
          </v-list-item-avatar>
        </v-list-item>
      </v-card>
    </div>
    <v-card
      class="pa-2 flex-grow-1"
      min-width="120"
      outlined
      elevation="12"
    >
      <v-card-title>
        Employees stat
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
        :headers="headers"
        :items="Users"
        :search="search"
        :sort-by="['Username', 'Datetime']"
        :sort-desc="[false, true]"
        multi-sort
        class="elevation-1"
      />
    </v-card>

    <v-card
      class="pa-2 flex-grow-1"
      outlined
      elevation="12"
    >
      <v-card-title>
        Server Message
        <v-spacer />
      </v-card-title>
      <v-card-text>
        <v-form v-model="valid">
          <v-text-field
            v-model="Message"
            :rules="Required"
            label="Сообщение"
            required
          />
          <v-select
            v-model="type"
            :items="types"
            label="Тип сообщения"
            required
          />
          <v-img
            height="130"
          />
          <v-btn
            small
            dark
            color="basic"
            @click="SendMessage(Message,type)"
          >
            отправить
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <div
      id="SecondGroup"
      :class="'flex-grow-1 d-flex justify-space-between ' + (ContainerWidth <= 900 ? 'flex-column' : '' ) "
    >
      <v-card
        class="pa-2"
        outlined
        elevation="12"
      >
        <v-list-item three-line>
          <v-list-item-avatar
            tile
            size="80"
            color="basic"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-cards-outline
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="display-2 basic--text text-right mb-1"
            >
              {{ gitlabMetrics.openedIssues }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-right">
              Opened issues on gitlab
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-card>

      <v-card
        class="pa-2"
        outlined
        elevation="12"
      >
        <v-list-item three-line>
          <v-list-item-avatar
            tile
            size="80"
            color="basic"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-call-merge
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="display-2 basic--text text-right mb-1"
            >
              {{ gitlabMetrics.openedMergeRequests }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-right">
              Opened merge requests on gitlab
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-card>

      <v-card
        class="pa-2"
        outlined
        elevation="12"
      >
        <v-list-item three-line>
          <v-list-item-avatar
            tile
            size="80"
            color="basic"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-call-split
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="display-2 basic--text text-right mb-1"
            >
              {{ this.gitlabMetrics.currentBranches }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-right">
              Current branches on gitlab
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
export default {
  name: 'Dashboard',
  data: () => ({
    search: '',
    type: 'primary',
    valid: false,
    Message: '',
    ContainerWidth: undefined,
    Required: [v => !!v || 'This field is required'],
    types: ['primary', 'warning', 'error'],
    headers: [
      {
        text: 'Username',
        align: 'start',
        value: 'Username'
      },
      { text: 'LastActivity', value: 'LastActivity' }
    ],
    Users: [
      {
        Username: 'petrp',
        LastActivity: '2020-03-11 13:53:19.368414'
      },
      {
        Username: 'Admin',
        LastActivity: '2020-03-7 13:53:19.368414'
      },
      {
        Username: 'Moderator',
        LastActivity: '2020-03-9 13:53:19.368414'
      },
      {
        Username: 'User',
        LastActivity: '2020-03-10 13:53:19.368414'
      }
    ],
    ws: new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/system/'),
    dashboardStats: {
      currentlyOnline: undefined,
      todayRegistration: undefined,
      todayMessages: undefined
    },
    gitlabMetrics: {
      openedIssues: undefined,
      openedMergeRequests: undefined,
      currentBranches: undefined
    },
    initial_time: moment(),
    minutes_went: moment().fromNow()
  }),
  created () {
    this.getGitlabMetrics()
    this.getDashboardStatistics()
    window.addEventListener('resize', this.updateWidthOfElements)
    this.ContainerWidth = document.getElementById('Container').offsetWidth
  },
  destroyed () {
    window.removeEventListener('resize', this.updateWidthOfElements)
  },
  methods: {
    startInterval: function () {
      setInterval(() => {
          this.minutes_went = this.initial_time.fromNow()
      }, 60000)
    },
    getGitlabMetrics () {
      axios.get('/api/admin/gitlabmetrics/')
        .then(res => {
          this.gitlabMetrics.openedIssues = res.data.opened_issues
          this.gitlabMetrics.openedMergeRequests = res.data.opened_merge_requests
          this.gitlabMetrics.currentBranches = res.data.current_branches
        })
    },
    getDashboardStatistics () {
      this.startInterval()
      axios.get('/api/admin/users/stat/')
        .then(res => {
          this.dashboardStats.currentlyOnline = res.data.count
        })
      axios.get('/api/admin/register/stat/')
        .then(res => {
          this.dashboardStats.todayRegistrations = res.data.count
        })
      axios.get('/api/messages/count/')
        .then(res => {
          this.dashboardStats.todayMessages = res.data.count
        })
    },
    SendMessage (Message, type) {
      this.ws.send(JSON.stringify({ message: Message, type: type }))
    },
    updateWidthOfElements () {
      console.log('e')
      this.ContainerWidth = document.getElementById('Container').offsetWidth
    }
  }
}

</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}
.v-card {
  margin-top:25px;
  margin-left: 10px;
  margin-right: 10px;
}

</style>
