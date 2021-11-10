<template>
  <div class="show_center">
    <h1>展示中心页面</h1>
    <a-button type="danger">
      Danger
    </a-button>
    <div :style="{ width: '300px', border: '1px solid #d9d9d9', borderRadius: '4px' }">
      <a-calendar :fullscreen="false" @panelChange="onPanelChange"/>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShowCenter",
  created(){
    console.log("host:::", this.$settings.host);
    this.$axios.get("http://wthrcdn.etouch.cn/weather_mini?city=北京",).then(response => {
      console.log(response.data.data.forecast);
    })
  },
  methods: {
    onPanelChange(value, mode) {
      console.log(value, mode);
    },
  },
}
</script>

<style scoped>

</style>