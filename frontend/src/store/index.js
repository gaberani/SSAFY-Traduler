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

//   state: {
//     LoginFlag: false,
//     authToken: cookies.get('auth-token'),
//     UserInfo: {}
//   },
//   mutations: {
//     SET_TOKEN(state, token) {
//       state.authToken = token
//       cookies.set('auth-token', token)
//     },
//     DELETE_TOKEN(state) {
//       state.authToken = null
//       cookies.remove('auth-token')
//     },
//     SET_LOGIN_FLAG(state) {
//       state.LoginFlag = !!state.authToken
//     },
//     LOGIN_STATE(state, result) {
//       if ( result === true) {
//         state.LoginFlag = result
//       } else {
//         state.LoginFlag = false
//         state.authToken = null
//       }
//     },
//     GET_USER_INFO(state, info) {
//       state.UserInfo = info
//     }
//   },
//   actions: {
//     SubmitLoginData({ state, commit }, UserLoginData) {
//       if (state.LoginFlag === false) {
//         if (UserLoginData.username.trim() && UserLoginData.password.trim()) {
//           Vue.prototype.$http
//             .post(process.env.VUE_APP_SERVER_URL + '/rest-auth/login/', UserLoginData, { headers: { 'X-CSRFToken': cookies.get('csrftoken')}})
//             .then(res => {
//               const token = res.data.token
//               cookies.set('auth-token', token)
//               window.sessionStorage.setItem('username', UserLoginData.username)
//               commit("SET_TOKEN", token)
//               commit("LOGIN_STATE", true)
//               router
//                 .push({ name: 'Home'})
//                 .catch(err => {
//                   if(err.name !== "NavigationDuplicated" ){
//                     throw err
//                   }
//                 })
//             })
//             .catch(err => {
//               commit("LOGIN_STATE", false)
//               console.log(err.response)
//             })
          
//         }
//       } else {
//         router.push({ name: 'Home'})
//         alert('이미 로그인 상태입니다.')
//       }
//     },

//     SubmitLogout({ state, getters, commit }) {
//       if (getters.LoginFlag === true) {
//         const config = {
//           headers: {'Authorization': `jwt ${state.authToken}`}
//         }
//         Vue.prototype.$http
//           .post(process.env.VUE_APP_SERVER_URL + '/rest-auth/logout/', null, config)
//           .catch(err => {
//             console.log(err.response)
//             alert('로그아웃이 정상적으로 처리되지 않았습니다.')
//           })
//           .finally(() => {
//             cookies.remove('auth-token')
//             commit("LOGIN_STATE", false)
//             if (router.history.current.name !== 'Home') {
//               router.push({ name:'Home'})
//             }
//           })
//       }
//     },

//     SubmitSignupData({ state, commit }, UserSignupData) {
//       if (state.LoginFlag === false) {
//         if (UserSignupData.username.trim() && UserSignupData.password1.trim()) {
//           // console.log(cookies.get('csrftoken'))
//           UserSignupData.age *= 1 
//           Vue.prototype.$http
//             .post(process.env.VUE_APP_SERVER_URL + '/rest-auth/signup/', UserSignupData, { headers: { 'X-CSRFToken': cookies.get('csrftoken')}})
//             .then(res => {
//               const token = res.data.token
//               cookies.set('auth-token', token)
//               commit("SET_TOKEN", token)
//               commit("LOGIN_STATE", true)
//               router
//                 .push({ name: 'Home'})
//                 .catch(err => {
//                   if(err.name !== "NavigationDuplicated" ){
//                     throw err
//                   }
//                 })
//             })
//             .catch(err => {
//               console.log(err.response.data)
//               commit("LOGIN_STATE", false)
//               // console.log(err)
//             })
//         }
//       }
//     },

//     GetUserInfo({ state, getters, commit }) {
//       if (getters.LoginFlag === true) {
//         const config = {
//           headers: {'Authorization': `jwt ${state.authToken}`}
//         }
//         Vue.prototype.$http
//           .get(process.env.VUE_APP_SERVER_URL + '/accounts/', config)
//           .then(() => {
//             commit("GET_USER_INFO", {username: 'asdasd'})
//           })
//       }
//     }
//   },
//   modules: {
//   },
//   getters: {
//     LoginFlag: state => !! state.authToken,
//     config: (state) => `jwt ${state.authToken}`,
//     // header: (state) => `{headers: {Authorization: ${state.authToken}}}`
//     userInfo: state => state.UserInfo
//   }
// })
