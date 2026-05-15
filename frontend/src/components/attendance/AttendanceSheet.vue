<script setup>
import { ref, watch, computed } from 'vue'
import { useCourseStore } from '@/stores/courses'
import { useAttendanceStore } from '@/stores/attendance' // Import your pre-made attendance store
import { toast } from 'vue-sonner'

import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetFooter,
} from '@/components/ui/sheet'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'

const props = defineProps({
  open: { type: Boolean, required: true },
  session: { type: Object, default: null }
})

const emit = defineEmits(['update:open', 'refresh'])

// Core Stores Injection
const courseStore = useCourseStore()
const attendanceStore = useAttendanceStore() // Wired directly to your custom pinia store instance

const isSubmitting = ref(false)
const attendanceRecords = ref([])

// Filters courseStore.enrollments to gather students linked to this specific class session's course parent
const filteredStudents = computed(() => {
  if (!props.session) return []
  
  const sessionCourseId = props.session.course || props.session.subject?.course
  const sessionCourseName = props.session.course_name || props.session.subject?.course_name
  
  return courseStore.enrollments.filter(enrollment => {
    if (enrollment.status !== 'active') return false

    const courseIdMatches = sessionCourseId && enrollment.course === sessionCourseId
    const courseNameMatches = sessionCourseName && enrollment.course_name === sessionCourseName
    
    return courseIdMatches || courseNameMatches
  })
})

// Build or fetch reactive working rows when sheet changes visibility state
watch(() => props.open, async (isOpen) => {
  if (isOpen && props.session) {
    try {
      // 1. Fetch saved lines from Django
      await attendanceStore.fetchAttendanceBySession(props.session.id)
    } catch (err) {
      console.error("Failed to pre-fetch existing session records:", err)
    }

    // 2. Safely capture arrays across direct lists or paginated result objects
    const savedRecords = Array.isArray(attendanceStore.attendance) 
      ? attendanceStore.attendance 
      : (attendanceStore.attendance?.results || [])

    // 3. Map your student data grid rows cleanly
    attendanceRecords.value = filteredStudents.value.map(item => {
      const studentEntity = item.student && typeof item.student === 'object' ? item.student : item
      
      // Match records by locating either flat numbers or nested serializer structural keys
      const existingRecord = savedRecords.find(record => {
        const recordStudentId = record.student_id || record.student?.id
        return Number(recordStudentId) === Number(studentEntity.id)
      })

      return {
        student_id: studentEntity.id,
        first_name: studentEntity.first_name,
        last_name: studentEntity.last_name,
        email: studentEntity.email,
        // Bind existing status if found, otherwise default to baseline 'present' rule
        status: existingRecord?.status ? existingRecord.status : 'present', 
        notes: existingRecord?.notes ? existingRecord.notes : ''
      }
    })
  }
})

const closeSheet = () => {
  emit('update:open', false)
}

const submitAttendance = async () => {
  if (!props.session) return
  isSubmitting.value = true
  
  try {
    const payload = {
      attendance: attendanceRecords.value.map(record => ({
        student_id: record.student_id,
        session_id: props.session.id,
        status: record.status,
        notes: record.notes || ''
      }))
    }
    
    // CLEAN LAYER INTERACTION: Utilizing your store action which maps directly to your attendanceService
    await attendanceStore.bulkSubmit(payload)
    
    toast.success('Attendance batch operations processed successfully')
    emit('refresh')
    closeSheet()
  } catch (error) {
    console.error('Attendance submit transaction abort:', error)
    toast.error(error.response?.data?.message || 'Failed to sync remote records array')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Sheet :open="open" @update:open="closeSheet">
    <SheetContent class="sm:max-w-2xl overflow-y-auto">
      <SheetHeader class="pb-4 border-b">
        <SheetTitle class="text-lg font-bold text-neutral-900">
          Take Attendance: {{ session?.subject_name || 'Algebra' }}
        </SheetTitle>
        <SheetDescription class="text-xs text-neutral-500">
          Parent Course: {{ session?.course_name || 'Math' }} | Date: {{ session?.date?.split('T')[0] }}
        </SheetDescription>
      </SheetHeader>

      <!-- Empty State Handler -->
      <div v-if="attendanceRecords.length === 0" class="py-12 text-center text-sm text-neutral-400 italic">
        No active student enrollments verified for the parent course database.
      </div>

      <!-- Core Attendance Matrix Table -->
      <div v-else class="py-4">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Student</TableHead>
              <TableHead class="text-center w-72">Status Options</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="record in attendanceRecords" :key="record.student_id">
              <TableCell class="font-medium">
                <div class="text-neutral-900 font-semibold">{{ record.first_name }} {{ record.last_name }}</div>
                <div class="text-[10px] text-neutral-400 font-mono mt-0.5">{{ record.email }}</div>
              </TableCell>
              
              <TableCell>
                <!-- Shadcn RadioGroup Binding mapping options horizontally -->
                <RadioGroup 
                  v-model="record.status" 
                  class="flex items-center justify-between gap-2 bg-neutral-100 p-1.5 rounded-lg border border-neutral-200"
                >
                  <div class="flex items-center space-x-1">
                    <RadioGroupItem value="present" :id="`p-${record.student_id}`" class="text-emerald-600 focus:ring-emerald-500" />
                    <Label :for="`p-${record.student_id}`" class="text-[11px] font-bold cursor-pointer text-emerald-700">Pres</Label>
                  </div>
                  
                  <div class="flex items-center space-x-1">
                    <RadioGroupItem value="absent" :id="`a-${record.student_id}`" class="text-rose-600 focus:ring-rose-500" />
                    <Label :for="`a-${record.student_id}`" class="text-[11px] font-bold cursor-pointer text-rose-700">Abs</Label>
                  </div>
                  
                  <div class="flex items-center space-x-1">
                    <RadioGroupItem value="late" :id="`l-${record.student_id}`" class="text-amber-600 focus:ring-amber-500" />
                    <Label :for="`l-${record.student_id}`" class="text-[11px] font-bold cursor-pointer text-amber-700">Late</Label>
                  </div>
                  
                  <div class="flex items-center space-x-1">
                    <RadioGroupItem value="excused" :id="`e-${record.student_id}`" class="text-blue-600 focus:ring-blue-500" />
                    <Label :for="`e-${record.student_id}`" class="text-[11px] font-bold cursor-pointer text-blue-700">Exc</Label>
                  </div>
                </RadioGroup>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <!-- Action Footer Command Panel Bar -->
      <SheetFooter class="pt-4 border-t mt-auto sticky bottom-0 bg-white">
        <div class="flex w-full justify-end gap-3">
          <Button type="button" variant="outline" @click="closeSheet" :disabled="isSubmitting">
            Cancel
          </Button>
          <Button type="button" @click="submitAttendance" :disabled="isSubmitting || attendanceRecords.length === 0">
            {{ isSubmitting ? 'Processing Transaction...' : 'Commit Attendance Data' }}
          </Button>
        </div>
      </SheetFooter>
    </SheetContent>
  </Sheet>
</template>