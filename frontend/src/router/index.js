import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    name: 'CaseList',
    component: () => import('@/views/CaseList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id',
    name: 'CaseDetail',
    component: () => import('@/views/CaseDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id/upload',
    name: 'DocumentUpload',
    component: () => import('@/views/DocumentUpload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id/elements',
    name: 'ElementReview',
    component: () => import('@/views/ElementReview.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/templates',
    name: 'TemplateManage',
    component: () => import('@/views/TemplateManage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/case/:id/preview',
    name: 'DocumentPreview',
    component: () => import('@/views/DocumentPreview.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
