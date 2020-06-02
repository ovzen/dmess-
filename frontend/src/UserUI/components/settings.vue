<template>
  <div>
    <v-divider />
    <v-col>
      <p
        class="basic_text--text font-weight-medium pa-2"
        style="font-family: Roboto;
              font-size: 18px !important;
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
    <v-list-item>
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
          Dark Theme [BETA]
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
    dialogsWarnings: false,
    userId: undefined,
    userIsStaff: false
  }),
  created () {
    this.userId = jwt.decode(this.$cookie.get('Authentication')).user_id
    this.getUserStaff()
  },
  methods: {
    saveTheme () {
      console.log(this.$vuetify.theme.dark)
      localStorage.setItem('Dark', this.$vuetify.theme.dark);
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
