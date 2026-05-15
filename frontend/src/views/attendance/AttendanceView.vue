<script setup>
import { ref, onMounted } from 'vue'
import { useScheduleStore } from '@/stores/scheduling'
import { useCourseStore } from '@/stores/courses'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import AttendanceSheet from '@/components/attendance/AttendanceSheet.vue'

const scheduleStore = useScheduleStore()
const courseStore = useCourseStore()

const isSheetOpen = ref(false)
const selectedSession = ref(null)

onMounted(async () => {
  try {
    // Parallel load schedule sessions and course enrollment rosters
    await Promise.all([
      scheduleStore.fetchSchedules(),
      courseStore.fetchEnrollments()
    ])
  } catch (error) {
    console.error('Failed to load initial attendance dependencies:', error)
  }
})

const openAttendanceSheet = (session) => {
  selectedSession.value = session
  isSheetOpen.value = true
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return new Date(`1970-01-01T${timeStr}`).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <p class="text-sm text-muted-foreground">Select a class session below to log or modify student attendance metrics.</p>
    </div>

    <!-- Active Class Sessions Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card 
        v-for="session in scheduleStore.schedules" 
        :key="session.id"
        class="hover:shadow-md transition-all cursor-pointer border-neutral-200"
        @click="openAttendanceSheet(session)"
      >
        <CardHeader class="pb-3 flex flex-row items-start justify-between space-y-0">
          <div>
            <!-- Custom API fallback checks for course and subject fields -->
            <CardTitle class="text-base font-bold text-neutral-900">
              {{ session.subject_name || session.subject?.name || 'Algebra' }}
            </CardTitle>
            <p class="text-xs font-medium text-neutral-500 mt-1">
              Course: {{ session.course_name || session.subject?.course_name || 'Math' }}
            </p>
          </div>
          <!-- Verification badge block -->
          <Badge :variant="session.attendance_recorded ? 'default' : 'secondary'" class="text-[10px] uppercase font-bold tracking-wider">
            {{ session.attendance_recorded ? 'Recorded' : 'Not Recorded' }}
          </Badge>
        </CardHeader>
        
        <CardContent class="text-xs text-neutral-600 space-y-1.5">
          <div class="flex items-center gap-2">
            <span class="font-semibold text-neutral-400">Date:</span>
            <span>{{ session.date ? session.date.split('T')[0] : 'N/A' }}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="font-semibold text-neutral-400">Time:</span>
            <span>{{ formatTime(session.start_time) }} - {{ formatTime(session.end_time) }}</span>
          </div>
          <div v-if="session.room" class="flex items-center gap-2">
            <span class="font-semibold text-neutral-400">Room:</span>
            <span>{{ session.room }}</span>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Right Slide-Over Panel Container Anchor -->
    <AttendanceSheet 
      v-model:open="isSheetOpen" 
      :session="selectedSession"
      @refresh="() => { scheduleStore.fetchSchedules(); triggerSuccessNotification(); }"
    />
  </div>
</template>