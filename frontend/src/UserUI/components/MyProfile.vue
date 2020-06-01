<template>
  <v-responsive
    class="background_white mx-auto"
    height="100%"
    max-width="650"
  >
    <v-container>
      <v-list-item
        class="ml-4"
      >
        <v-list-item-avatar
          size="100px"
        >
          <v-skeleton-loader
            v-if="loading"
            type="avatar"
            class="mx-auto"
          />
          <div v-else>
            <v-avatar
              size="100px"
              :color="( edit ? 'background_grey' : 'basic_text')"
            >
              <span
                v-if="!edit && !UserProfile.profile.avatar"
                class="display-1 white--text"
              >
                {{ getUserInitials }}
              </span>

              <v-img
                v-if="!edit && UserProfile.profile.avatar"
                :src="UserProfile.profile.avatar"
              />
              <v-img
                v-if="edit && UserProfile.profile.avatar"
                :src="UserProfile.profile.avatar"
                style="opacity: 0.3"
              />
              <v-btn
                v-if="edit"
                icon
                dark
                absolute
                style="left:50%;top:50%;transform: translate(-50%, -50%);"
                @click="runFileSelect"
              >
                <v-icon large>
                  mdi-camera-outline
                </v-icon>
              </v-btn>
              <input
                ref="file"
                type="file"
                style="display:none"
                @change="onFileSelected"
              >
            </v-avatar>
          </div>
        </v-list-item-avatar>
        <v-list-item-content
          class="ml-4"
        >
          <v-skeleton-loader
            v-if="loading"
            type="list-item-two-line"
            class="mx-auto"
          />
          <div v-else>
            <v-list-item-title
              class="headline"
            >
              <div
                class="overline basic_text--text"
              >
                Name
              </div>
              <v-skeleton-loader
                v-if="loading"
                type="text"
                class="mx-auto"
                style="width:75%;position:absolute;left:10%;"
              />
              <div v-else>
                <div
                  v-if="!edit"
                  class="body-2 black--text"
                >
                  {{ UserProfile.first_name || "Не указано" }}
                </div>
                <v-text-field
                  v-else
                  v-model="UserProfile.first_name"
                  style="width:90.6%;margin-top:-20px;margin-bottom:-20px;"
                  color="basic"
                />
              </div>
              <v-divider
                v-if="!loading && !edit"
                width="404"
              />
            </v-list-item-title>

            <v-list-item-subtitle>
              <div
                class="pt-2 overline basic_text--text"
              >
                Surname
              </div>
              <v-skeleton-loader
                v-if="loading"
                type="text"
                class="mx-auto"
                style="width:75%;position:absolute;left:10%;"
              />
              <div v-else>
                <div
                  v-if="!edit"
                  class="body-2 black--text"
                >
                  {{ UserProfile.last_name || "Не указано" }}
                </div>
                <v-text-field
                  v-else
                  v-model="UserProfile.last_name"
                  style="width:90.6%;margin-top:-20px;margin-bottom:-20px;"
                  color="basic"
                />
              </div>
              <v-divider
                v-if="!loading && !edit"
                width="404"
              />
            </v-list-item-subtitle>
          </div>
        </v-list-item-content>
      </v-list-item>
      <v-card-text
        class="ml-9"
      >
        <div
          class="pt-5 overline basic_text--text"
        >
          BIO
        </div>
        <v-skeleton-loader
          v-if="loading"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%;"
        />
        <div v-else>
          <div
            v-if="!edit"
            class="body-2 black--text"
          >
            {{ UserProfile.profile.bio }}
          </div>
          <v-text-field
            v-else
            v-model="UserProfile.profile.bio"
            style="width:90.6%;margin-top:-20px;margin-bottom:-20px;"
            color="basic"
          />
        </div>

        <v-divider
          v-if="!loading && !edit"
          width="538"
          class="mb-2"
        />

        <div
          class="pt-2 overline basic_text--text"
          style="margin-top:10px"
        >
          USERNAME
        </div>
        <v-skeleton-loader
          v-if="loading"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%;"
        />
        <div v-else>
          <div
            v-if="!edit"
            class="body-2 black--text"
          >
            {{ UserProfile.username }}
          </div>
          <v-text-field
            v-else
            v-model="UserProfile.username"
            style="width:90.6%;margin-top:-20px;margin-bottom:-20px"
            color="basic"
          />
        </div>
        <v-divider
          v-if="!loading && !edit"
          width="538"
          class="mb-1"
        />

        <div
          class="pt-4 overline basic_text--text"
        >
          EMAIL
        </div>
        <v-skeleton-loader
          v-if="loading"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%;"
        />
        <div v-else>
          <div
            v-if="!edit"
            class="body-2 black--text"
          >
            {{ UserProfile.email || 'Эл. почта не указана' }}
          </div>
          <v-text-field
            v-else
            v-model="UserProfile.email"
            style="width:90.6%;margin-top:-20px;margin-bottom:-20px"
            color="basic"
          />
        </div>
        <v-divider
          v-if="!loading && !edit"
          width="538"
        />
      </v-card-text>
      <v-card-actions>
        <v-card-text
          class="mt-12"
        >
          <v-list-item
            v-if="!edit"
            @click="edit=!edit"
          >
            <v-list-item-action>
              <v-icon
                class="ml-3 pb-4"
                color="basic"
              >
                mdi-lead-pencil
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-4 body-1 black--text"
              >
                Edit profile
              </v-list-item-title>
              <v-divider
                width="538"
              />
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-if="edit"
            @click="save(), edit=!edit"
          >
            <v-list-item-action>
              <v-icon
                class="ml-3 pb-4"
                color="basic"
              >
                mdi-lead-pencil
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-4 body-1 black--text"
              >
                Save changes
              </v-list-item-title>
              <v-divider
                width="538"
              />
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            @click="exit()"
          >
            <v-list-item-action>
              <v-icon
                class="ml-3 pb-6"
                color="red"
              >
                mdi-login-variant
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-6 body-1 red--text"
              >
                Logout
              </v-list-item-title>
              <v-divider
                width="550"
              />
            </v-list-item-content>
          </v-list-item>
        </v-card-text>
      </v-card-actions>
    </v-container>
  </v-responsive>
</template>

<script>
import VueCookie from 'vue-cookie'
import Vue from 'vue'
import api from '../api'
import jwt from 'jsonwebtoken'
Vue.use(VueCookie)
export default {
  name: 'MyProfile',
  data: () => ({
    user_id: undefined,
    UserProfile: undefined,
    loading: true,
    edit: false
  }),
  computed: {
    getUserInitials () {
      if (typeof this.UserProfile !== 'undefined') {
        if (this.UserProfile.first_name !== '' && this.UserProfile.last_name !== '') {
          return (this.UserProfile.first_name[0] + this.UserProfile.last_name[0]).toUpperCase()
        } else {
          return this.UserProfile.username[0].toUpperCase()
        }
      } return ''
    }
  },
  created () {
    this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    this.get_data()
  },
  methods: {
    get_data () {
      this.loading = true
      api.axios
        .get('/api/users/' + this.user_id + '/')
        .then(res => {
          this.UserProfile = res.data
          this.loading = false
        })
        .catch(error => {
          alert(error)
        })
    },
    save () {
      let formData = new FormData()

      formData.append('first_name', this.UserProfile.first_name)
      formData.append('last_name', this.UserProfile.last_name)
      formData.append('username', this.UserProfile.username)
      formData.append('email', this.UserProfile.email)
      formData.append('profile.bio', this.UserProfile.profile.bio)
      // если не отправить статус, то появляется ошибка "this field is required"
      formData.append('profile.status', 'online')
      if (this.UserProfile.avatar) {
        formData.append('profile.avatar', this.UserProfile.avatar)
      }

      api.axios
        .put('/api/accounts/profile/', formData)
        .then(res => {
          console.log(res)
          if (res.status === 200) {
            this.get_data()
          }
        })
        .catch(error => {
          alert(error)
        })
    },
    exit () {
      localStorage.removeItem('UpdateKey')
      this.$cookie.delete('Authentication')
      window.location.reload()
    },
    runFileSelect () {
      this.$refs.file.click()
    },
    onFileSelected () {
      this.UserProfile.avatar = this.$refs.file.files[0]
      console.log('avatar: ', this.UserProfile.avatar)
    }

  }
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
.label {
color: #6202EE;
}
</style>
