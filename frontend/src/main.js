import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from 'axios'
import LazyLoading from "@/components/common/LazyLoading";
import VueCookies from 'vue-cookies'

Vue.prototype.$http = axios;
Vue.component("lazy-loading", LazyLoading);

const csrf = VueCookies.get("csrftoken")
if (csrf){
  Vue.prototype.$http.defaults.headers.common['X-CSRFToken'] = csrf
}

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
