<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        DialogActivity / Просмотр активности диалогов
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
        :items="Dialogs"
        :search="search"
        :sort-by="['Dialog Name', 'url', 'Date Time']"
        :sort-desc="[false, true]"
        multi-sort
        class="elevation-1"
      />
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'DialogActivity',
  data: () => ({
    search: '',
    headers: [
      {
        text: 'Dialog Name',
        align: 'start',
        value: 'DialogName'
      },
      { text: 'url', value: 'url' },
      { text: 'Date Time', value: 'DateTime' }
    ],
    Dialogs: [
      {
        DialogName: 'somechat1',
        DateTime: '2020-03-11 13:53:19.368414',
        url: '/somechat1/'
      },
      {
        DialogName: 'somechat2',
        DateTime: '2020-03-7 13:53:19.368414',
        url: '/somechat2/'
      },
      {
        DialogName: 'somechat3',
        DateTime: '2020-03-9 13:53:19.368414',
        url: '/somechat3/'
      },
      {
        DialogName: 'somechat4',
        DateTime: '2020-03-10 13:53:19.368414',
        url: '/somechat4/'
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