<template>
  <v-app>
  <a href="/admin" style="text-decoration: none;"><v-btn class="ma-2" outlined color="indigo" >Комнатка админа</v-btn></a>
  <v-form v-model="valid">
    <v-container>
      <v-row>
          <v-text-field
            v-model="login"
            label="Login"
            clearable
            required
          ></v-text-field>

        <v-col
          cols="12"
          md="1"
        >
        </v-col>
          <v-text-field
            v-model="password"
            clearable
            label="Password"
            required
          ></v-text-field>
      </v-row>
      <div class="text-center">
      <v-btn class="ma-2" outlined color="indigo" v-text="button" @click="auth(login,password)" >Войти</v-btn>
      </div>
    </v-container>
    </v-form>
  </v-app>
</template>

<script>
import api from '@/api';
import jwt from 'jsonwebtoken'
export default {
  name: 'App',
  data: () => ({
    login: "",
    button: "Войти",
    password: "",
  }),
  methods: {
    auth(username,password) {
      api.axios.post('/api/token/', {"username": username, "password": password}).then((res) => {
        console.log(res.data)
        localStorage.setItem('jwt', res.data.access)
        this.button=jwt.decode(localStorage.jwt)
        console.log(jwt.decode(localStorage.jwt))
      })
    }
  }
};
</script>
