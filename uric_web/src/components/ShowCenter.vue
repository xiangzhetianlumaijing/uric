<template>
  <div class="show_center">
    <h1>展示中心页面</h1>
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
}
</script>

<style scoped>

</style>