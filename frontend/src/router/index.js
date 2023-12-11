import {createRouter, createWebHashHistory} from 'vue-router'
import {useAuthStore} from "@/stores";


let authStore = null

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/dashboard',
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('@/views/dashboard/Layout.vue'),
            meta: {
                needAuth: true,
            },
            children: [
                {
                    path: '',
                    redirect: {name: 'courses'},
                },
                {
                    path: 'courses',
                    name: 'courses',
                    component: () => import('@/views/dashboard/Courses.vue'),
                },
                {
                    path: 'account',
                    name: 'account',
                    component: () => import('@/views/dashboard/Account.vue'),
                },
                {
                    path: 'order',
                    name: 'order',
                    component: () => import('@/views/dashboard/Order.vue'),
                },
                {
                    path: 'help',
                    name: 'help',
                    component: () => import('@/views/dashboard/Help.vue'),
                },
                {
                    path: 'inmail',
                    name: 'inmail',
                    component: () => import('@/views/dashboard/Inmail.vue')
                },
                {
                    path: 'confirm/:order_id',
                    name: 'confirm',
                    component: () => import('@/views/dashboard/OrderConfirm.vue')
                },
                {
                    path: 'setting',
                    name: 'setting',
                    component: () => import('@/views/dashboard/setting/Layout.vue'),
                    children: [
                        {
                            path: '',
                            redirect: {name: 'accountsetting'},
                        },
                        {
                            path: 'account',
                            name: 'accountsetting',
                            component: () => import('@/views/dashboard/setting/Account.vue'),
                        },
                        {
                            path: 'course',
                            name: 'coursesetting',
                            component: () => import('@/views/dashboard/setting/Course.vue'),
                        },
                    ],
                },
            ],
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/login/Login.vue'),
            meta: {
                needAuth: false,
            },
        },
        {
            path: '/admin',
            component: () => import('../views/admin/Layout.vue'),
            children: [
                {
                    path: '',
                    redirect: '/admin/dashboard',
                },

                {
                    path: 'dashboard',
                    name: '仪表盘',
                    children: [
                        {
                            path: '',
                            redirect: {name: '工作台'}
                        },
                        {
                            path: 'workbench',
                            name: '工作台',
                            component: () => import('@/views/admin/dashboard/Workbench.vue'),
                        },
                        {
                            path: 'analysis',
                            name: '分析页',
                            component: () => import('@/views/admin/dashboard/Analysis.vue'),
                        }
                    ]
                },
                {
                    path: 'order',
                    name: '订单管理',
                    children: [
                        {
                            path: '',
                            redirect: {name: '刷课订单'},
                        },
                        {
                            path: 'course',
                            name: '刷课订单',
                            component: () => import('@/views/admin/order/CourseOrder.vue'),
                        },
                        {
                            path: 'logger',
                            name: '日志',
                            component: () => import('@/views/admin/order/Log.vue')
                        }
                    ],
                },
                {
                    path: 'user',
                    name: '用户管理',
                    children: [
                        {
                            path: '',
                            redirect: {name: '用户列表'},
                        },
                        {
                            path: 'member',
                            name: '用户列表',
                            component: () => import('@/views/admin/user/Member.vue'),
                        },
                        {
                            path: 'admin',
                            name: '管理员列表',
                            component: () => import('@/views/admin/user/Admin.vue'),
                        },
                    ],
                },
                {
                    path: 'rbac',
                    name: '权限管理',
                    children: [
                        {
                            path: '',
                            redirect: {name: '权限列表'},
                        },
                        {
                            path: 'permission',
                            name: '权限列表',
                            component: () => import('@/views/admin/rbac/Permission.vue'),
                        },
                        {
                            path: 'role',
                            name: '角色列表',
                            component: () => import('@/views/admin/rbac/Role.vue'),
                        },
                    ],
                },
            ],
        },
        {
            path: '/admin/login',
            name: 'adminlogin',
            component: () => import('@/views/admin/Login.vue')
        },
    ],
})

router.beforeEach((to, from, next) => {
    if (authStore === null) {
        authStore = useAuthStore()
    }
    const requireAuth = to.matched.some((record) => record.meta.needAuth)
    if (requireAuth && !authStore.isAuth) {
        next('/login')
    } else next()
})

export default router
