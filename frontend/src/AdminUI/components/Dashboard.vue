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
              class="headline indigo--text mb-1"
            >
              + 45
            </v-list-item-title>
            <v-list-item-subtitle>
              last updated 3 minutes ago
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-avatar
            tile
            size="80"
            color="indigo"
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
              class="headline indigo--text mb-1"
            >
              + 2542
            </v-list-item-title>
            <v-list-item-subtitle>
              last updated 3 minutes ago
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-avatar
            tile
            size="80"
            color="indigo"
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
              class="headline indigo--text mb-1"
            >
              215
            </v-list-item-title>
            <v-list-item-subtitle>
              last updated 3 minutes ago
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-avatar
            tile
            size="80"
            color="indigo"
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
            color="primary"
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
            color="indigo"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-account-plus-outline
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="display-2 indigo--text text-right mb-1"
            >
              {{ gitlabOpenIssues }}
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
            color="indigo"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-account-plus-outline
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="display-2 indigo--text text-right mb-1"
            >
              75
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
            color="indigo"
          >
            <v-icon
              color="white"
              x-large
            >
              mdi-account-plus-outline
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              class="display-2 indigo--text text-right mb-1"
            >
              75
            </v-list-item-title>
            <v-list-item-subtitle class="text-right">
              Opened issues on gitlab
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios'
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
    ws: new WebSocket('ws://' + window.location.host + '/ws/chat/system/'),
    gitlabOpenIssues: undefined
  }),
  created () {
    this.getGitlabOpenIssues()
    window.addEventListener('resize', this.updateWidthOfElements)
    this.ContainerWidth = document.getElementById('Container').offsetWidth
  },
  destroyed () {
    window.removeEventListener('resize', this.updateWidthOfElements)
  },
  methods: {
    getGitlabOpenIssues () {
      const instance = axios.create({
        timeout: 1000,
        headers: { 'Authorization': 'Bearer NgXcHgR-7W1Uq6mYrJMU' }
      })
      instance.get('https://gitlab.informatics.ru/api/v4/projects/1932/issues_statistics')
        .then(res => {
          console.log(res)
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
  color: #2c3e50;
}
.v-card {
  margin-top:25px;
  margin-left: 10px;
  margin-right: 10px;
}

</style>
