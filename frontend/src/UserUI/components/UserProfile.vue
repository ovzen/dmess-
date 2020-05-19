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
              v-if="UserProfile.profile.avatar"
              size="100px"
            >
              <v-img
                :src="UserProfile.profile.avatar"
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
                {{ getUserAvatar }}
              </span>
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
              {{ UserProfile.username }}
            </v-list-item-title>
            <v-list-item-subtitle>
              <span
                class="basic--text text--lighten"
              >
                {{ ( UserProfile.profile.is_online == true ? 'В сети' : 'Не в сети' ) }}
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
          class="pt-5 overline basic--text"
        >
          BIO
        </div>
        <v-skeleton-loader
          v-if="loading"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%;"
        />
        <div
          v-else
          class="body-2 black--text"
        >
          {{ UserProfile.profile.bio }}
        </div>

        <v-divider
          v-if="!loading"
          width="538"
          class="mb-2"
        />

        <div
          class="pt-2 overline basic--text"
          style="margin-top:10px"
        >
          USERNAME
        </div>
        <v-skeleton-loader
          v-if="loading"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%"
        />
        <div
          v-else
          class="body-2 black--text"
        >
          {{ UserProfile.username }}
        </div>
        <v-divider
          v-if="!loading"
          width="538"
          class="mb-1"
        />

        <div
          class="pt-4 overline basic--text"
        >
          EMAIL
        </div>
        <v-skeleton-loader
          v-if="loading"
          type="text"
          class="mx-auto"
          style="width:75%;position:absolute;left:10%"
        />
        <div
          v-else
          class="body-2 black--text"
        >
          {{ UserProfile.email || 'Эл. почта не указана' }}
        </div>
        <v-divider
          v-if="!loading"
          width="538"
        />
      </v-card-text>
      <v-card-actions>
        <v-card-text
          class="mt-12"
        >
          <v-list-item
            @click="add_contact()"
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
import jwt from 'jsonwebtoken'
export default {
  name: 'UserProfile',
  data: () => ({
    loading: true,
    UserProfile: undefined,
    current_user_id: undefined
  }),
  computed: {
    getUserAvatar () {
      if (typeof this.UserProfile !== 'undefined') {
        if (this.UserProfile.first_name !== '' && this.UserProfile.last_name !== '') {
          return (this.UserProfile.first_name[0] + this.UserProfile.last_name[0]).toUpperCase()
        } else {
          return this.UserProfile.username[0].toUpperCase()
        }
      } return ''
    }
  },
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['get_data']
  },
  created () {
    this.get_data()
    if (this.$cookie.get('Authentication')) {
      this.current_user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  methods: {
    get_data () {
      this.loading = true
      api.axios
        .get('/api/users/' + this.$route.params.Userid + '/')
        .then(res => {
          this.UserProfile = res.data
          this.loading = false
        })
        .catch(error => {
          alert(error)
        })
    },
    add_contact () {
      api.axios.post('/api/contacts/', {
        user: jwt.decode(this.$cookie.get('Authentication')).user_id,
        contact: this.$route.params.Userid
      }).then(res => {
        if (res.status === 201) {
          this.$root.$children[0].getContacts()
          this.$root.$children[0].findedUsers = this.$root.$children[0].findedUsers.filter(user => {
            console.log(user.id, ' ', this.$route.params.Userid)
            if (user.id === parseInt(this.$route.params.Userid)) {
              return false
            }
            return true
          })
          this.$root.$children[0].$forceUpdate()
        }
      })
    },
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
                users: [this.current_user_id, this.$route.params.Userid]
              })
              .then(response => {
                if (response && response.data && response.data.id) {
                  this.$router.push('/ChatUser/' + response.data.id)
                }
              })
          }
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
</style>
