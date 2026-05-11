<script setup>
import { ref, watch } from 'vue'
import { useStudentStore } from '@/stores/students.js'

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'

const props = defineProps({
    student: {
        type: Object,
        default: null
    },
    open: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:open'])

const studentStore = useStudentStore()

const form = ref({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    date_of_birth: '',
    is_active: true,
})

const errors = ref({})

// When editing, pre-fill the form with the student's data
watch(() => props.student, (student) => {
    if (student) {
        form.value = {
            first_name: student.first_name,
            last_name: student.last_name,
            email: student.email,
            phone_number: student.phone_number,
            date_of_birth: student.date_of_birth,
            is_active: student.is_active,
        }
    } else {
        form.value = {
            first_name: '',
            last_name: '',
            email: '',
            phone_number: '',
            date_of_birth: '',
            is_active: true,
        }
    }
})

function validate() {
    errors.value = {}
    if (!form.value.first_name) errors.value.first_name = 'First name is required'
    if (!form.value.last_name) errors.value.last_name = 'Last name is required'
    if (!form.value.email) errors.value.email = 'Email is required'
    return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
    if (!validate()) return

    if (props.student) {
        await studentStore.updateStudent(props.student.id, form.value)
    } else {
        await studentStore.createStudent(form.value)
    }

    emit('update:open', false)
}
</script>

<template>
    <Dialog :open="open" @update:open="emit('update:open', $event)">
        <DialogContent class="overflow-y-auto max-h-[90vh]">
            <DialogHeader>
                <DialogTitle>{{ student ? 'Edit Student' : 'Add Student' }}</DialogTitle>
            </DialogHeader>

            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label>First Name</Label>
                    <Input v-model="form.first_name" placeholder="First name" />
                    <span v-if="errors.first_name" class="text-sm text-red-500">{{ errors.first_name }}</span>
                </div>

                <div class="grid gap-2">
                    <Label>Last Name</Label>
                    <Input v-model="form.last_name" placeholder="Last name" />
                    <span v-if="errors.last_name" class="text-sm text-red-500">{{ errors.last_name }}</span>
                </div>

                <div class="grid gap-2">
                    <Label>Email</Label>
                    <Input v-model="form.email" type="email" placeholder="Email" />
                    <span v-if="errors.email" class="text-sm text-red-500">{{ errors.email }}</span>
                </div>

                <div class="grid gap-2">
                    <Label>Phone Number</Label>
                    <Input v-model="form.phone_number" placeholder="Phone number" />
                </div>

                <div class="grid gap-2">
                    <Label>Date of Birth</Label>
                    <Input v-model="form.date_of_birth" type="date" />
                </div>
            </div>

            <div class="flex items-center justify-between">
                <Label>Active Status</Label>
                <Switch v-model="form.is_active" />
            </div>

            <DialogFooter>
                <Button variant="outline" @click="emit('update:open', false)" class="cursor-pointer">Cancel</Button>
                <Button @click="handleSubmit" class="cursor-pointer">{{ student ? 'Save Changes' : 'Add Student' }}</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>