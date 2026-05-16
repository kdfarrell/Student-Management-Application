import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {

	state: () => ({
		token: localStorage.getItem('token') || null,
		refreshToken: localStorage.getItem("refreshToken") || null,
		teacher: (() => {
			try {
				return JSON.parse(localStorage.getItem('teacher') || 'null')
			} catch {
				return null
			}
		})(),

	}),

	getters: {
		isAuthenticated: (state) => !!state.token,
	},

	actions: {
		login(data) {
			this.token = data.access
			this.refreshToken = data.refresh
			this.teacher = { username: data.username, school_name: data.school_name }

			localStorage.setItem('token', data.access)
			localStorage.setItem('refreshToken', data.refresh)
			localStorage.setItem('teacher', JSON.stringify({ username: data.username, school_name: data.school_name }))
		},

		logout() {
			this.token = null
			this.refreshToken = null
			this.teacher = null

			localStorage.removeItem('token')
			localStorage.removeItem('refreshToken')
			localStorage.removeItem('teacher')
		},

		setToken(access) {
			this.token = access
			localStorage.setItem('token', access)
		},
	},
})