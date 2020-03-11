<template>
  <v-app>
    <v-app-bar
      app
      color="white"
      scroll-target="#scrolling-techniques-7"
      elevate-on-scroll
    >
      <v-toolbar-title style="min-width:100px">
        AdminUI
      </v-toolbar-title>
      <v-tabs>
        <v-tab to="/UserActivity/">
          Активность пользователей
        </v-tab>
        <v-tab to="/DialogActivity/">
          Активность в чатах
        </v-tab>
      </v-tabs>
      <v-spacer />
      <v-btn href="/" replace>UserUI</v-btn>
    </v-app-bar>
    <v-sheet
      id="scrolling-techniques-7"
      class="overflow-y-auto"
      max-height="100vh"
    >
      <v-content>
        <router-view />
      </v-content>
    </v-sheet>
  </v-app>
</template>

<script>
export default {
  name: 'AdminUI',
  data: () => ({
  })
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
