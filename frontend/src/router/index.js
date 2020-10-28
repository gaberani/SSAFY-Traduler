import Vue from 'vue'
import VueRouter from 'vue-router'



Vue.use(VueRouter)

const routes = [
  {
    path: '/spot',
    name: 'Spot',
    component: () => import(/* webpackChunkName: "spot" */ '../views/Spot.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/users/UsersLogin')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('@/views/users/UsersSignup')
  },
  {
    path: '/mypage',
    name: 'Mypage',
    component: () => import('@/views/users/UsersMypage')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
