<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-flex
      justify-center
      d-flex
    >
      <v-container
        class="display-1 grey--text"
        d-flex
      >
        <pre class="display-2 grey--text">
                        ／＞　 フ
                        |    _　 _|
                    ／`ミ _x 彡
                   /　　　     |
                  /   ヽ　　  ﾉ
         ／￣|       |　|　 |
        | (￣ヽ＿_ヽ_)_)
         ＼二つ
        </pre>
      </v-container>
      <v-container
        mt-12
        pt-12
      >
        <p
          class="display-3 text-center grey--text font-weight-black"
        >
          404
        </p>
        <p
          class="overline text-center grey--text font-weight-black"
        >
          PAGE NOT FOUND
        </p>
      </v-container>
    </v-flex>
  </v-container>
</template>

<script>
export default {
  name: 'Error404',
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
