<template>
  <div>
    <v-container>
      <div
        class="text-left"
      >
        <v-card
          max-width="460px"
          class="float-right d-flex"
          style="border-radius: 20px;"
          flat
        >
          <v-card-text>
            <span
              class="font-weight-light message_color--text"
            >
              Text message
            </span>
            <span
              class="float-right ml-2"
            >
              18:00
            </span>
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
            style="border-radius: 20px;"
            max-width="460px"
            class="d-flex"
            color="background_pink"
            flat
          >
            <v-card-text>
              <span
                class="font-weight-light message_color--text"
              >
                Text message
              </span>
              <span
                class="float-right ml-2"
              >
                18:00
              </span>
            </v-card-text>
          </v-card>
        </div>
      </v-container>
    </v-container>
    <ChatInput />
  </div>
</template>

<script>
import ChatInput from './ChatInput'
export default {
  name: 'ChatUser',
  components: { ChatInput },
  data: () => ({
  })
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
.text{
  font-style: normal;
  font-weight: bolder;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
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
  position: relative;
}
</style>
