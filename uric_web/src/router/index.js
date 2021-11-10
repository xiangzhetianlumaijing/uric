import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../components/Login')
  },
  {
    path: '/uric',
    name: 'Base',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../components/Base'),
    children: [
      {
        path: 'workbench',  //访问路径：父级路由 + 当前路由
        name: 'ShowCenter',
        component: () => import(/* webpackChunkName: "about" */ '../components/ShowCenter')
      },
      {
        path: 'host',  //访问路径：父级路由 + 当前路由
        name: 'Host',
        component: () => import(/* webpackChunkName: "about" */ '../components/Host')
      },
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
