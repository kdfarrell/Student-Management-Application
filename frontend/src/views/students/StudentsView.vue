<script setup>
import {
  Table, TableBody, TableCell,
  TableHead, TableHeader, TableRow
} from "@/components/ui/table";

import { Button } from '@/components/ui/button';

import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationNext,
  PaginationPrevious
} from '@/components/ui/pagination';

import { useStudentStore } from "@/stores/students.js";
// 1. Import the Course Store to get enrollment data
import { useCourseStore } from "@/stores/courses.js"; 
import { SquarePen, Trash2, Eye } from "lucide-vue-next";

import { onMounted, ref } from 'vue';

import StudentModal from "@/components/students/StudentModal.vue";
import StudentDeleteConfirm from "@/components/students/StudentDeleteConfirm.vue";
import StudentDetail from "@/components/students/StudentDetail.vue";

const studentStore = useStudentStore()
// 2. Initialize the Course Store
const courseStore = useCourseStore() 

onMounted(async () => {
  await studentStore.fetchStudents()
})

const selectedStudent = ref(null)
const openModal = ref(false)
const openDelete = ref(false)
const openDetail = ref(false)

// 3. New function to load data BEFORE opening the sheet
async function handleViewDetail(student) {
  selectedStudent.value = student
  // This fetches the enrollments so the Detail sheet has data to show
  await courseStore.fetchEnrollments() 
  openDetail.value = true
}

function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(dateString) {
  if (!dateString) return '—';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<template>
  <div class="flex mb-4">
    <Button class="cursor-pointer" @click="selectedStudent = null; openModal = true">
      Add Student
    </Button>
  </div>

  <Table>
    <TableHeader>
      <TableRow>
        <TableHead class="w-40">Name</TableHead>
        <TableHead class="w-42">Email</TableHead>
        <TableHead class="w-30 text-center">Phone Number</TableHead>
        <TableHead class="w-30 text-center">Enrolled</TableHead>
        <TableHead class="w-30 text-center">Status</TableHead>
        <TableHead class="w-30 text-center">Actions</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="student in studentStore.students" :key="student.id">
        <TableCell class="font-medium">
          {{ capitalize(student.first_name) }} {{ capitalize(student.last_name) }}
        </TableCell>
        <TableCell>{{ student.email }}</TableCell>
        <TableCell class="text-center">{{ student.phone_number }}</TableCell>
        <TableCell class="text-center">{{ formatDate(student.enrollment_date) }}</TableCell>
        <TableCell class="text-center">
          <div class="flex justify-center">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping-slow absolute inline-flex h-full w-full rounded-full opacity-75"
                :class="student.is_active ? 'bg-green-400' : 'bg-red-400'"></span>
              <span class="relative inline-flex rounded-full h-2 w-2"
                :class="student.is_active ? 'bg-green-500' : 'bg-red-500'"></span>
            </span>
          </div>
        </TableCell>
        <TableCell>
          <div class="flex items-center justify-center gap-2">

            <button
              class="p-1 hover:text-blue-500 transition-colors cursor-pointer"
              @click="handleViewDetail(student)"
            >
              <Eye class="w-4 h-4" />
            </button>
            <button
              class="p-1 hover:text-yellow-500 transition-colors cursor-pointer"
              @click="selectedStudent = student; openModal = true"
            >
              <SquarePen class="w-4 h-4" />
            </button>
            <button
              class="p-1 hover:text-red-500 transition-colors cursor-pointer"
              @click="selectedStudent = student; openDelete = true"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </TableCell>
      </TableRow>
    </TableBody>
  </Table>

  <div class="flex items-center justify-end mt-4">
    <Pagination
      v-slot="{ page }"
      :total="studentStore.count"
      :items-per-page="studentStore.pageSize || 10"
      :page="studentStore.currentPage"
      @update:page="studentStore.goToPage($event)"
    >
      <PaginationContent v-slot="{ items }">
        <PaginationPrevious class="cursor-pointer" />
        <template v-for="(item, index) in items" :key="index">
          <PaginationItem v-if="item.type === 'page'" :value="item.value" :is-active="item.value === page" class="cursor-pointer">
            {{ item.value }}
          </PaginationItem>
        </template>
        <PaginationNext class="cursor-pointer"/>
      </PaginationContent>
    </Pagination>
  </div>

  <StudentModal
    :student="selectedStudent"
    :open="openModal"
    @update:open="openModal = $event"
  />

  <StudentDeleteConfirm
    :student="selectedStudent"
    :open="openDelete"
    @update:open="openDelete = $event"
  />

  <StudentDetail
    :student="selectedStudent"
    :open="openDetail"
    @update:open="openDetail = $event"
  />
</template>