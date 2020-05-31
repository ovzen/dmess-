<template>
  <div>
    <v-divider />
    <v-col>
      <v-text-field
        v-model="dialogSearch"
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
    <div
      v-if="getDialogsList.length"
    >
      <div
        v-for="dialog in (dialogSearch ? SortDialogs : getDialogsList)"
        :key="dialog.id"
      >
        <v-list-item
          :to="{ name: 'ChatUser', params: { id: dialog.id } }"
        >
          <v-list-item-avatar>
            <v-avatar
              v-if="getUsersByDialog(dialog).length > 0"
              size="36px"
              color="basic"
            >
              <v-img
                v-if="getUsersByDialog(dialog)[0].profile.avatar !== null"
                :src="getUsersByDialog(dialog)[0].profile.avatar"
              />
              <span
                v-else
                class="white--text"
              >
                {{ MakeAvatar(getUsersByDialog(dialog)[0]) }}
              </span>
            </v-avatar>
            <v-avatar
              v-else
              size="36px"
              color="basic"
            />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>
              {{ getContactName(getUsersByDialog(dialog)[0]) }}
            </v-list-item-title>
            <v-list-item-subtitle style="min-width:10px;min-height:18.67px;">
              <span
                style="color:#757575; font-size:115%;"
              >
                {{ (dialog.last_message ? (dialog.last_message.text ? decodeEmojiCode(dialog.last_message.text) : (dialog.last_message.image_url ? 'Image' : ' ')) : ' ') }}
              </span>
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-list-item-action-text v-if="dialog.last_message">
              {{ formatTime(dialog.last_message.create_date) }}
            </v-list-item-action-text>
            <v-avatar
              v-if="GetUnreadMessages(dialog)"
              color="basic"
              class="subheading white--text"
              size="24"
              v-text="GetUnreadMessages(dialog)"
            />
          </v-list-item-action>
        </v-list-item>
        <v-divider
          inset
        />
      </div>
    </div>
    <div
      v-else
      class="d-flex flex-column justify-center align-center fill-height"
      style="height:75vh"
    >
      <div class="mt-12">
        <p class="display-2 text-center grey--text">
          ( つ ^‿^ )つ
        </p>
        <p class="overline text-center font-weight-medium text_second--text">
          START MESSAGING WITH SOMEONE
          <br>
          CHAT WILL BE DISPLAY HERE
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { mapActions, mapGetters, mapMutations } from 'vuex'
import { emojis } from 'vue-chat-emoji'
let ws = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/dialog_notifications/')

export default {
  name: 'DialogsList',
  data: () => ({
    dialogSearch: ''
  }),
  computed: {
    ...mapGetters(['getDialogsList', 'getUsersByDialog', 'getUserId', 'isDialogDownloaded', 'getUserById']),
    SortDialogs () {
      return this.getDialogsList.filter(dialog => {
        if (this.getUsersByDialog(dialog).length === 0) {
          return false
        } else {
          return this.getUserName(this.getUsersByDialog(dialog)[0]).toLowerCase().indexOf(this.dialogSearch.toLowerCase()) > -1
        }
      })
    }
  },
  mounted () {
    let Vue = this
    ws.onmessage = function (event) {
      let UpdateDialog = JSON.parse(event.data).data
      Vue.UpdateDialogByWs(UpdateDialog)
    }
    this.DownloadUsersInDialogs()
  },
  methods: {
    ...mapMutations(['UpdateDialogByWs']),
    ...mapActions(['getUserData']),
    DownloadUsersInDialogs () {
      if (this.isDialogDownloaded === true) {
        for (let dialog in this.getDialogsList) {
          for (let user in this.getDialogsList[dialog].users) {
            this.getUserData(this.getDialogsList[dialog].users[user])
          }
        }
      } else {
        setTimeout(this.DownloadUsersInDialogs, 250)
      }
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
    GetUnreadMessages (dialog) {
      if (typeof this.getUserId !== 'undefined') {
        if (dialog.users[0] === this.getUserId) {
          return dialog.unread_messages[dialog.users[0]]
        }
        return dialog.unread_messages[dialog.users[1]]
      }
      return ''
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
    getContactName (users) {
      // console.log(users)
      if (typeof users !== 'undefined') {
        return this.getUserName(users)
      } else {
        return 'В диалоге нет других пользователей'
      }
    },
    getContact (users) {
      return (users[0].id === this.user_id) ? users[1] : users[0]
    },
    decodeEmojiCode (str) {
      return emojis.decodeEmoji(str)
    }
  }
}
</script>
