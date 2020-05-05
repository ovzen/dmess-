<template>
  <v-container>
    <v-footer
      color="background_white"
      absolute
      padless
    >
      <v-form style="width:100%;">
        <v-row>
          <v-col
            style="padding-bottom: 0px; padding-top: 0px; padding-left:20px; padding-right:20px"
            cols="12"
          >
            <v-text-field
              v-model="message"
              dense
              single-line
              :append-outer-icon="message ? 'mdi-send' : 'mdi-microphone'"
              :prepend-icon="icon"
              label="Message"
              type="text"
              @click:append-outer="sendMessage(message)"
              @click:prepend="changeIcon"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-footer>
  </v-container>
</template>

<script>
import VueNativeSock from 'vue-native-websocket'
import Vue from 'vue'

export default {
  name: 'ChatInput',
  data: () => ({
    password: 'Password',
    show: false,
    message: '',
    marker: true,
    iconIndex: 0,
    icons: [
      'mdi-paperclip'
    ]
  }),

  computed: {
    icon () {
      return this.icons[this.iconIndex]
    }
  },

  methods: {
    toggleMarker () {
      this.marker = !this.marker
    },
    sendMessage (message) {
      this.resetIcon()
      if (message) {
        console.log('messagetext: ', message)
        this.$socket.send(
          JSON.stringify({
            message: message
          })
        )
        this.clearMessage()
      }
    },
    clearMessage () {
      this.message = ''
    },
    resetIcon () {
      this.iconIndex = 0
    },
    changeIcon () {
      this.iconIndex === this.icons.length - 1
        ? this.iconIndex = 0
        : this.iconIndex++
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
