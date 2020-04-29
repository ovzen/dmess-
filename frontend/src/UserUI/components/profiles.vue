<template>
  <div>
    <v-divider />
    <v-col>
      <v-text-field
        clearable
        solo
        background-color="grey lighten-2"
        dense
        flat
        color="basic"
        hide-details
        prepend-inner-icon="mdi-magnify"
        label="Search for users"
        style="border-radius:50px; max-width:450px;"
      />
    </v-col>
    <v-divider />
    <v-list-item to="/ChatUser">
      <v-list-item-avatar>
        <v-avatar
          size="36px"
          color="basic"
        >
          <span
            class="white--text"
          >
            NU
          </span>
          <!--<v-img
            src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
          />-->
        </v-avatar>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
          Name User
        </v-list-item-title>
        <v-list-item-subtitle>
          <span
            class="basic--text text--lighten"
          >
            online
          </span>
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: 'Profiles',
  data: () => ({
  })
}
</script>

<style lang="scss" scoped>
.container {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
</style>
