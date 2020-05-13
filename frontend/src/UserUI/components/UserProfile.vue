<template>
  <v-responsive
    class="background_white mx-auto"
    height="100vh"
    max-width="650"
  >
    <v-container>
      <v-list-item
        class="ml-4"
      >
        <v-list-item-avatar
          size="100px"
        >
          <v-avatar
            size="100px"
            color="basic"
          >
            <v-skeleton-loader
              :loading="loading"
              type="avatar"
              class="mx-auto"
            >
              <span
                class="display-1 white--text"
              >
                NU
              </span>
              <v-skeleton-loader />
              <!--<v-img
              src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
            />-->
            </v-skeleton-loader>
          </v-avatar>
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
            @click=""
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
            @click=""
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
export default {
  name: 'UserProfile',
  data: () => ({
    loading: true,
    UserProfile: undefined
  }),
  watch: {
    // при изменениях маршрута запрашиваем данные снова
    $route: ['get_data']
  },
  created () {
    this.get_data()
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
