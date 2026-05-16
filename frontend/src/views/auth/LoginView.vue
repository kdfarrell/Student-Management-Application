<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api.js'
import { useAuthStore } from '../../stores/auth.js'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const auth = useAuthStore()

async function handleLogin() {
	loading.value = true
	error.value = ''

	try {
		const res = await api.post('auth/login/', {
			username: username.value,
			password: password.value,
		})
		auth.login(res.data)
		router.push('/dashboard')
	}
	catch {
		error.value = 'Invalid username or password'
	}
	finally {
		loading.value = false
	}
}

</script>


<template>
	<Card class="m-2">
		<CardHeader>
			<CardTitle>Login</CardTitle>
		</CardHeader>

		<CardContent>
			<div class="flex flex-col gap-4">
				<div>
					<Label for="username">Username</Label>
					<Input id="username" v-model="username" type="text" placeholder="Enter username" class="mt-2" />
				</div>
				<div>
					<Label for="password">Password</Label>
					<Input id="password" v-model="password" type="password" placeholder="Enter password" class="mt-2"
						@keyup.enter="handleLogin" />
				</div>

				<div v-if="error" class="text-red-500 text-sm">
					{{ error }}
				</div>

				<Button :disabled="loading" @click="handleLogin">
					{{ loading ? 'Logging in...' : 'Login' }}
				</Button>

			</div>

		</CardContent>
	</Card>
</template>