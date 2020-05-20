<template>
  <v-container
    fluid
  >
    <a
      href="/django_admin/"
      style="text-decoration: none;"
    >
      <v-btn
        class="ma-2"
        outlined
        color="basic"
      >
        Комнатка админа
      </v-btn>
    </a>
    <a
      href="/admin/"
      style="text-decoration: none;"
    >
      <v-btn
        class="ma-2"
        outlined
        color="basic"
      >
        Комнатка модератора
      </v-btn>
    </a>
    <v-form>
      <v-container>
        <v-row>
          <v-text-field
            v-model="ChatName"
            clearable
            label="Chat name"
            required
          />
          <v-btn
            class="ma-2"
            outlined
            color="basic"
            @click="FindChat(ChatName)"
          >
            Перейти в чат
          </v-btn>
        </v-row>
      </v-container>
    </v-form>

    <div class="main">
      <h1 class="main_smile smile_color--text">
        ¯\_(^ ‿ ^)\
      </h1>
      <span class="main_smile_text smile_color--text">
        select a dialog to start messaging
      </span>
    </div>
  </v-container>
</template>

<script>
import api from '../api'
import jwt from 'jsonwebtoken'
import VueCookie from 'vue-cookie'
import Vue from 'vue'
Vue.use(VueCookie)
export default {
  name: 'Main',
  data: () => ({
    login: '',
    ChatName: null,
    button: 'Войти',
    password: '',
    message_text: '',
    data: '',
    user_id: undefined
  }),
  created () {
    if (this.$cookie.get('Authentication')) {
      this.user_id = jwt.decode(this.$cookie.get('Authentication')).user_id
    } else {
      console.warn('The current user was not found')
    }
  },
  methods: {
    FindChat (ChatName) {
      if (ChatName) {
        api.axios
          .get('/api/dialog/', {
            params: {
              name: ChatName
            }
          })
          .then(response => {
            if (response.data.length > 0) {
              this.$router.push('ChatUser/' + response.data[0].id)
            } else {
              api.axios
                .post('/api/dialog/', {
                  name: ChatName,
                  users: [this.user_id]
                })
                .then(response => {
                  console.log('post response:', response)
                  if (response && response.data && response.data.id) {
                    this.$router.push('ChatUser/' + response.data.id)
                  }
                })
            }
          })
      }
    },
    Exit () {
      localStorage.removeItem('jwt')
      this.$cookie.delete('Authentication')
      location.reload()
    },
    Register (username, password) {
      if (username && password) {
        api.axios
          .post('/api/register/', {
            username: username,
            password: password
          })
          .catch(error => {
            if (error.response.status === 400) {
              alert('Пользователь с таким именем уже существует')
            }
          })
      }
    },
    auth (username, password) {
      api.axios
        .post('/api/token/', {
          username: username,
          password: password
        })
        .then(res => {
          console.log(res.data)
          this.$cookie.set('Authentication', res.data.access, {
            expires: '5m'
          })
          this.button = 'Приветствуем ' + jwt.decode(this.$cookie.get('Authentication')).name
        })
        .catch(error => {
          if (error.response.status === 401) {
            this.button = 'Ошибка неправильное имя пользователя или пароль'
          }
          console.log(error.response.status)
        })
    }
  }
}
</script>
<style lang="scss">
.main {
  margin:auto;
  position: fixed;
  top:44%;
  left:50%;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
}
.main_smile {
  margin-bottom: 32px;
  margin-left: -36px;
  font-family: Roboto;
  font-style: normal;
  font-weight: 300;
  font-size: 96px;
  line-height: 112px;
  /* identical to box height */
  letter-spacing: -1.5px;
}
.main_smile_text {
  margin-top: 32px;
  font-family: Roboto;
  font-style: normal;
  font-weight: 500;
  font-size: 14px;
  line-height: 16px;
  letter-spacing: 0.75px;
  text-transform: uppercase;
}
</style>
