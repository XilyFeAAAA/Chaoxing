import { createRouter, createWebHistory } from 'vue-router'
import * as storage from '@/common/storage'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('../views/dashboard/Layout.vue'),
            meta: {
                needAuth: true
            }
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/login/Login.vue'),
            meta: {
                needAuth: false
            }
        },
    ],
})

router.beforeEach((to, from, next) => {
    const requireAuth = to.matched.some((record) => record.meta.needAuth)
    if (requireAuth && !storage.getAccessToken()) {
        next('/login')
    } else next()
})

export default router
