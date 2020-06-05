
<template>
  <div style="height:100%">
    <v-row
      align="center"
      justify="center"
      style="padding-bottom:56px;height:100%;"
    >
      <div class="d-flex flex-column">
        <span
          style="font-weight: 300;
              font-size: 96px;
              line-height: 112px;
              text-align: center;
              letter-spacing: -1.5px;"
          class="smile_color--text"
        >
          ¯\_(ツ)_/¯
        </span>
        <span
          style="font-family: Roboto;
              font-style: normal;
              font-weight: 500;
              font-size: 14px;
              line-height: 16px;
              text-align: center;
              letter-spacing: 0.75px;
              text-transform: uppercase;
              padding-top:15px"
          class="smile_color--text"
        >
          there are no messages yet
        </span>
      </div>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'NoMessages',
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
