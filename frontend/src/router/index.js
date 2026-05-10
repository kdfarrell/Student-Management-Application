import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

import AuthLayout from '../layouts/AuthLayout.vue'
import AppLayout from '../layouts/AppLayout.vue'
import LoginView from '../views/auth/LoginView.vue'

const routes = [
    {
        path: '/login',
        component: AuthLayout,
        children: [
            { path: '', component: LoginView }
        ]
    },
    {
        path: '/',
        redirect: '/dashboard',
        component: AppLayout,
        meta: { requiresAuth: true },
        children: [
            { 
                path: 'dashboard', 
                component: { template: '<div>Dashboard placeholder</div>' }
            }
        ]
    }
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const auth = useAuthStore()

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        next('/login')
    }
    else if (to.path === '/login' && auth.isAuthenticated) {
        next('/dashboard')
    }
    else {
        next()
    }
})

export default router