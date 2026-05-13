import api from './api'

export const studentService = {

    getStudents(params = {}) {
        return api.get('students/', { params })
    },

    getStudent(id) {
        return api.get(`students/${id}/`) 
    },

    createStudent(data) {
        return api.post('students/', data)
    },

    updateStudent(id, data) {
        return api.patch(`students/${id}/`, data)
    },

    deleteStudent(id) {
        return api.delete(`students/${id}/`)
    },

}