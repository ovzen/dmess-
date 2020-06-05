<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Invites
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
          Create invite
        </v-btn>
      </v-card-title>
      <v-data-table
        :loading="loading"
        loading-text="Loading... Please wait"
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
            color="basic"
            @click.stop="Edit(item)"
          />
        </template>
        <template v-slot:item.for_user="{ item }">
          {{ item.for_user || 'Not used' }}
        </template>
        <template v-slot:item.used_at="{ item }">
          {{ DecodeTime(item.used_at) || 'Not used' }}
        </template>
        <template v-slot:item.reg_btn="{ item }">
          <v-tooltip
            bottom
            :open-on-hover="false"
          >
            <template v-slot:activator="{ on }">
              <v-btn
                color="basic"
                dark
                small
                retain-focus-on-click
                v-on:click="on.click"
                @blur="on.blur"
                @click="CopyLink(item)"
              >
                Get the link
              </v-btn>
            </template>
            <span>Copied!</span>
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
        text: 'Code',
        value: 'code'
      },
      { text: 'Created', value: 'created_at' },
      { text: 'Is active', value: 'is_active' },
      { text: 'For user', value: 'for_user' },
      { text: 'Used at', value: 'used_at' },
      { text: 'Copy Link for registration', value: 'reg_btn', align: 'center', sortable: false },
      { text: 'Delete', value: 'del_btn', align: 'center', sortable: false }
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
        alert('Error')
      }).then(res => {
        console.log(res)
        if (res.status === 201) {
          this.loading = true
          this.update()
        }
      }
      )
    },
    Edit (item) {
      api.axios.put('/api/admin/invites/' + item.code + '/', { is_active: !item.is_active }).catch(res => {
        alert('Error')
      }).then(res => {
        if (res.status === 200) {
          this.loading = true
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
        alert('Error')
      }).then(res => {
        if (res.status === 204) {
          this.loading = true
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
