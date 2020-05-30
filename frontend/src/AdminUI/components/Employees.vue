<template>
  <div style="height:100%;width:100%">
    <v-card-title>
      Employees
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
      :loading="loading"
      loading-text="Загрузка... Пожалуйста подождите / Loading... Please wait"
      :headers="headers"
      :page.sync="page"
      :items-per-page="5"
      :items="Users"
      style="height:69%"
      :search="search"
      :sort-desc="[false, true]"
      multi-sort
      hide-default-footer
      @page-count="pageCount = $event"
    />
    <v-pagination
      v-model="page"
      :length="pageCount"
    />
  </div>
</template>

<script>
import api from '../api'
export default {
  name: 'Employees',
  data: () => ({
    search: '',
    loading: true,
    headers: [
      {
        text: 'ID',
        value: 'id'
      },
      { text: 'Имя пользователя / Username', value: 'username' },
      { text: 'Имя / First name', value: 'first_name' },
      { text: 'Фамилия / Last name', value: 'last_name' },
      { text: 'Статус / Status', value: 'profile.status', sortable: false }
    ],
    Users: [],
    page: 1,
    pageCount: 0
  }),
  mounted () {
    this.update()
  },
  methods: {
    update () {
      api.axios.get('/api/users/').then(res => {
        this.Users = res.data.results.filter(user => user.is_staff === true)
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.v-card {
  margin:20px
}
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
