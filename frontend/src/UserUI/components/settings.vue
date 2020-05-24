<template>
  <div>
    <v-divider />
    <v-col>
      <a class="basic--text">
        <u>
          SETTINGS
        </u>
      </a>
    </v-col>
    <v-list-item
      to="/MyProfile"
    >
      <v-icon
        class="pb-2"
        color="basic"
      >
        mdi-account-circle-outline
      </v-icon>
      <v-list-item-content>
        <v-list-item-title
          class="pl-7 pb-2"
        >
          Profile
        </v-list-item-title>
        <v-divider
          class="ml-7"
        />
      </v-list-item-content>
    </v-list-item>
    <v-dialog
      v-model="dialogsWarnings"
      width="630px"
    >
      <v-card>
        <v-card-title
          class="headline textShineBlack"
        >
          You are leaving the client app and go the admin panel!
        </v-card-title>

        <v-card-actions>
          <v-spacer />
          <v-btn
            color="basic"
            text
            href="/admin/"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-list-item
      @click.stop="dialogsWarnings = true"
    >
      <v-icon
        class="pb-2 textShineBlack"
      >
        mdi-account-supervisor
      </v-icon>
      <v-list-item-content>
        <v-list-item-title
          class="pl-7 pb-2 textShineBlack"
        >
          The Dark Admin Side
        </v-list-item-title>
        <v-divider
          class="ml-7"
        />
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data: () => ({
    dialogsWarnings: false
  })
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
.textShineBlack {
  background: linear-gradient(to right, #000 20%, #c31678 30%, #6202ee 70%, #000 80%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-fill-color: transparent;
  background-size: 300% auto;
  animation: textShine 7s ease-in-out infinite alternate;
}
@keyframes textShine {
  to {
    background-position: 300%;
  }
}
</style>
