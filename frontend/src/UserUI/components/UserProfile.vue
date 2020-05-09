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
            <span
              class="display-1 white--text"
            >
              NU
            </span>
            <!--<v-img
              src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
            />-->
          </v-avatar>
        </v-list-item-avatar>

        <v-list-item-content
          class="ml-4"
        >
          <v-list-item-title
            class="headline"
          >
            Name User
          </v-list-item-title>
          <v-list-item-subtitle>
            <span
              class="basic--text text--lighten"
            >
              online
            </span>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider
        class="ml-8"
        width="555"
      />

      <v-card-text
        class="ml-7 mt-4"
      >
        <div
          class="pt-5 overline basic--text"
        >
          BIO
        </div>
        <div
          class="body-2 black--text"
        >
          text bio
        </div>
        <v-divider
          width="538"
        />

        <div
          class="pt-2 overline basic--text"
        >
          USERNAME
        </div>
        <div
          class="body-2 black--text"
        >
          Name_USER
        </div>
        <v-divider
          width="538"
        />

        <div
          class="pt-2 overline basic--text"
        >
          EMAIL
        </div>
        <div
          class="body-2 black--text"
        >
          name@mail.ru
        </div>
        <v-divider
          width="538"
        />
      </v-card-text>
      <v-card-actions>
        <v-card-text
          class="mt-12"
        >
          <v-list-item>
            <v-list-item-action>
              <v-icon
                class="pb-4"
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

          <v-list-item>
            <v-list-item-action>
              <v-icon
                class="pb-4"
                color="basic"
              >
                mdi-message-text-outline
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title
                class="pb-4 body-1 black--text"
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
export default {
  name: 'UserProfile',
  data: () => ({
  })
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
