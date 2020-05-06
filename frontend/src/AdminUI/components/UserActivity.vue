<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Users / Пользователи
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
          @click="close(),dialog=true"
        >
          Создать пользователя
        </v-btn>
      </v-card-title>
      <v-data-table
        :loading="loading"
        loading-text="Загрузка... Пожалуйста подождите / Loading... Please wait"
        :headers="headers"
        :items="Users"
        :search="search"
        :sort-desc="[false, true]"
        multi-sort
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar
            flat
            color="white"
          >
            <v-spacer />
            <v-dialog
              v-model="dialog"
              max-width="500px"
              @click:outside="close()"
            >
              <v-card style="margin: 0px">
                <v-card-title>
                  <span class="headline">
                    {{ formTitle }}
                  </span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem.id"
                          label="ID"
                          :solo="editedIndex === -1"
                          :disabled="editedIndex === -1"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem.username"
                          label="Имя пользователя / Username"
                        />
                      </v-col>
                      <v-col
                        v-if="editedIndex === -1"
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem.password"
                          label="Пароль / password"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem.first_name"
                          label="Имя / First name"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem.last_name"
                          label="Фамилия / Last name"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem.email"
                          label="Эл почта / Email"
                        />
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer />
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="close"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="save"
                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="editItem(item)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            @click="deleteItem(item)"
          >
            mdi-delete
          </v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn
            color="primary"
            @click="initialize"
          >
            Reset
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
        text: 'ID',
        value: 'id'
      },
      { text: 'Имя пользователя / Username', value: 'username' },
      { text: 'Имя / First name', value: 'first_name' },
      { text: 'Фамилия / Last name', value: 'last_name' },
      { text: 'Эл почта / Email', value: 'email' },
      { text: 'Actions', value: 'actions', sortable: false }
    ],
    dialog: false,
    Users: [
    ],
    editedIndex: -1,
    editedItem: {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      actions: 0
    },
    defaultItem: {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      actions: 0
    }
  }),
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Новый пользователь / New User' : 'Изменение пользователя / Edit User'
    }
  },
  mounted () {
    this.update()
  },
  methods: {
    update () {
      api.axios.get('/api/register/').then(res => {
        this.Users = res.data.results
        this.loading = false
      })
    },
    Create () {
      api.axios
        .post('/api/register/', {
          username: this.editedItem.username,
          password: this.editedItem.password,
          first_name: this.editedItem.first_name,
          last_name: this.editedItem.last_name,
          email: this.editedItem.email,
          invite_code: this.editedItem.invitecode
        })
        .catch(error => {
          console.log(error)
          if (error.response.status === 400) {
            alert('Пользователь с таким именем уже существует.')
          }
        }).then(
          this.loading = true,
          setTimeout(this.update(), 1000)
        )
    },
    editItem (item) {
      this.editedIndex = this.Users.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem (item) {
      const index = this.Users.indexOf(item)
      confirm('Are you sure you want to delete this item?') && this.desserts.splice(index, 1)
    },
    CopyLink (item) {
      navigator.clipboard.writeText(window.location.host + '/auth/register/' + item.code + '/')
    },
    close () {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    save () {
      if (this.editedIndex > -1) {
      } else {
        this.Create()
      }
      this.close()
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
