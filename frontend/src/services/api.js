import axios  from 'axios'
import { useAuthStore } from "../stores/auth.js"

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/'
})

// Request Interceptor 
api.interceptors.request.use((config) => {
    const auth = useAuthStore()
    if (auth.token) {
        config.headers.Authorization = `Bearer ${auth.token}`
    }
    return config
})

// Response Interceptor 

api.interceptors.response.use((response) => response, async(error) => {
    const auth = useAuthStore()
    const original = error.config

    if (error.response?.status == 401 && !original._retry && !original.url.includes('auth/login')) {
        original._retry = true

        try {
            const res = await axios.post('http://127.0.0.1:8000/api/auth/token/refresh/', {
                refresh: auth.refreshToken,
            })
            auth.setToken(res.data.access)
            original.headers.Authorization =   `Bearer ${res.data.access}`
            return api(original)
        }
        catch {
            auth.logout()
            window.location.href = '/login'
        }
    }

    return Promise.reject(error)
})

export default api