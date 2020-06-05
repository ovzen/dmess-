<template>
  <v-container style="height:100%;">
    <v-row
      class="d-flex flex-column-reverse"
      style="padding-bottom:0px;height:100%;"
      align="end"
    >
      <v-container
        v-for="(message, i) in messages"
        :id="'Message_' + message.id"
        :key="message.id"
        py-2
      >
        <v-card
          v-if="isNewDate(message, messages[i+1])"
          style="border-radius: 15px;width:min-content"
          class="d-inline-flex align-content-center"
          color="background_white"
        >
          <v-card-text
            style="padding: 8px"
          >
            <span
              class="message_color--text message"
            >
              {{ getDay(message.create_date) }}
            </span>
          </v-card-text>
        </v-card>
        <div
          v-if="isOwnMessage(message.user)"
          class="text-left message-hover"
        >
          <v-card
            style="border-radius: 20px;"
            max-width="460px"
            class="d-flex align-content-start flex-wrap flex-shrink-1"
            flat
            min-width="200px"
          >
            <v-container
              class="d-inline-flex align-content-center"
              pb-0
              mb-0
            >
              <v-img
                v-if="message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg'"
                :src="message.image_url"
                max-width="440px"
                min-width="200px"
                @click="dialog=true,link=message.image_url"
              /><file-pond
                v-if="!(message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg') && message.image_url !== '' && message.image_url !== 'False'"
                ref="pond2"
                name="image"
                :disabled="true"
                style="max-width=440px;min-width:400px;border-radius:.5em;"
                :files="[message.image_url]"
                class-name="123"
                :instant-upload="false"
                :allow-download-by-url="true"
                label-idle="Drop files here..."
              />
            </v-container>
            <v-card-text
              style="padding-top: 3px; padding-bottom: 0px"
            >
              <span
                class="message_color--text message"
              >
                {{ decodeEmojiCode(message.text) }}
              </span>
            </v-card-text>
            <v-card-actions style="padding-top: 0px; margin-left: auto">
              <span
                class="float-right overline"
              >
                {{ getTime(message.create_date) }}
              </span>
            </v-card-actions>
          </v-card>
        </div>
        <v-container
          class="d-flex flex-row-reverse"
          py-0
        >
          <div
            v-if="!isOwnMessage(message.user)"
            class="text-left"
          >
            <v-card
              style="border-radius: 20px;"
              max-width="460px"
              class="d-flex align-content-start flex-wrap flex-shrink-1"
              color="background_pink"
              flat
              min-width="200px"
            >
              <v-container
                class="d-inline-flex align-content-center"
                pb-0
                mb-0
              >
                <v-img
                  v-if="message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg'"
                  :src="message.image_url"
                  max-width="440px"
                  min-width="200px"
                  @click="dialog=true,link=message.image_url"
                /><file-pond
                  v-if="!(message.extension === '.png' || message.extension === '.jpeg' || message.extension === '.jpg') && message.image_url !== '' && message.image_url !== 'False'"
                  ref="pond2"
                  name="image"
                  :disabled="true"
                  style="max-width=440px;min-width:400px;border-radius:.5em;"
                  :files="[message.image_url]"
                  class-name="123"
                  :instant-upload="false"
                  :allow-download-by-url="true"
                  label-idle="Drop files here..."
                />
              </v-container>
              <v-card-text
                style="padding-top: 3px; padding-bottom: 0px"
              >
                <div
                  class="d-flex flex-column-reverse"
                >
                  <div class="message-hover">
                    <span
                      class="message_color--text message"
                    >
                      {{ decodeEmojiCode(message.text) }}
                    </span>
                  </div>
                  <div class="menu-hover mt-n7">
                    <div class="rounded-menu d-flex flex-row-reverse">
                      <div class="rounded-menu flex-row-reverse elevation-6">
                        <v-tooltip top>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              icon
                              style="width:23px; height:20px;"
                              v-on="on"
                              @click="messageUpdate(message)"
                            >
                              <v-icon
                                style="font-size:18px;"
                                color="black"
                              >
                                mdi-pencil
                              </v-icon>
                            </v-btn>
                          </template>
                          <span>Edit message</span>
                        </v-tooltip>
                        <v-tooltip top>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              icon
                              style="width:23px; height:20px;"
                              v-on="on"
                              @click="removeId = message.id, removeDialog = true"
                            >
                              <v-icon
                                style="font-size:18px;"
                                color="black"
                              >
                                mdi-delete-forever
                              </v-icon>
                            </v-btn>
                          </template>
                          <span>Delete message</span>
                        </v-tooltip>
                        <v-tooltip top>
                          <template
                            v-slot:activator="{ on }"
                            class="white"
                          >
                            <v-btn
                              icon
                              style="width:23px; height:20px;"
                              v-on="on"
                            >
                              <v-icon
                                style="font-size:18px;"
                                color="black"
                              >
                                mdi-dots-vertical
                              </v-icon>
                            </v-btn>
                          </template>
                          <span>Something more</span>
                        </v-tooltip>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card-text>
              <v-card-actions style="padding-top: 0px; margin-left: auto">
                <span
                  class="float-right overline"
                >
                  {{ getTime(message.create_date) }}
                </span>
              </v-card-actions>
            </v-card>
          </div>
        </v-container>
      </v-container>
      <v-progress-circular
        v-if="messages.length < dialogMessagesLength"
        indeterminate
        size="36"
        style="position: relative; right:50%;margin-top: 25px;margin-bottom: 25px;"
        color="basic"
      />
    </v-row>
    <v-dialog
      v-model="dialog"
      content-class="elevation-0"
    >
      <v-img
        contain
        style="box-shadow: none !important"
        max-height="85vh"
        :src="link"
        @click="dialog=false"
      />
    </v-dialog>
    <v-dialog
      v-model="removeDialog"
      max-width="700"
    >
      <v-card>
        <v-card-title
          class="headline"
        >
          Delete message
        </v-card-title>

        <v-card-text>
          Do you really want to delete this message? <br> This change cannot be undone.
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn
            color="basic"
            text
            @click="removeDialog = false"
          >
            Cancel
          </v-btn>

          <v-btn
            color="red"
            text
            @click="deleteMessage(removeId), removeDialog = false"
          >
            DELETE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: 'MessagesList',
  props: {
    dialogMessagesLength: Number,
    messages: Array,
    getTime: Function,
    deleteMessage: Function,
    messageUpdate: Function,
    decodeEmojiCode: Function,
    isOwnMessage: Function,
    isNewDate: Function,
    getDay: Function
  },
  data: () => ({
    link: '',
    dialog: false,
    removeDialog: false,
    removeId: null
  }),
  mounted () {
    var Data = this
    this.$nextTick(function () {
      Data.$vuetify.goTo(document.getElementById('Message_' + Data.messages[0].id), { duration: 450, offset: 0 })
    })
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

.menu-hover {
  opacity: 0;
  visibility: hidden;
  transition-duration: 0.2s;
}

.menu-hover:hover {
  opacity: 1;
  visibility: visible;
}

.message-hover:hover + .menu-hover {
  opacity: 1;
  visibility: visible;
}
.rounded-menu {
  border-radius: 10px;
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
.composer-popover.active {
  bottom: -100px !important;
  left:200px !important;
}
.filepond--root {
  background-color: #fff;
}
.v-image__image{
  width:100%;
  height:100%;
}
.message {
  font-family: Roboto;
  font-style: normal;
  font-weight: normal;
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
  }
.time-text {
  font-family: Roboto;
  font-style: normal;
  font-weight: 500;
  font-size: 10px;
  letter-spacing: 1.5px;
}

</style>
