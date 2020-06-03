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
            v-if="checkThatUser"
            type="avatar"
            class="mx-auto"
          />
          <div v-else>
            <v-avatar
              v-if="getThatUser.profile.avatar"
              size="100px"
            >
              <v-img
                :src="getThatUser.profile.avatar"
              />
            </v-avatar>
            <v-avatar
              v-else
              size="100px"
              color="basic"
            >
              <span
                class="display-1 white--text"
              >
                {{ MakeAvatar }}
              </span>
            </v-avatar>
          </div>
        </v-list-item-avatar>
        <v-list-item-content
          class="ml-4"
        >
          <v-skeleton-loader
            v-if="checkThatUser"
            type="list-item-two-line"
            class="mx-auto"
          />
          <div v-else>
            <v-list-item-title
              class="headline"
            >
              {{ getUserName(getThatUser) }}
            </v-list-item-title>
            <v-list-item-subtitle>
              <span
                :class="(getThatUser.profile.status === 'online' ? 'basic_text--text text--lighten' : 'text_second--text')"
              >
                {{ getThatUser.profile.status }}
              </span>
            </v-list-item-subtitle>
          </div>
        </v-list-item-content>
      </v-list-item>
      <v-divider
        class="ml-8"
        width="555"
      />

      <v-card-text
        class="ml-9 mt-4"
      >
        <div
          class="pt-5 overline basic_text--text"
        >
          BIO
        </div>
        <v-skeleton-loader
          v-if="checkThatUser"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%;"
        />
        <div
          v-else
          class="body-2 black--text"
        >
          {{ getThatUser.profile.bio }}
        </div>

        <v-divider
          v-if="!checkThatUser"
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
          v-if="checkThatUser"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%"
        />
        <div
          v-else
          class="body-2 black--text"
        >
          {{ getThatUser.username }}
        </div>
        <v-divider
          v-if="!checkThatUser"
          width="538"
          class="mb-1"
        />

        <div
          class="pt-4 overline basic_text--text"
        >
          EMAIL
        </div>
        <v-skeleton-loader
          v-if="checkThatUser"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%"
        />
        <div
          v-else
          class="body-2 black--text"
        >
          {{ getThatUser.email || 'Эл. почта не указана' }}
        </div>
        <v-divider
          v-if="!checkThatUser"
          width="538"
        />
      </v-card-text>
      <v-card-actions>
        <v-card-text
          class="mt-12"
        >
          <v-list-item
            v-if="typeof getThatUser.is_contact === 'undefined'"
            @click="add_Сontact($route.params.Userid)"
          >
            <v-list-item-action>
              <v-icon
                class="ml-3 pb-4"
                color="basic"
              >
                mdi-plus
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-4 body-1 black--text"
              >
                Add to contact list
              </v-list-item-title>
              <v-divider
                width="538"
              />
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            v-else
            @click="remove_Сontact($route.params.Userid)"
          >
            <v-list-item-action>
              <v-icon
                class="ml-3 pb-4"
                color="red"
              >
                mdi-minus
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-4 body-1 black--text"
              >
                Remove from contact list
              </v-list-item-title>
              <v-divider
                width="538"
              />
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            @click="findChat()"
          >
            <v-list-item-action>
              <v-icon
                class="ml-3 pb-6"
                color="basic"
              >
                mdi-message-text-outline
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-6 body-1 black--text"
              >
                Start messaging
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
import api from '../api'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'UserProfile',
  data: () => ({
  }),
  computed: {
    ...mapGetters(['getUserById', 'checkUserById', 'getUserId']),
    getThatUser () {
      return this.getUserById(this.$route.params.Userid)
    },
    checkThatUser () {
      return !this.checkUserById(this.$route.params.Userid)
    },
    MakeAvatar () {
      if (typeof this.getThatUser !== 'undefined') {
        if (this.getThatUser.first_name !== '' && this.getThatUser.last_name !== '') {
          return this.getThatUser.first_name[0] + this.getThatUser.last_name[0]
        }
        if (this.getThatUser.first_name !== '') {
          return this.getThatUser.first_name[0]
        }
        if (this.getThatUser.last_name !== '') {
          return this.getThatUser.last_name[0]
        }
        if (this.getThatUser.username !== '') {
          return this.getThatUser.username[0]
        }
      }
      return '...'
    }
  },
  created () {
    if (this.checkThatUser) {
      this.getUserData(this.$route.params.Userid)
    }
  },
  methods: {
    ...mapActions(['getUserData', 'add_Сontact', 'remove_Сontact']),
    findChat () {
      api.axios
        .get('/api/dialog/', {
          params: {
            users: this.$route.params.Userid
          }
        })
        .then(response => {
          if (response.data.results.length > 0) {
            this.$router.push('/ChatUser/' + response.data.results[0].id)
          } else {
            api.axios
              .post('/api/dialog/', {
                users: [this.getUserId, this.$route.params.Userid]
              })
              .then(response => {
                if (response && response.data && response.data.id) {
                  this.$router.push('/ChatUser/' + response.data.id)
                }
              })
          }
        })
    },
    getUserName (user) {
      if (typeof user !== 'undefined') {
        if (user.first_name && user.last_name) {
          return (user.first_name + ' ' + user.last_name)
        } else if (user.first_name) {
          return user.first_name
        } else if (user.last_name) {
          return user.last_name
        } else {
          return user.username
        }
      }
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
