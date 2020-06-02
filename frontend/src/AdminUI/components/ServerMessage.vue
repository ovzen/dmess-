<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Server Message
        <v-spacer />
      </v-card-title>
      <v-card-text>
        <v-form v-model="valid">
          <v-text-field
            v-model="Message"
            :rules="Required"
            label="Message"
            required
          />
          <v-select
            v-model="type"
            :items="types"
            label="Message type"
            required
          />
          <v-btn
            color="primary"
            @click="SendMessage(Message,type)"
          >
            Send message
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'UserActivity',
  data: () => ({
    type: 'primary',
    valid: false,
    Message: '',
    Required: [v => !!v || 'This field is required'],
    types: ['primary', 'warning', 'error'],
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
