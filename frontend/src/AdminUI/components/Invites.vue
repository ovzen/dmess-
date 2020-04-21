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
        <template v-slot:item.created_at="{ item }">
          {{ DecodeTime(item.created_at) }}
        </template>
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
          {{ DecodeTime(item.used_at) || 'Не использовано' }}
        </template>
        <template v-slot:item.reg_btn="{ item }">
          <v-tooltip
            bottom
            :open-on-hover="false"
          >
            <template v-slot:activator="{ on }">
              <v-btn
                color="primary"
                small
                retain-focus-on-click
                v-on:click="on.click"
                @blur="on.blur"
                @click="CopyLink(item)"
              >
                Получить ссылку
              </v-btn>
            </template>
            <span>Скопировано в буфер обмена / Copied!</span>
          </v-tooltip>
        </template>
        <template v-slot:item.del_btn="{ item }">
          <v-btn
            color="error"
            small
            @click="deleteItem(item)"
          >
            <v-icon>
              mdi-delete
            </v-icon>
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
      { text: 'Получить ссылку / Copy Link for registration', value: 'reg_btn', align: 'center', sortable: false },
      { text: 'Удалить / Delete', value: 'del_btn', align: 'center', sortable: false }
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
        this.Invites = res.data.results
        this.loading = false
      })
    },
    Create () {
      api.axios.post('/api/admin/invites/').catch(res => {
        alert('Ошибка')
      }).then(res => {
        console.log(res)
        if (res.status === 201) {
          this.update()
        }
      }
      )
    },
    Edit (item) {
      api.axios.put('/api/admin/invites/' + item.code + '/', { is_active: !item.is_active }).catch(res => {
        alert('Ошибка')
      }).then(res => {
        if (res.status === 200) {
          this.update()
        }
      }
      )
    },
    CopyLink (item) {
      navigator.clipboard.writeText(window.location.host + '/auth/register/' + item.code + '/')
    },
    deleteItem (item) {
      api.axios.delete('/api/admin/invites/' + item.code + '/').catch(res => {
        alert('Ошибка')
      }).then(res => {
        if (res.status === 204) {
          this.update()
        }
      }
      )
    },
    DecodeTime (item) {
      if (item) {
        let data = item.split(/\s*T\s*/)
        let date = data[0].replace(/-/g, '.')
        let time = item.split(/\s*T\s*/)[1].split(/\s*:\s*/)
        return time[0] + ':' + time[1] + ' ' + date
      }
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
