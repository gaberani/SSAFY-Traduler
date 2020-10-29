import Vue from 'vue'
import Vuex from 'vuex'
import cookies from 'vue-cookies'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    LoginFlag: false,
    authToken: cookies.get('auth-token'),
    UserInfo: {}
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
    SET_LOGIN_FLAG(state) {
      state.LoginFlag = !!state.authToken
    },
    LOGIN_STATE(state, result) {
      if ( result === true) {
        state.LoginFlag = result
      } else {
        state.LoginFlag = false
        state.authToken = null
      }
    },
    GET_USER_INFO(state, info) {
      state.UserInfo = info
    }
  },
  actions: {
    SubmitLoginData({ state, commit }, UserLoginData) {
      if (state.LoginFlag === false) {
        if (UserLoginData.username.trim() && UserLoginData.password.trim()) {
          Vue.prototype.$http
            .post(process.env.VUE_APP_SERVER_URL + '/rest-auth/login/', UserLoginData, { headers: { 'X-CSRFToken': cookies.get('csrftoken')}})
            .then(res => {
              console.log(res)
              const token = res.data.token
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
            .catch(() => {
              commit("LOGIN_STATE", false)
              // console.log(err)
            })
          
        }
      } else {
        router.push({ name: 'Home'})
        alert('이미 로그인 상태입니다.')
      }
    },
    SubmitLogout({ state, getters, commit }) {
      if (getters.LoginFlag === true) {
        const config = {
          headers: {'Authorization': `jwt ${state.authToken}`}
        }
        Vue.prototype.$http
          .post(process.env.VUE_APP_SERVER_URL + '/rest-auth/logout/', null, config)
          .catch(() => {
            // console.log(err.response)
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
    GetUserInfo({ state, getters, commit }) {
      if (getters.LoginFlag === true) {
        const config = {
          headers: {'Authorization': `jwt ${state.authToken}`}
        }
        Vue.prototype.$http
          .get(process.env.VUE_APP_SERVER_URL + '/accounts/', config)
          .then(res => {
            console.log(res)
            commit("GET_USER_INFO", {username: 'asdasd'})
          })
      }
    }
  },
  modules: {
  },
  getters: {
    LoginFlag: state => !! state.authToken,
    config: (state) => `jwt ${state.authToken}`,
  }
})
