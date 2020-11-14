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
    path: '/schedule',
    name: 'ScheduleMain',
    component: () => import('@/views/schedules/ScheduleMain')
  },
  {
    path: '/schedule/result',
    name: 'Scheduleresult',
    component: () => import('@/views/schedules/Scheduleresult')
  },
  {
    path: '/schedule/new',
    name: 'NewSchedule',
    component: () => import('@/views/schedules/NewSchedule')
  },
  {
    path: '/schedule/create',
    name: 'CreateSchedule',
    component: () => import('@/views/schedules/CreateSchedule')
  },
  {
    path: '/schedule/:schedule_id',
    name: 'DetailSchedule',
    component: () => import('@/views/schedules/DetailSchedule')
  },
  {
    path: '*',
    redirect: '/404'
  },
  {
    path: '/404',
    name: '404Page',
    component: () => import('@/views/404Page')
  }
]

const router = new VueRouter({
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
