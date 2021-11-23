import Vue from 'vue'
import App from './App.vue'
import router from './router'
import settings from "./settings";
import axios from "axios";
import 'xterm/css/xterm.css'
import 'xterm/lib/xterm'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

Vue.prototype.$settings = settings;  //prototype原型链

axios.defaults.withCredentials = false;  //是否在ajax请求时允许携带cookie到服务器
axios.defaults.baseURL = settings.host;
axios.defaults.timeout = 3000;
Vue.prototype.$axios = axios;

import Antd from 'ant-design-vue';
Vue.use(Antd);
import 'ant-design-vue/dist/antd.css';
