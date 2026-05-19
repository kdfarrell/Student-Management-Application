export function formatAuditDetailPreview(detail, maxLength = 72) {
	if (!detail) return '—'
	if (typeof detail === 'string') return detail
	if (typeof detail === 'object') {
		const text = Object.entries(detail)
			.map(([key, value]) => `${key}: ${value}`)
			.join(' · ')
		return text.length > maxLength ? `${text.slice(0, maxLength)}…` : text
	}
	return String(detail)
}

export function formatAuditDetailFull(detail) {
	if (!detail) return '—'
	if (typeof detail === 'string') return detail
	if (typeof detail === 'object') {
		return Object.entries(detail)
			.map(([key, value]) => `${key}: ${value}`)
			.join('\n')
	}
	return JSON.stringify(detail, null, 2)
}
