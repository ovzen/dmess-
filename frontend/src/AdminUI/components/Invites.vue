<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Invites / Приглашения
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        />
        <v-btn
          style="margin-left:20px"
          color="success"
          small
          @click="Create()"
        >
          Создать приглашение
        </v-btn>
      </v-card-title>
      <v-data-table
        :loading="loading"
        loading-text="Загрузка... Пожалуйста подождите / Loading... Please wait"
        :headers="headers"
        :items="Invites"
        :search="search"
        :sort-desc="[false, true]"
        multi-sort
        class="elevation-1"
      >
        <template v-slot:item.is_active="{ item }">
          <v-checkbox
            v-model="item.is_active"
            @click.stop="Edit(item)"
          />
        </template>
        <template v-slot:item.for_user="{ item }">
          {{ item.for_user || 'Не использовано' }}
        </template>
        <template v-slot:item.used_at="{ item }">
          {{ item.used_at || 'Не использовано' }}
        </template>
        <template v-slot:item.reg_btn="{ item }">
          <v-btn
            color="primary"
            small
            @click="CopyLink(item)"
          >
            Получить ссылку
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import api from '../api'
export default {
  name: 'Invites',
  data: () => ({
    search: '',
    loading: true,
    headers: [
      {
        text: 'Код / Code',
        value: 'code'
      },
      { text: 'Дата создания / Created at', value: 'created_at' },
      { text: 'Активно / Is active', value: 'is_active' },
      { text: 'Кем использовано / For user', value: 'for_user' },
      { text: 'Время использования / Used at', value: 'used_at' },
      { text: 'Получить ссылку / Copy Link for registration', value: 'reg_btn', align: 'center' }
    ],
    Invites: [
    ]
  }),
  mounted () {
    this.update()
  },
  methods: {
    update () {
      api.axios.get('/api/admin/invites/').then(res => {
        this.Invites = res.data
        this.loading = false
      })
    },
    Create () {
      api.axios.post('/api/admin/invites/').catch(res => {
        alert('Ошибка')
      }).then(
        this.loading = true,
        setTimeout(this.update(), 1000)
      )
    },
    Edit (item) {
      api.axios.put('/api/admin/invites/' + item.code + '/', { is_active: !item.is_active }).catch(res => {
        alert('Ошибка')
      }).then(
        item.is_active = !item.is_active
      )
    },
    CopyLink (item) {
      navigator.clipboard.writeText(window.location.host + '/auth/register/' + item.code + '/')
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
