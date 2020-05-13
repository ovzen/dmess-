<template>
 <div>
    <v-divider />
    <v-col>
      <a class="basic--text">
        <u>
          SETTINGS
        </u>
      </a>
    </v-col>
    <v-list-item
      to="/MyProfile"
    >
      <v-icon
        class="pb-2"
        color="basic"
      >
        mdi-account-circle
      </v-icon>
      <v-list-item-content>
        <v-list-item-title
          class="pl-7 pb-2"
        >
          Profile
        </v-list-item-title>
        <v-divider
          class="ml-7"
        />
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: 'Settings',
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
