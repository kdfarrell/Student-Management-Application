<script setup>
import { useCourseStore } from '@/stores/courses.js'
import { ref, watch } from 'vue'

import { Button } from '@/components/ui/button'
import {
	Dialog,
	DialogContent,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { toast } from 'vue-sonner'

const props = defineProps({
	course: { type: Object, default: null },
	open: { type: Boolean, default: false }
})

const emit = defineEmits(['update:open', 'saved'])

const courseStore = useCourseStore()

const form = ref({
	name: props.course?.name || "",
	description: props.course?.description || "",
	is_active: props.course !== null ? props.course.is_active : true,
})

const errors = ref({})

watch(() => props.open, (open) => {
	if (open && !props.course) {
		form.value = {
			name: "",
			description: "",
			is_active: true,
		}
	}
	if (open && props.course) {
		form.value = {
			name: props.course.name,
			description: props.course.description,
			is_active: props.course.is_active,
		}
	}
})

function validate() {
	errors.value = {}
	if (!form.value.name) errors.value.name = 'Name is required'
	if (!form.value.description) errors.value.description = 'Description is required'
	return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
	if (!validate()) return

	try {
		if (props.course) {
			await courseStore.updateCourse(props.course.id, form.value)
			toast.success('Course updated successfully.')
		} else {
			await courseStore.createCourse(form.value)
			toast.success('Course created successfully.')
		}
		emit('saved')
		emit('update:open', false)
	} catch {
		toast.error('Failed to save course.')
	}
}

</script>

<template>
	<Dialog :open="open" @update:open="emit('update:open', $event)">

		<DialogContent class="overflow-y-auto max-h-[90vh]">

			<DialogHeader>
				<DialogTitle>{{ course ? 'Edit course' : 'Add course' }}</DialogTitle>
			</DialogHeader>

			<div class="grid gap-4 py-4">
				<div class="grid gap-2">
					<Label>Name</Label>
					<Input v-model="form.name" placeholder="Course Name" />
					<span v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</span>
				</div>

				<div class="grid gap-2">
					<Label>Description</Label>
					<Input v-model="form.description" placeholder="Description" />
					<span v-if="errors.description" class="text-sm text-red-500">{{ errors.description }}</span>
				</div>
			</div>

			<div class="flex items-center justify-between">
				<Label>Active Status</Label>
				<Switch :model-value="form.is_active" @update:model-value="form.is_active = $event" />
			</div>

			<DialogFooter>
				<Button variant="outline" @click="emit('update:open', false)" class="cursor-pointer">Cancel</Button>
				<Button @click="handleSubmit" class="cursor-pointer">{{ course ? 'Save Changes' : 'Add course'
					}}</Button>
			</DialogFooter>

		</DialogContent>

	</Dialog>

</template>
