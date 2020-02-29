<template>
  <v-app>
    <v-app>
      <div>
        <v-app-bar
          :collapse-on-scroll="true"
          absolute
          dark
          scroll-target="#scrolling-techniques-6"
        >
          <v-app-bar-nav-icon @click="drawer = true" />
          <v-toolbar-title>Навигация</v-toolbar-title>
          <v-spacer />
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-app-bar>

        <v-navigation-drawer
          v-model="drawer"
          absolute
          temporary
        >
          <v-row no-gutters>
            <v-navigation-drawer
              v-model="drawer"
              dark
              mini-variant
              mini-variant-width="58px"
              absolute
            >
              <v-list>
                <v-list-item>
                  <v-list-item-action>
                    <v-icon>mdi-chat</v-icon>
                  </v-list-item-action>
                </v-list-item>
                <v-divider />
                <v-list-item>
                  <v-list-item-avatar>
                    <v-img src="https://www.technistone.com/color-range/image-slab/deska_gobi_black_p.jpg" />
                  </v-list-item-avatar>
                </v-list-item>
                <v-list-item>
                  <v-list-item-avatar>
                    <v-img src="https://www.technistone.com/color-range/image-slab/deska_gobi_black_p.jpg" />
                  </v-list-item-avatar>
                </v-list-item>
              </v-list>
            </v-navigation-drawer>
            <v-list
              class="pa-9"
              nav
              dense
              style="padding-right: 0px !important;padding-left: 58px !important;"
            >
              <v-list-item-group
                v-model="group"
              >
                <v-list-item class="grow">
                  <v-list-item-icon>
                    <v-icon>mdi-chat</v-icon>
                  </v-list-item-icon>
                  <v-list-item-text>Другой диалог</v-list-item-text>
                </v-list-item>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-chat</v-icon>
                  </v-list-item-icon>
                  <v-list-item-text>Другой диалог</v-list-item-text>
                </v-list-item>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-chat</v-icon>
                  </v-list-item-icon>
                  <v-list-item-text>Другой диалог</v-list-item-text>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-row>
        </v-navigation-drawer>
        <v-sheet
          id="scrolling-techniques-6"
          class="overflow-y-auto"
          max-height="100vh"
        >
          <router-view style="height:2000px; margin-top:64px" />
        </v-sheet>
      </div>
    </v-app>
  </v-app>
</template>

<script>
export default {
  name: 'Skeleton',
  data: () => ({
    login: '',
    button: 'Войти',
    password: '',
    message_text: '',
    data: '',
    messages: [],
    dialog: false,
    id: 0,
    drawer: false
  })
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
  height: 100vh;
}
</style>
