import Vue from 'vue'
import Vuex from 'vuex'

import cookies from 'vue-cookies'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    LoginFlag: false,
    authToken: cookies.get('auth-token'),
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.authToken = token
      cookies.set('auth-token', token)
    },
    DELETE_TOKEN(state) {
      state.authToken = null
      cookies.remove('auth-token')
    },
  },
  actions: {
    loginTry({ state, commit }, UserLoginData) {
      if (state.LoginFlag === false) {
        if (UserLoginData.username.trim() && UserLoginData.password.trim()) {
          Vue.prototype.$http
            .post(process.env.VUE_APP_SERVER_URL + '/users/login/', UserLoginData, { headers: { 'X-CSRFToken': cookies.get('csrftoken')}})
            .then(res => {
              const token = res.data.key
              cookies.set('auth-token', token)
              window.sessionStorage.setItem('username', UserLoginData.username)
              commit("SET_TOKEN", token)
              commit("LOGIN_STATE", true)
              router
                .push({ name: 'Home'})
                .catch(err => {
                  if(err.name != "NavigationDuplicated" ){
                    throw err
                  }
                })
            })
            .catch(err => {
              commit("LOGIN_STATE", false)
              console.log(err)
            })
          
        }
      } else {
        router.push({ name: 'Home'})
        alert('이미 로그인 상태입니다.')
      }
    },
    logoutTry({ state, getters, commit }) {
      if (getters.LoginFlag === true) {
        const config = {
          headers: {'Authorization': `Token ${state.authToken}`}
        }
        Vue.prototype.$http
          .post(process.env.VUE_APP_SERVER_URL + '/users/logout/', null, config)
          .catch(err=> {
            console.log(err.response)
            alert('로그아웃이 정상적으로 처리되지 않았습니다.')
          })
          .finally(() => {
            window.sessionStorage.removeItem('username')
            cookies.remove('auth-token')
            commit("LOGIN_STATE", false)
            router.push({ name:'Home'})
          })
      }
    },
  },
  modules: {
  },
  getters: {
    LoginFlag: state => !! state.authToken
  }
})
