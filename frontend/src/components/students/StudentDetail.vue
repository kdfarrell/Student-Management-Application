<script setup>
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
} from '@/components/ui/sheet'
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table'
import { useCourseStore } from '@/stores/courses'
import attendanceService from '@/services/attendanceService'
import { Calendar, CalendarCheck, Mail, Phone } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'

import StudentGradeSummary from '@/components/grades/StudentGradeSummary.vue'

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
const courseStore = useCourseStore()

const summary = ref([])
const loadingSummary = ref(false)

const studentEnrollments = computed(() => {
    if (!props.student?.id || !courseStore.enrollments) return []
    return courseStore.enrollments.filter(e => {
        const studentIdFromEnrollment = e.student?.id || e.student
        return Number(studentIdFromEnrollment) === Number(props.student.id)
    })
})

watch(() => props.open, async (val) => {
    if (val && props.student?.id) {
        loadingSummary.value = true
        try {
            const res = await attendanceService.getAttendanceSummary(props.student.id)
            summary.value = res.data
        } finally {
            loadingSummary.value = false
        }
    }
})

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
                            <Badge
                                :class="student?.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                                variant="secondary">
                                {{ student?.is_active ? 'Active' : 'Inactive' }}
                            </Badge>
                        </SheetDescription>
                    </div>
                </div>
            </SheetHeader>

            <Separator />

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

            <Separator />

            <div class="px-4">
                <p class="text-sm font-medium mb-3">Enrolled Courses</p>

                <div v-if="studentEnrollments.length === 0" class="text-sm text-muted-foreground italic">
                    No active enrollments found.
                </div>

                <div v-else class="space-y-2">
                    <div v-for="enrollment in studentEnrollments" :key="enrollment.id"
                        class="flex items-center justify-between p-3 rounded-lg border bg-neutral-50/50">
                        <div>
                            <p class="text-sm font-semibold">{{ enrollment.course_name }}</p>
                            <p class="text-[11px] text-muted-foreground">
                                Enrolled: {{ formatDate(enrollment.date_enrolled) }}
                            </p>
                        </div>

                        <Badge variant="outline" class="text-[10px] capitalize"
                            :class="(enrollment.status === 'active' && enrollment.course_is_active !== false) ? 'text-green-600 border-green-200' : 'text-red-600 border-red-200'">
                            {{ (enrollment.status === 'active' && enrollment.course_is_active !== false) ? 'Active' : 'Inactive' }}
                        </Badge>
                    </div>
                </div>
            </div>

            <Separator />

            <div class="px-4">
                <p class="text-sm font-medium mb-3">Attendance Summary</p>

                <div v-if="loadingSummary" class="text-sm text-muted-foreground italic">Loading...</div>

                <div v-else-if="summary.length === 0" class="text-sm text-muted-foreground italic">
                    No attendance records found.
                </div>

                <Table v-else>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Course</TableHead>
                            <TableHead>Sessions</TableHead>
                            <TableHead>Present</TableHead>
                            <TableHead>%</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        <TableRow v-for="s in summary" :key="s.course">
                            <TableCell>{{ s.course }}</TableCell>
                            <TableCell>{{ s.total_sessions }}</TableCell>
                            <TableCell>{{ s.present }}</TableCell>
                            <TableCell>
                                <Badge :class="s.percentage >= 75 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" variant="secondary">
                                    {{ s.percentage }}%
                                </Badge>
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>

            <Separator />

            <div class="px-4 mb-4">
                <p class="text-sm font-medium mb-3">Grade Summary</p>
                <StudentGradeSummary v-if="student?.id" :student-id="student.id" />
            </div>
        </SheetContent>
    </Sheet>
</template>