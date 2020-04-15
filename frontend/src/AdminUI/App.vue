<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list dense>
        <v-list-item to="/Dashboard/">
          <v-list-item-action>
            <v-icon>mdi-heart</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/UserActivity/">
          <v-list-item-action>
            <v-icon>mdi-heart</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Users</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/DialogActivity/">
          <v-list-item-action>
            <v-icon>mdi-heart</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Invites</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="indigo"
      dark
      scroll-target="#scrolling-techniques-7"
      elevate-on-scroll
    >
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
      />
      <v-toolbar-title>
        Dmess Admin
      </v-toolbar-title>
      <v-spacer />
      <v-menu
        left
        bottom
      >
        <template
          v-slot:activator="{ on }"
        >
          <v-btn
            icon
            v-on="on"
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item>
            <v-tab href="/">
              <v-list-item-content>
                <v-list-item-title>Home</v-list-item-title>
              </v-list-item-content>
            </v-tab>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-sheet
      id="scrolling-techniques-7"
      class="overflow-y-auto"
    >
      <v-content>
        <router-view />
      </v-content>
    </v-sheet>
    <v-footer
      color="indigo"
      app
    >
      <span class="white--text">
        &copy; 2020
      </span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'AdminUI',
  data: () => ({
    drawer: false
  })
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
