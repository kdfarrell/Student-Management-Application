import api from './api'

export const scheduleService = {

    getSchedules(params = {}) {
        return api.get('sessions/', { params })
    },

    getSchedule(id) {
        return api.get(`sessions/${id}/`)
    },

    createSchedule(data) {
        return api.post('sessions/', data)
    },

    updateSchedule(id, data) {
        return api.patch(`sessions/${id}/`, data)
    },

    deleteSchedule(id) {
        return api.delete(`sessions/${id}/`)
    }
}

export default scheduleService