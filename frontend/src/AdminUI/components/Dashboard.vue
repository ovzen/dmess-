<template>
  <v-container
    justify-center
    my-6
  >
    <v-card
      class="d-inline-block mx-5"
      max-width="320"
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
      class="d-inline-block mx-5"
      max-width="320"
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
      class="d-inline-block mx-4"
      max-width="320"
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

    <v-container
      justify-center
      mt-6
    >
      <v-card
        class="d-inline-block mx-auto"
        max-width="500"
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
        class="d-inline-block mx-5"
        width="500"
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

      <v-container
        justify-center
        mt-9
      >
        <v-card
          class="d-inline-block me-6"
          max-width="285"
          outlined
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
          class="d-inline-block mx-9"
          max-width="285"
          outlined
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
          class="d-inline-block mx-9"
          max-width="285"
          outlined
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
      </v-container>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: 'Dashboard',
  data: () => ({
    search: '',
    type: 'primary',
    valid: false,
    Message: '',
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
    ws: new WebSocket('ws://' + window.location.host + '/ws/chat/system/')
  }),
  methods: {
    SendMessage (Message, type) {
      this.ws.send(JSON.stringify({ message: Message, type: type }))
    }
  }
}

</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
