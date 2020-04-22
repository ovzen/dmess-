<template>
  <v-container>
    <div
      class="text-left"
    >
      <v-card
        shaped
        max-width="460px"
        class="float-right d-flex"
      >
        <v-card-text class="font-weight-black">
          Text Message
          <v-list-item-action-text
            class="pl-5"
          >
            18:00
          </v-list-item-action-text>
        </v-card-text>
      </v-card>
    </div>
    <v-container
      class="d-flex"
    >
      <div
        class="text-left"
      >
        <v-card
          shaped
          max-width="460px"
          class="d-flex"
          color="pink lighten-5"
        >
          <v-card-text class="font-weight-black">
            Text Message
            <v-list-item-action-text
              class="pl-5"
            >
              18:00
            </v-list-item-action-text>
          </v-card-text>
        </v-card>
      </div>
    </v-container>
    <v-form>
      <v-row>
        <v-col
          cols="12"
        >
          <v-text-field
            v-model="message"
            :append-outer-icon="message ? 'mdi-send' : 'mdi-microphone'"
            :prepend-icon="icon"
            solo
            label="Message"
            type="text"
            @click:append-outer="sendMessage"
            @click:prepend="changeIcon"
          />
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'ChatUser',
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
    sendMessage () {
      this.resetIcon()
      this.clearMessage()
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
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  border-radius: 6px;
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
  background-color:rgba(0,0,0,0.7);
}
.rounded-card{
    border-radius:50px;
}
.container {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.v-application--wrap {
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  min-height: 10px;
  max-width: 100%;
  position: relative;
}
</style>
