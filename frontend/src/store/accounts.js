import Vue from 'vue'

import cookies from 'vue-cookies'
import router from '@/router'
import axios from 'axios'

import SERVER from '@/api/api'


export default {
  namespaced: true,
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
    SET_USER_INFO(state, info) {
      state.UserInfo = info
    }
  },
  actions: {
    SubmitLoginData({ getters, commit }, UserLoginData) {
      if (getters.LoginFlag === false) {
        if (UserLoginData.username.trim() && UserLoginData.password.trim()) {
          axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.USER.LOGIN, UserLoginData, { headers: { 'X-CSRFToken': cookies.get('csrftoken')}})
          .then(res => {
            const token = res.data.token
            cookies.set('auth-token', token)
            window.sessionStorage.setItem('username', UserLoginData.username)
            commit("SET_TOKEN", token)
            commit("LOGIN_STATE", true)
            router
              .push({ name: 'Home'})
              .catch(err => {
                if(err.name !== "NavigationDuplicated" ){
                  throw err
                }
              })
          })
          .catch(err => {
            commit("LOGIN_STATE", false)
            console.log(err.response)
          })
        }
      } else {
        alert('이미 로그인 상태입니다.')
        router
          .push({ name: 'Home'})
          .catch(err => { 
            if(err.name !== "NavigationDuplicated" ){ throw err }
          })
      }
    },

    SubmitLogout({ getters, commit }) {
      if (getters.LoginFlag === true) {
        const config = {
          headers: {'Authorization': getters.authToken}
        }
        axios.post(process.env.VUE_APP_SERVER_URL + SERVER.URL.USER.LOGOUT, null, config)
          .catch(err => {
            console.log(err.response)
            alert('로그아웃이 정상적으로 처리되지 않았습니다.')
          })
          .finally(() => {
            cookies.remove('auth-token')
            commit("LOGIN_STATE", false)
            window.sessionStorage.removeItem('username')
            if (router.history.current.name !== 'Home') {
              router.push({ name:'Home'})
            }
          })
      } else {
        alert('로그인한 상태가 아닙니다.')
        router
          .push({name: 'UsersLogin'})
          .catch(err => { 
            if(err.name !== "NavigationDuplicated" ){ throw err }
          })
      }
    },

    SubmitSignupData({ state, commit }, UserSignupData) {
      if (state.LoginFlag === false) {
        if (UserSignupData.username.trim() && UserSignupData.password1.trim()) {
          // console.log(cookies.get('csrftoken'))
          UserSignupData.age *= 1 
          Vue.prototype.$http
            .post(process.env.VUE_APP_SERVER_URL + SERVER.URL.USER.SIGNUP, UserSignupData, { headers: { 'X-CSRFToken': cookies.get('csrftoken')}})
            .then(res => {
              const token = res.data.token
              cookies.set('auth-token', token)
              commit("SET_TOKEN", token)
              commit("LOGIN_STATE", true)
              router
                .push({ name: 'Home'})
                .catch(err => {
                  if(err.name !== "NavigationDuplicated" ){
                    throw err
                  }
                })
            })
            .catch(err => {
              console.log(err.response.data)
              commit("LOGIN_STATE", false)
            })
        }
      }
    },

    GetUserInfo({ state, getters, commit }) {
      if (getters.LoginFlag === true) {
        const config = {
          headers: {'Authorization': `jwt ${state.authToken}`}
        }
        Vue.prototype.$http
          .get(process.env.VUE_APP_SERVER_URL + SERVER.URL.USER.EDITORDEL, config)
          .then(res => {
            commit("SET_USER_INFO", res.data)
          })
      }
    }
  },
  getters: {
    LoginFlag: state => !! state.authToken,
    config: (state) => `jwt ${state.authToken}`,
    // header: (state) => `{headers: {Authorization: ${state.authToken}}}`
    userInfo: state => state.UserInfo
  }
}
