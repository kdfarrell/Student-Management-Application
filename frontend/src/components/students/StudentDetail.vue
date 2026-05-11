<script setup>
import {
    Sheet,
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetDescription,
} from '@/components/ui/sheet'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { User, Mail, Phone, Calendar, CalendarCheck } from 'lucide-vue-next'

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

function capitalize(str) {
    if (!str) return ''
    return str.charAt(0).toUpperCase() + str.slice(1)
}

function formatDate(dateString) {
    if (!dateString) return '—'
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })
}
</script>

<template>
    <Sheet :open="open" @update:open="emit('update:open', $event)">
        <SheetContent class="w-full sm:max-w-md overflow-y-auto">

            <SheetHeader class="pb-0">
                <div class="flex items-center gap-4">
                    <div>
                        <SheetTitle class="text-xl">
                            {{ capitalize(student?.first_name) }} {{ capitalize(student?.last_name) }}
                        </SheetTitle>
                        <SheetDescription class="mt-1">
                            <Badge :class="student?.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" variant="secondary">
                                {{ student?.is_active ? 'Active' : 'Inactive' }}
                            </Badge>
                        </SheetDescription>
                    </div>
                </div>
            </SheetHeader>

            <Separator/>

            <div class="flex flex-col gap-5 px-4">
                <div class="flex items-center gap-3">
                    <div class="h-9 w-9 rounded-md bg-neutral-100 flex items-center justify-center shrink-0">
                        <Mail class="w-4 h-4 text-neutral-500" />
                    </div>
                    <div>
                        <p class="text-xs text-muted-foreground">Email</p>
                        <p class="text-sm font-medium">{{ student?.email || '—' }}</p>
                    </div>
                </div>

                <div class="flex items-center gap-3">
                    <div class="h-9 w-9 rounded-md bg-neutral-100 flex items-center justify-center shrink-0">
                        <Phone class="w-4 h-4 text-neutral-500" />
                    </div>
                    <div>
                        <p class="text-xs text-muted-foreground">Phone Number</p>
                        <p class="text-sm font-medium">{{ student?.phone_number || '—' }}</p>
                    </div>
                </div>

                <div class="flex items-center gap-3">
                    <div class="h-9 w-9 rounded-md bg-neutral-100 flex items-center justify-center shrink-0">
                        <Calendar class="w-4 h-4 text-neutral-500" />
                    </div>
                    <div>
                        <p class="text-xs text-muted-foreground">Date of Birth</p>
                        <p class="text-sm font-medium">{{ formatDate(student?.date_of_birth) }}</p>
                    </div>
                </div>

                <div class="flex items-center gap-3">
                    <div class="h-9 w-9 rounded-md bg-neutral-100 flex items-center justify-center shrink-0">
                        <CalendarCheck class="w-4 h-4 text-neutral-500" />
                    </div>
                    <div>
                        <p class="text-xs text-muted-foreground">Enrollment Date</p>
                        <p class="text-sm font-medium">{{ formatDate(student?.enrollment_date) }}</p>
                    </div>
                </div>
            </div>

            <Separator/>

            <div class="px-4">
                <p class="text-sm font-medium mb-2">Enrolled Courses</p>
                <p class="text-sm text-muted-foreground">Coming soon.</p>
            </div>

        </SheetContent>
    </Sheet>
</template>