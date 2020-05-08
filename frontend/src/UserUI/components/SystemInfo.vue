<template>
  <v-container
    v-if="message"
    fluid
  >
    <v-chip
      class="ma-2"
      :color="type"
      label
      outlined
    >
      {{ message }}
    </v-chip>
  </v-container>
</template>

<script>
let ws = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/chat/system/')
export default {
  name: 'SystemInfo',
  data: () => ({
    message: '',
    type: ''
  }),
  mounted () {
    let Vue = this
    ws.onmessage = function (event) { Vue.message = JSON.parse(event.data).message; Vue.type = JSON.parse(event.data).message_type }
  }
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
