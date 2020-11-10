import Vue from 'vue'
import VueRouter from 'vue-router'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home')
  },
  {
    path: '/spot',
    name: 'SpotMain',
    component: () => import(/* webpackChunkName: "spot" */ '../views/spots/SpotMain.vue')
  },
  {
    path: '/spot/search',
    name: 'SpotSearch',
    component: () => import(/* webpackChunkName: "spot" */ '../views/spots/SpotSearch.vue')
  },
  {
    path: '/spot/:spot_id',
    name: 'SpotDetail',
    component: () => import(/* webpackChunkName: "spot" */ '../views/spots/SpotDetail.vue')
  },
  {
    path: '/login',
    name: 'UsersLogin',
    component: () => import('@/views/users/UsersLogin')
  },
  {
    path: '/signup',
    name: 'UsersSignup',
    component: () => import('@/views/users/UsersSignup')
  },
  {
    path: '/mypage',
    name: 'UsersMypage',
    component: () => import('@/views/users/UsersMypage')
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('@/views/schedules/Schedule')
  },
  {
    path: '/schedulemain',
    name: 'ScheduleMain',
    component: () => import('@/views/ScheduleMain')
  },
  {
    path: '/sdresult',
    name: 'SDresult',
    component: () => import('@/views/SDresult')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
