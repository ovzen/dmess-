<template>
  <v-app>
    <v-app-bar
      app
      :value="!(AlwaysOnDisplay || ExpandOnHover)"
      collapse-on-scroll
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
      :app="AlwaysOnDisplay"
      :expand-on-hover="ExpandOnHover"
      :temporary="!(AlwaysOnDisplay || ExpandOnHover)"
    >
      <v-row no-gutters>
        <v-navigation-drawer
          v-model="drawer"
          dark
          :app="ExpandOnHover"
          mini-variant
          mini-variant-width="56px"
          absolute
        >
          <v-list>
            <v-list-item>
              <v-list-item-action>
                <v-icon>mdi-chat</v-icon>
              </v-list-item-action>
            </v-list-item>
            <v-list-item>
              <v-list-item-action>
                <v-icon>mdi-settings</v-icon>
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
        <div style="position: absolute; top: 80%;">
          <v-switch
            v-model="AlwaysOnDisplay"
            label="Постоянное отображение меню"
            style="padding-right: 0px !important;padding-left: 58px !important;"
            :disabled="ExpandOnHover"
          />
          <v-switch
            v-model="ExpandOnHover"
            label="Мини версия меню"
            style="padding-right: 0px !important;padding-left: 58px !important;"
            :disabled="AlwaysOnDisplay"
          />
        </div>
      </v-row>
    </v-navigation-drawer>
    <v-sheet
      id="scrolling-techniques-6"
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
  name: 'App',
  data: () => ({
    login: '',
    button: 'Войти',
    password: '',
    message_text: '',
    data: '',
    messages: [],
    dialog: false,
    id: 0,
    drawer: false,
    AlwaysOnDisplay: false,
    ExpandOnHover: false,
    group: []
  })
}
</script>

<style lang="scss">
#app {
  color: #2c3e50;
  height: 100vh;
}
</style>
