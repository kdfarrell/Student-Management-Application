<script setup>
import AttendanceReportForm from '@/components/reports/AttendanceReportForm.vue'
import CourseReportForm from '@/components/reports/CourseReportForm.vue'
import GradeReportForm from '@/components/reports/GradeReportForm.vue'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BookOpen, CalendarCheck, FileText } from 'lucide-vue-next'
</script>

<template>
	<div class="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
		<!-- Header -->
		<div class="space-y-2">
			<h1 class="text-2xl sm:text-3xl font-bold text-slate-900">
				Reports
			</h1>
			<p class="text-slate-500 text-sm sm:text-base">
				Generate and export PDF reports for students and courses.
			</p>
		</div>

		<!-- Reports Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">

			<!-- Grade Report -->
			<Card class="hover:shadow-md transition-shadow">
				<CardHeader>
					<div class="flex items-start gap-4">
						<div class="bg-blue-100 text-blue-600 p-3 rounded-xl flex-shrink-0">
							<FileText class="w-6 h-6" />
						</div>
						<div>
							<CardTitle class="text-lg">Student Grade Report</CardTitle>
							<CardDescription class="mt-1">
								Individual student grades with weighted averages across subjects
							</CardDescription>
						</div>
					</div>
				</CardHeader>
				<CardContent>
					<GradeReportForm />
				</CardContent>
			</Card>

			<!-- Attendance Report -->
			<Card class="hover:shadow-md transition-shadow">
				<CardHeader>
					<div class="flex items-start gap-4">
						<div class="bg-green-100 text-green-600 p-3 rounded-xl flex-shrink-0">
							<CalendarCheck class="w-6 h-6" />
						</div>
						<div>
							<CardTitle class="text-lg">Student Attendance Report</CardTitle>
							<CardDescription class="mt-1">
								Detailed session-by-session attendance breakdown
							</CardDescription>
						</div>
					</div>
				</CardHeader>
				<CardContent>
					<AttendanceReportForm />
				</CardContent>
			</Card>

			<!-- Course Grade Report -->
			<Card class="hover:shadow-md transition-shadow">
				<CardHeader>
					<div class="flex items-start gap-4">
						<div class="bg-purple-100 text-purple-600 p-3 rounded-xl flex-shrink-0">
							<BookOpen class="w-6 h-6" />
						</div>
						<div>
							<CardTitle class="text-lg">Course Grade Report</CardTitle>
							<CardDescription class="mt-1">
								Performance overview of all students in a course
							</CardDescription>
						</div>
					</div>
				</CardHeader>
				<CardContent>
					<CourseReportForm />
				</CardContent>
			</Card>

		</div>
	</div>
</template>
