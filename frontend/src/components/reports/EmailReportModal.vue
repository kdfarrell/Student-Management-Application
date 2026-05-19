<template>
	<Dialog :open="true" @update:open="emit('close')">
		<DialogContent class="max-w-md">
			<DialogHeader>
				<DialogTitle>Send Report via Email</DialogTitle>
				<DialogDescription>
					Sending a
					<span class="font-semibold capitalize">{{ reportType }}</span>
					report for this student.
				</DialogDescription>
			</DialogHeader>

			<div class="space-y-4 py-2">
				<div class="space-y-2">
					<Label>Recipient Email</Label>
					<Input v-model="email" type="email" placeholder="student@example.com" />
				</div>

				<Alert v-if="errorMessage" variant="destructive">
					<AlertDescription>{{ errorMessage }}</AlertDescription>
				</Alert>
			</div>

			<DialogFooter>
				<Button variant="outline" @click="emit('close')">Cancel</Button>
				<Button :disabled="!email || sending" @click="handleSend">
					<Send class="w-4 h-4 mr-2" />
					{{ sending ? 'Sending...' : 'Send Report' }}
				</Button>
			</DialogFooter>
		</DialogContent>
	</Dialog>
</template>

<script setup>
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useReportsStore } from '@/stores/reports'
import { getApiErrorMessage } from '@/utils/apiError'
import { Send } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
	studentId: { type: String, required: true },
	courseId: { type: String, default: null },
	reportType: { type: String, required: true },
	studentEmail: { type: String, default: '' },
})

const emit = defineEmits(['close'])
const reportsStore = useReportsStore()
const email = ref('')
const sending = ref(false)
const errorMessage = ref('')

onMounted(() => {
	email.value = props.studentEmail
})

async function handleSend() {
	sending.value = true
	errorMessage.value = ''
	try {
		await reportsStore.sendEmailReport({
			student_id: props.studentId,
			course_id: props.courseId,
			report_type: props.reportType,
			recipient_email: email.value,
		})
		toast.success('Report sent successfully!')
		emit('close')
	} catch (err) {
		errorMessage.value = await getApiErrorMessage(err, 'Failed to send email.')
		toast.error(errorMessage.value)
	} finally {
		sending.value = false
	}
}
</script>
