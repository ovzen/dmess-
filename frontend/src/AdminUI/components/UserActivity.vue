<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        UserActivity / Зарегистрировавшиеся пользователи
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        />
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="Users"
        :search="search"
        :sort-by="['Username', 'Datetime']"
        :sort-desc="[false, true]"
        multi-sort
        class="elevation-1"
      />
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'UserActivity',
  data: () => ({
    search: '',
    headers: [
      {
        text: 'Username',
        align: 'start',
        value: 'Username'
      },
      { text: 'LastActivity', value: 'LastActivity' }
    ],
    Users: [
      {
        Username: 'petrp',
        LastActivity: '2020-03-11 13:53:19.368414'
      },
      {
        Username: 'Admin',
        LastActivity: '2020-03-7 13:53:19.368414'
      },
      {
        Username: 'Moderator',
        LastActivity: '2020-03-9 13:53:19.368414'
      },
      {
        Username: 'User',
        LastActivity: '2020-03-10 13:53:19.368414'
      }
    ]
  })
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
