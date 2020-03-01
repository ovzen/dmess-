<template>
  <v-app>
    <v-card
    class="mx-auto"
    max-width="500"
  >
    <v-list-item>
      <v-list-item-content>
        <div class="overline mb-4">Ваш профиль</div>
        <v-list-item-title class="headline mb-1 indigo--text">Рест-пользователь</v-list-item-title>
        <v-list-item-subtitle>Статус пользователя: рест-статус</v-list-item-subtitle>
        <v-list-item-subtitle>Дата регистрации: дд.мм.гггг</v-list-item-subtitle>
        <v-list-item-subtitle>Дополнительная информация</v-list-item-subtitle>
      </v-list-item-content>

      <v-list-item-avatar
        size="120"
        color="grey"
      >
        <v-img src="https://images.unsplash.com/photo-1574069498412-60e183438d5d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"></v-img>
      </v-list-item-avatar>
    </v-list-item>

  </v-card>
  </v-app>
</template>

<script>
export default {
  name: 'Profile',
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
