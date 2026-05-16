import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

import DashboardView from '@/views/dashboard/DashboardView.vue'
import GradesView from '@/views/grades/GradesView.vue'
import AppLayout from '../layouts/AppLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'
import Attendance from '../views/attendance/AttendanceView.vue'
import LoginView from '../views/auth/LoginView.vue'
import CourseDetail from '../views/courses/CourseDetail.vue'
import CoursesView from '../views/courses/CoursesView.vue'
import Schedule from '../views/schedule/Schedule.vue'
import StudentsView from '../views/students/StudentsView.vue'

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
				component: DashboardView
			},
			{
				path: 'students',
				component: StudentsView
			},
			{
				path: 'courses',
				component: CoursesView
			},
			{
				path: 'courses/:id',
				component: CourseDetail
			},
			{
				path: 'schedule',
				component: Schedule
			},
			{
				path: 'attendance',
				component: Attendance
			},
			{
				path: 'grades',
				component: GradesView
			},
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