import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../components/Login')
  },
  {
    path: '/uric',
    name: 'Base',
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
      {
        path: 'console/:id',
        name: 'Console',
        component: () => import(/* webpackChunkName: "about" */ '../components/Console')
      },
      {
        path: 'multi_exec',
        name: 'MultiExec',
        component: () => import(/* webpackChunkName: "about" */ '../components/MultiExec')
      },
      {
        path: 'template_manage',
        name: 'TemplateManage',
        component: () => import(/* webpackChunkName: "about" */ '../components/TemplateManage')
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
