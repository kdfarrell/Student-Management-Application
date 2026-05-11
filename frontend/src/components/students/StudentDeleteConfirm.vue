<script setup>
import { useStudentStore } from '@/stores/students.js'

import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/components/ui/alert-dialog'

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

async function handleDelete() {
    await studentStore.deleteStudent(props.student.id)
    emit('update:open', false)
}
</script>

<template>
    <AlertDialog :open="open" @update:open="emit('update:open', $event)">
        <AlertDialogContent>
            <AlertDialogHeader>
                <AlertDialogTitle>Delete Student</AlertDialogTitle>
                <AlertDialogDescription>
                    Are you sure you want to delete
                    <span class="font-medium text-foreground">
                        {{ student?.first_name }} {{ student?.last_name }}
                    </span>?
                    This action cannot be undone.
                </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
                <AlertDialogCancel class="cursor-pointer" @click="emit('update:open', false)">
                    Cancel
                </AlertDialogCancel>
                <AlertDialogAction
                    class="cursor-pointer bg-red-600 hover:bg-red-700"
                    @click="handleDelete"
                >
                    Delete
                </AlertDialogAction>
            </AlertDialogFooter>
        </AlertDialogContent>
    </AlertDialog>
</template>