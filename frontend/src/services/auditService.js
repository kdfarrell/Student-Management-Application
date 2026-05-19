import api from './api'

export const auditService = {

	getAudits(params = {}) {
		return api.get('audit/', { params })
	},

	getAudit(id) {
		return api.get(`audit/${id}/`)
	},

}
