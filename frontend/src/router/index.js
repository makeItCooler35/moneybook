import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '',
    name: '',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/book',
    name: 'book',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/BookView.vue')
  },
  {
    path: '/operations',
    name: 'operations',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/OperationsView.vue'),
    children: [
      {
        path: 'uploadtinkoff',
        name: 'uploadtinkoff',
        component: () => import('../views/operations/UploadTinkoffView.vue'),
      },
      {
        path: 'unloadcosts',
        name: 'unloadcosts',
        component: () => import('../views/operations/UnloadCostsView.vue'),
      }
    ],
  },
  {
    path: '/handbooks',
    name: 'handbooks',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/HandBooksView.vue')
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('../views/handbooks/CategoriesView.vue'),
  },
  {
    path: '/accounts',
    name: 'accounts',
    component: () => import('../views/PageNotCreatedYet.vue')
  },
  {
    path: "*",
    component: () => import('../views/PageNotFound.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
