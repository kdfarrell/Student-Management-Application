export async function getApiErrorMessage(error, fallback = 'Something went wrong.') {
	const data = error?.response?.data

	if (data instanceof Blob) {
		try {
			const json = JSON.parse(await data.text())
			return json.error || json.detail || json.message || fallback
		} catch {
			return fallback
		}
	}

	if (typeof data === 'object' && data !== null) {
		return data.error || data.detail || data.message || fallback
	}

	return error?.message || fallback
}
