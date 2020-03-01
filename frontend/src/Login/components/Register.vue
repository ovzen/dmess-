<template>
  <v-app>
    <v-form>
      <v-container>
        <v-text-field
          v-model="login"
          label="Login"
          clearable
          required
          name="username"
          :rules="loginRules"
        />
        <v-form ref="passwords">
          <v-text-field
            v-model="password"
            clearable
            label="Password"
            required
            name="password"
            :rules="passwordRules"
          />
          <v-text-field
            v-model="repeatpassword"
            clearable
            label="Repeat password"
            required
            name="Repeat_password"
            :rules="repeatpasswordRules"
          />
        </v-form>
        <v-text-field
          v-model="name"
          clearable
          label="Name"
          name="first_name"
        />
        <v-text-field
          v-model="secondname"
          clearable
          label="Second name"
          name="last_name"
        />
        <v-text-field
          v-model="email"
          clearable
          label="E-mail"
          :rules="emailRules"
          name="email"
        />
        <div class="text-center">
          <v-btn
            class="ma-2"
            outlined
            color="primary"
            @click="GoToLogin()"
            v-text="button"
          >
            Войти
          </v-btn>
          <v-btn
            class="ma-2"
            outlined
            color="primary"
            @click="Register(login, password, repeatpassword, name, secondname, email)"
          >
            Регистрация
          </v-btn>
        </div>
      </v-container>
    </v-form>
  </v-app>
</template>

<script>
import api from '../api'
import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)
export default {
  name: 'Login',
  data: () => ({
    login: '',
    password: '',
    name: '',
    repeatpassword: '',
    secondname: '',
    email: '',
    ChatId: null,
    button: 'Войти',
    message_text: '',
    next: '',
    loginRules: [
      v => !!v || 'Login is required',
      v => (v || '').length >= 2 ||
              `Minimal length of username is 2 symbols`
    ],
    emailRules: [
      v => /.+@.+\..+/.test(v) || v.length <= 0 || 'E-mail must be valid'
    ]
  }),
  computed: {
    repeatpasswordRules () {
      const rules = []
      rules.push(v => !!v || 'Repeat password is required')
      rules.push(v => (!!v && v) === this.password ||
              'Values do not match')
      return rules
    },
    passwordRules () {
      const rules = []
      rules.push(v => !!v || 'Password is required')
      return rules
    }
  },
  watch: {
    repeatpassword: 'validateField',
    password: 'validateField'
  },
  created () {
    if (this.$route.query.next) {
      this.next = 'http://' + window.location.host + this.$route.query.next
    } else {
      this.next = 'http://' + window.location.host
    }
    this.login = this.$root.$children[0].login
    this.name = this.$root.$children[0].name
    this.secondname = this.$root.$children[0].secondname
    this.email = this.$root.$children[0].email
  },
  methods: {
    validateField () {
      this.$refs.passwords.validate()
    },
    GoToLogin () {
      this.$root.$children[0].login = this.login
      this.$root.$children[0].name = this.name
      this.$root.$children[0].secondname = this.secondname
      this.$root.$children[0].email = this.email
      this.$router.push('/login/')
    },
    Register (username, password, repeatpassword, name, secondname, email) {
      if ((username && password) && (password === repeatpassword)) {
        api.axios
          .post('/api/register/', {
            username: username,
            password: password,
            first_name: name,
            last_name: secondname,
            email: email
          })
          .catch(error => {
            console.log(error)
            if (error.response.status === 400) {
              alert('Пользователь с таким именем уже существует.')
            }
          }).then(data => {
            if (data.status === 201) {
              api.axios.post('/api/token/', {
                username: username,
                password: password
              }).then(res => {
                console.log(res.data)
                this.$cookie.set('Authentication', res.data.access, {
                  expires: '5m'
                })
                window.location.href = this.next
              })
            }
          })
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
