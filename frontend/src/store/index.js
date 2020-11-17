import Vue from 'vue'
import Vuex from 'vuex'
// import cookies from 'vue-cookies'
// import router from '../router'

import moduleAccounts from "./accounts";
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    accounts: moduleAccounts
  },
})