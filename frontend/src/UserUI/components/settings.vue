<template>
  <div>
    <v-divider />
    <v-col>
      <p
        class="basic_text--text font-weight-medium pa-2"
        style="font-size: 18px !important;
              line-height: 16px;
              font-style: normal;
              font-weight: normal;
              margin-bottom:-3px"
      >
        Settings
      </p>
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
    <v-tooltip top>
      <template v-slot:activator="{ on }">
        <v-list-item v-on="on">
          <v-switch
            v-model="$vuetify.theme.dark"
            class="pb-2"
            color="basic"
            @change="saveTheme()"
          />
          <v-list-item-content>
            <v-list-item-title
              class="pl-7 pb-2"
            >
              Dark Theme
            </v-list-item-title>
            <v-divider
              class="ml-7"
            />
          </v-list-item-content>
        </v-list-item>
      </template>
      <span>Click here to go in dark theme or use ALT+S</span>
    </v-tooltip>

    <v-dialog
      v-model="colorPicker"
      hide-overlay
      content-class="elevation-0"
    >
      <template v-slot:activator="{ on }">
        <v-list-item v-on="on">
          <v-icon
            class="pb-2"
            color="basic"
          >
            mdi-palette
          </v-icon>
          <v-list-item-content>
            <v-list-item-title
              class="pl-7 pb-2"
            >
              Select or write your's favorite color in hex
            </v-list-item-title>
            <v-divider
              class="ml-7"
            />
          </v-list-item-content>
        </v-list-item>
      </template>
      <v-card
        :style="'position:fixed;' + 'left:' + (this.$vuetify.application.left/2-150) + 'px'"
        max-width="300px"
      >
        <v-color-picker
          v-model="color"
          mode="hexa"
          style="margin:0px"
          @input="setColor()"
        />
        <v-btn
          block
          color="basic"
          dark
          @click="resetColor()"
        >
          Reset to defaults
        </v-btn>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="dialogsWarnings"
      width="630px"
    >
      <v-card>
        <v-card-title
          class="headline textShineBlack font-weight-bold"
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
      v-if="userIsStaff"
      @click.stop="dialogsWarnings = true"
    >
      <v-icon
        class="pb-2 textShineBlack"
      >
        mdi-account-supervisor
      </v-icon>
      <v-list-item-content>
        <v-list-item-title
          class="pl-7 pb-2 textShineBlack font-weight-bold"
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
import api from '../api'
import jwt from 'jsonwebtoken'
export default {
  name: 'Settings',
  data: () => ({
    colorPicker: false,
    dialogsWarnings: false,
    userId: undefined,
    userIsStaff: false,
    color: '',
    items: [
      '#66CCFF',
      '#DA7',
      '#77AAB'
    ]
  }),
  created () {
    this.userId = jwt.decode(this.$cookie.get('Authentication')).user_id
    this.getUserStaff()
  },
  mounted () {
    if (localStorage.getItem('customColor') !== null) {
      this.color = localStorage.getItem('customColor')
    } else {
      if (!this.$vuetify.theme.dark) { this.color = '#6202ee' } else { this.color = '#D7B7FD' }
    }
  },
  methods: {
    setColor () {
      this.$vuetify.theme.themes.dark.basic = this.color
      this.$vuetify.theme.themes.light.basic = this.color
      this.$vuetify.theme.themes.dark.basic_text = this.color
      this.$vuetify.theme.themes.light.basic_text = this.color
      this.$vuetify.theme.themes.light.background_user = this.color
      this.$vuetify.theme.themes.dark.primary = this.color
      clearTimeout(this._timerId)
      this._timerId = setTimeout(() => { localStorage.setItem('customColor', this.color) }, 500)
    },
    resetColor () {
      this.colorPicker = false
      this.$vuetify.theme.themes.dark.basic = '#D7B7FD'
      this.$vuetify.theme.themes.light.basic = '#6202EE'
      this.$vuetify.theme.themes.dark.basic_text = '#D7B7FD'
      this.$vuetify.theme.themes.light.basic_text = '#6202EE'
      this.$vuetify.theme.themes.light.background_user = '#6202EE'
      this.$vuetify.theme.themes.dark.primary = '#6202EE'
      localStorage.removeItem('customColor')
    },
    saveTheme () {
      localStorage.setItem('Dark', this.$vuetify.theme.dark)
    },
    getUserStaff  () {
      this.loading = true
      api.axios
        .get('/api/users/' + this.userId + '/')
        .then(res => {
          if (res.data) {
            this.userIsStaff = res.data.is_staff
            console.log('userIsStaff', res.data.is_staff)
          }
        })
        .catch(error => {
          alert(error)
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
.textShineBlack {
  background: linear-gradient(to right, #C3005E 20%, #BB86FC 30%, #C3005E 70%, #BB86FC 80%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-fill-color: transparent;
  background-size: 300% auto;
  animation: textShine 7s ease-in-out infinite alternate;
}
@keyframes textShine {
  to {
    background-position: 100%;
  }
}
</style>
