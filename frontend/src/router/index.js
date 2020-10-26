import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'



Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/spot',
  //   name: 'Spot',
  //   component: () => import(/* webpackChunkName: "spot" */ '../views/Spot.vue')
  // },
  {
    path: '/',
    name: 'Home',
    component: Home
  },
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
