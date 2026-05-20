<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api.js'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const username = ref('')
const email = ref('')
const schoolName = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()

async function handleRegister() {
	loading.value = true
	error.value = ''

	try {
		await api.post('auth/register/', {
			username: username.value,
			email: email.value,
			school_name: schoolName.value,
			password: password.value,
		})
		router.push('/login')
	}
	catch {
		error.value = 'Registration failed. Please try again.'
	}
	finally {
		loading.value = false
	}
}
</script>

<template>
	<Card class="m-2">
		<CardHeader>
			<CardTitle>Register</CardTitle>
		</CardHeader>
		<CardContent>
			<div class="flex flex-col gap-4">
				<div>
					<Label for="username">Username</Label>
					<Input id="username" v-model="username" type="text" placeholder="Enter username" class="mt-2" />
				</div>
				<div>
					<Label for="email">Email</Label>
					<Input id="email" v-model="email" type="email" placeholder="Enter email" class="mt-2" />
				</div>
				<div>
					<Label for="school_name">School Name</Label>
					<Input id="school_name" v-model="schoolName" type="text" placeholder="Enter school name"
						class="mt-2" />
				</div>
				<div>
					<Label for="password">Password</Label>
					<Input id="password" v-model="password" type="password" placeholder="Enter password" class="mt-2"
						@keyup.enter="handleRegister" />
				</div>
				<div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
				<Button :disabled="loading" @click="handleRegister">
					{{ loading ? 'Registering...' : 'Register' }}
				</Button>
				<p class="text-sm text-center text-neutral-500">
					Already have an account?
					<router-link to="/login" class="text-primary underline">Login</router-link>
				</p>
			</div>
		</CardContent>
	</Card>
</template>