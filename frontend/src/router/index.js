import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

// Layouts
import AppLayout from '../layouts/AppLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'

// Auth views (eager - needed immediately)
import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'

const routes = [
	{
		path: '/login',
		component: AuthLayout,
		children: [{ path: '', component: LoginView }]
	},
	{
		path: '/register',
		component: AuthLayout,
		children: [{ path: '', component: RegisterView }]
	},
	{
		path: '/',
		redirect: '/dashboard',
		component: AppLayout,
		meta: { requiresAuth: true },
		children: [
			{ path: 'dashboard', component: () => import('@/views/dashboard/DashboardView.vue') },
			{ path: 'students', component: () => import('@/views/students/StudentsView.vue') },
			{ path: 'courses', component: () => import('@/views/courses/CoursesView.vue') },
			{ path: 'courses/:id', component: () => import('@/views/courses/CourseDetail.vue') },
			{ path: 'schedule', component: () => import('@/views/schedule/Schedule.vue') },
			{ path: 'attendance', component: () => import('@/views/attendance/AttendanceView.vue') },
			{ path: 'grades', component: () => import('@/views/grades/GradesView.vue') },
			{ path: 'reports', component: () => import('@/views/reports/ReportsView.vue') },
			{ path: 'audit', component: () => import('@/views/audit/AuditView.vue') },
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
	} else if (to.path === '/login' && auth.isAuthenticated) {
		next('/dashboard')
	} else {
		next()
	}
})

export default router