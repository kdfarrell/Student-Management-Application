<script setup>
import { ref, watch } from 'vue'
import { useCourseStore } from '@/stores/courses.js'
import { useRoute } from 'vue-router'

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
import { toast } from 'vue-sonner'

const props = defineProps({
    subject: { type: Object, default: null },
    open: { type: Boolean, default: false }
})

const emit = defineEmits(['update:open', 'saved'])

const courseStore = useCourseStore()
const route = useRoute()


const form = ref({
    name: props.subject?.name || '',
    description: props.subject?.description || '',
    weight: props.subject?.weight || '',
    course: props.subject?.course || null
})

const errors = ref({})

watch(() => props.open, (open) => {
    if (open && !props.subject) {
        form.value = {
            name: '',
            description: '',
            weight: '',
            course: null
        }
    }
    if (open && props.subject) {
        form.value = {
            name: props.subject.name,
            description: props.subject.description,
            weight: props.subject.weight,
            course: props.subject.course
        }
    }
})



function validate() {
    errors.value = {}
    if (!form.value.name) errors.value.name = 'Name is required'
    if (!form.value.description) errors.value.description = 'Description is required'
    if (!form.value.weight) errors.value.weight = 'Weight is required'
    return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
    if (!validate()) return

    form.value.course = route.params.id

    try {
        if (props.subject) {
            await courseStore.updateSubject(props.subject.id, form.value)
            toast.success('Subject updated successfully.')
        } else {
            await courseStore.createSubject(form.value)
            toast.success('Subject added successfully.')
        }
        emit('saved')
        emit('update:open', false)
    } catch {
        toast.error('Failed to save subject.')
    }
}
</script>

<template>
    <Dialog :open="open" @update:open="emit('update:open', $event)">
        <DialogContent>
            <DialogHeader>
                <DialogTitle>{{ subject ? 'Edit Subject' : 'Add Subject' }}</DialogTitle>
            </DialogHeader>

            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label>Name</Label>
                    <Input v-model="form.name" placeholder="Subject name" />
                    <span v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</span>
                </div>

                <div class="grid gap-2">
                    <Label>Description</Label>
                    <Input v-model="form.description" placeholder="Description" />
                    <span v-if="errors.description" class="text-sm text-red-500">{{ errors.description }}</span>
                </div>

                <div class="grid gap-2">
                    <Label>Weight (e.g. 0.30 for 30%)</Label>
                    <Input v-model="form.weight" type="number" step="0.01" min="0" max="1" placeholder="0.00" />
                    <span v-if="errors.weight" class="text-sm text-red-500">{{ errors.weight }}</span>
                </div>
            </div>

            <DialogFooter>
                <Button variant="outline" class="cursor-pointer" @click="emit('update:open', false)">Cancel</Button>
                <Button class="cursor-pointer" @click="handleSubmit">{{ subject ? 'Save Changes' : 'Add Subject' }}</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>