<script setup>
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useDashboardStore } from '@/stores/dashboard'
import {
    ArcElement,
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    Title, Tooltip,
} from 'chart.js'
import { BookOpen, CalendarDays, ChevronRight, TriangleAlert, Users } from 'lucide-vue-next'
import { computed, onMounted } from 'vue'
import { Bar, Doughnut } from 'vue-chartjs'
import { RouterLink } from 'vue-router'

ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale)

// Store 
const dashboardStore = useDashboardStore()
onMounted(() => dashboardStore.fetchDashboard())

// Derived state 
const stats = computed(() => dashboardStore.stats)
const atRiskList = computed(() => dashboardStore.atRiskList ?? [])
const gradeRanges = computed(() => dashboardStore.gradeRanges)
const courseAttendance = computed(() => dashboardStore.attendanceOverview ?? [])

// Chart data colors
const GRADE_BAND_COLORS = [
    'rgba(248,113,113,0.85)',
    'rgba(251,146,60,0.85)',
    'rgba(96,165,250,0.85)',
    'rgba(74,222,128,0.85)',
]

const assessmentChartData = computed(() => {
    if (!dashboardStore.assessmentDistribution) return null
    const { test, assignment, exam, quiz } = dashboardStore.assessmentDistribution
    return {
        labels: ['Tests', 'Assignments', 'Exams', 'Quizzes'],
        datasets: [{
            data: [test, assignment, exam, quiz],
            backgroundColor: [
                'rgba(99, 102, 241, 0.85)',  // Indigo
                'rgba(16, 185, 129, 0.85)',  // Emerald
                'rgba(139, 92, 246, 0.85)',  // Violet
                'rgba(245, 158, 11, 0.85)',   // Amber
            ],
            borderWidth: 0,
            hoverOffset: 5,
        }],
    }
})

const gradeBandLegend = [
    { label: '0-49', color: GRADE_BAND_COLORS[0] },
    { label: '50-69', color: GRADE_BAND_COLORS[1] },
    { label: '70-84', color: GRADE_BAND_COLORS[2] },
    { label: '85-100', color: GRADE_BAND_COLORS[3] },
]

const gradeChartData = computed(() => {
    if (!gradeRanges.value) return null
    const { range_0_49, range_50_69, range_70_84, range_85_100 } = gradeRanges.value
    return {
        labels: ['0-49', '50-69', '70-84', '85-100'],
        datasets: [{
            label: 'Students',
            data: [range_0_49, range_50_69, range_70_84, range_85_100],
            backgroundColor: GRADE_BAND_COLORS,
            borderRadius: 8,
            borderSkipped: false,
            borderWidth: 0,
        }],
    }
})

// Chart options 
const TOOLTIP_STYLE = {
    backgroundColor: 'rgba(9,9,11,0.92)',
    titleColor: '#fafafa',
    bodyColor: '#a1a1aa',
    borderColor: 'rgba(255,255,255,0.06)',
    borderWidth: 1,
    padding: 10,
    cornerRadius: 8,
}

const barChartOptions = {
    responsive: true,
    datasets: { bar: { barThickness: 48, maxBarThickness: 56 } },
    plugins: {
        legend: { display: false },
        tooltip: TOOLTIP_STYLE,
    },
    scales: {
        x: {
            grid: { display: false },
            border: { display: false },
            ticks: { color: '#71717a', font: { size: 11 } },
        },
        y: {
            beginAtZero: true,
            ticks: { stepSize: 1, color: '#52525b', font: { size: 11 } },
            grid: { color: 'rgba(255,255,255,0.03)', drawBorder: false },
            border: { display: false },
        },
    },
}

const doughnutChartOptions = {
    responsive: true,
    maintainAspectRatio: false, 
    cutout: '75%',             
    plugins: {
        legend: { 
            position: 'right',     
            align: 'center',
            labels: { 
                color: '#71717a',  
                padding: 14,       
                boxWidth: 8,       
                boxHeight: 8,
                borderRadius: 2,   
                font: { size: 11, weight: '500' } 
            } 
        },
        tooltip: TOOLTIP_STYLE,
    },
}

// Helpers 
function calcAttendancePercent(student) {
    if (!student.attendance_count) return '0.0'
    return ((student.present_count / student.attendance_count) * 100).toFixed(1)
}

function isHighRisk(student) {
    const attendancePct = student.attendance_count > 0
        ? (student.present_count / student.attendance_count) * 100
        : 0
    const gradeAvg = student.avg_grade ?? 100
    return attendancePct < 50 || gradeAvg < 35
}

function courseAttendanceColor(pct) {
    const numericPct = Number(pct ?? 0);
    if (numericPct >= 75) return 'bg-foreground'
    if (numericPct >= 50) return 'bg-yellow-500'
    return 'bg-destructive'
}
</script>

<template>
    <div class="p-6 space-y-5">

        <div v-if="dashboardStore.loading" class="flex items-center justify-center h-64">
            <p class="text-muted-foreground text-sm">Loading...</p>
        </div>

        <div v-else-if="dashboardStore.error" class="text-destructive text-sm">
            {{ dashboardStore.error }}
        </div>

        <template v-else>

            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">

                <Card class="hover:shadow-md transition-shadow">
                    <CardHeader class="flex flex-row items-start justify-between space-y-0 pb-2">
                        <div class="w-9 h-9 rounded-xl bg-muted flex items-center justify-center">
                            <Users class="w-4 h-4 text-muted-foreground" />
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-1">
                        <p class="text-3xl font-bold tracking-tight">{{ stats?.total_students ?? 0 }}</p>
                        <p class="text-xs text-muted-foreground">Total Students</p>
                        <RouterLink to="/students"
                            class="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors pt-1">
                            View all
                            <ChevronRight class="w-3 h-3" />
                        </RouterLink>
                    </CardContent>
                </Card>

                <Card class="hover:shadow-md transition-shadow">
                    <CardHeader class="flex flex-row items-start justify-between space-y-0 pb-2">
                        <div class="w-9 h-9 rounded-xl bg-muted flex items-center justify-center">
                            <BookOpen class="w-4 h-4 text-muted-foreground" />
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-1">
                        <p class="text-3xl font-bold tracking-tight">{{ stats?.total_courses ?? 0 }}</p>
                        <p class="text-xs text-muted-foreground">Active Courses</p>
                        <RouterLink to="/courses"
                            class="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors pt-1">
                            View all
                            <ChevronRight class="w-3 h-3" />
                        </RouterLink>
                    </CardContent>
                </Card>

                <Card class="hover:shadow-md transition-shadow">
                    <CardHeader class="flex flex-row items-start justify-between space-y-0 pb-2">
                        <div class="w-9 h-9 rounded-xl bg-muted flex items-center justify-center">
                            <CalendarDays class="w-4 h-4 text-muted-foreground" />
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-1">
                        <p class="text-3xl font-bold tracking-tight">{{ stats?.sessions_this_week ?? 0 }}</p>
                        <p class="text-xs text-muted-foreground">Sessions This Week</p>
                        <RouterLink to="/schedule"
                            class="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors pt-1">
                            Schedule
                            <ChevronRight class="w-3 h-3" />
                        </RouterLink>
                    </CardContent>
                </Card>

                <Card class="hover:shadow-md transition-shadow">
                    <CardHeader class="flex flex-row items-start justify-between space-y-0 pb-2">
                        <div class="w-9 h-9 rounded-xl bg-destructive/10 flex items-center justify-center">
                            <TriangleAlert class="w-4 h-4 text-destructive" />
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-1">
                        <p class="text-3xl font-bold tracking-tight text-destructive">{{ stats?.at_risk_count ?? 0 }}
                        </p>
                        <p class="text-xs text-muted-foreground">At-Risk Students</p>
                        <p class="text-xs text-destructive/70 pt-1">Needs attention</p>
                    </CardContent>
                </Card>

            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

                <Card class="lg:col-span-2">
                    <CardHeader class="flex flex-row items-start justify-between space-y-0 pb-3">
                        <div>
                            <CardTitle class="text-sm font-semibold">Grade Distribution</CardTitle>
                            <CardDescription class="text-xs mt-0.5">Score bands across all students</CardDescription>
                        </div>
                        <div class="flex items-center gap-3 flex-wrap justify-end">
                            <span v-for="band in gradeBandLegend" :key="band.label"
                                class="flex items-center gap-1.5 text-xs text-muted-foreground">
                                <span class="w-2 h-2 rounded-full" :style="{ background: band.color }" />
                                {{ band.label }}
                            </span>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <Bar v-if="gradeChartData" :data="gradeChartData" :options="barChartOptions" class="max-h-52" />
                        <div v-else class="flex items-center justify-center h-52 text-sm text-muted-foreground">
                            No grade data yet.
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader class="pb-3">
                        <CardTitle class="text-sm font-semibold">Assessment Distribution</CardTitle>
                        <CardDescription class="text-xs mt-0.5">Total count by type</CardDescription>
                    </CardHeader>
                    <CardContent class="flex items-center justify-center">
                        <div class="w-full h-44 px-2">
                            <Doughnut v-if="assessmentChartData" :data="assessmentChartData"
                                :options="doughnutChartOptions" />
                            <div v-else class="flex items-center justify-center h-44 text-sm text-muted-foreground">
                                No assessment data yet.
                            </div>
                        </div>
                    </CardContent>
                </Card>

            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

                <Card class="lg:col-span-2">
                    <CardHeader class="flex flex-row items-start justify-between space-y-0 pb-3">
                        <div>
                            <CardTitle class="text-sm font-semibold">At-Risk Students</CardTitle>
                            <CardDescription class="text-xs mt-0.5">Students needing intervention</CardDescription>
                        </div>
                        <RouterLink to="/students"
                            class="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors mt-0.5">
                            View all
                            <ChevronRight class="w-3 h-3" />
                        </RouterLink>
                    </CardHeader>
                    <CardContent class="p-0">
                        <div v-if="!atRiskList.length" class="text-sm text-muted-foreground text-center py-10 px-6">
                            No at-risk students. Keep up the great work!
                        </div>
                        <Table v-else>
                            <TableHeader>
                                <TableRow>
                                    <TableHead class="text-xs uppercase tracking-wider pl-6">Student</TableHead>
                                    <TableHead class="text-xs uppercase tracking-wider">Attendance</TableHead>
                                    <TableHead class="text-xs uppercase tracking-wider">Grade Avg</TableHead>
                                    <TableHead class="text-xs uppercase tracking-wider">Risk</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-for="student in atRiskList" :key="student.first_name + student.last_name"
                                    class="hover:bg-muted/40 transition-colors">
                                    <TableCell class="pl-6">
                                        <div class="flex items-center gap-3">
                                            <div
                                                class="w-8 h-8 rounded-full bg-muted flex items-center justify-center text-xs font-semibold shrink-0">
                                                {{ student.first_name[0] }}{{ student.last_name[0] }}
                                            </div>
                                            <span class="font-medium text-sm">{{ student.first_name }} {{
                                                student.last_name }}</span>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div class="flex items-center gap-2">
                                            <div class="w-20 h-1.5 rounded-full bg-muted overflow-hidden">
                                                <div class="h-full rounded-full transition-all"
                                                    :class="Number(calcAttendancePercent(student)) < 50 ? 'bg-destructive' : 'bg-yellow-500'"
                                                    :style="{ width: calcAttendancePercent(student) + '%' }" />
                                            </div>
                                            <span class="text-xs tabular-nums text-muted-foreground">
                                                {{ calcAttendancePercent(student) }}%
                                            </span>
                                        </div>
                                    </TableCell>
                                    <TableCell class="tabular-nums text-sm font-medium">
                                        {{ student.avg_grade !== null ? Number(student.avg_grade).toFixed(1) : 'N/A' }}
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" :class="isHighRisk(student)
                                            ? 'bg-destructive/10 text-destructive border-destructive/20 text-xs'
                                            : 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20 text-xs'">
                                            {{ isHighRisk(student) ? 'High' : 'Medium' }}
                                        </Badge>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>

                <div class="flex flex-col gap-4">

                    <Card>
                        <CardHeader class="pb-3">
                            <CardTitle class="text-sm font-semibold">Course Breakdown</CardTitle>
                            <CardDescription class="text-xs mt-0.5">Attendance rate per course</CardDescription>
                        </CardHeader>
                        <CardContent class="space-y-3">
                            <div v-if="!courseAttendance.length" class="text-sm text-muted-foreground text-center py-4">
                                No data yet.
                            </div>
                            <div v-for="course in courseAttendance" :key="course.name" class="space-y-1.5">
                                <div class="flex items-center justify-between">
                                    <span class="text-sm font-medium truncate max-w-[130px]">{{ course.name }}</span>
                                    <span class="text-xs tabular-nums text-muted-foreground">
                                        {{ Number(course.attendance_percentage ?? 0).toFixed(0) }}%
                                    </span>
                                </div>
                                <div class="w-full h-1.5 rounded-full bg-muted overflow-hidden">
                                    <div class="h-full rounded-full transition-all duration-500"
                                        :class="courseAttendanceColor(course.attendance_percentage)"
                                        :style="{ width: (course.attendance_percentage ?? 0) + '%' }" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    <Card class="flex-1">
                        <CardHeader class="pb-3">
                            <CardTitle class="text-sm font-semibold">Recent Activity</CardTitle>
                            <CardDescription class="text-xs mt-0.5">Latest changes in your school</CardDescription>
                        </CardHeader>
                        <CardContent class="space-y-3">
                            <div v-if="!dashboardStore.recentActivity?.length"
                                class="text-sm text-muted-foreground text-center py-4">
                                No recent activity.
                            </div>
                            <div v-for="(activity, index) in dashboardStore.recentActivity" :key="index"
                                class="flex items-start gap-3">
                                <div class="w-1.5 h-1.5 rounded-full bg-foreground mt-1.5 shrink-0" />
                                <div>
                                    <p class="text-xs leading-snug">{{ activity.detail }}</p>
                                    <p class="text-xs text-muted-foreground mt-0.5">{{ activity.timestamp }}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                </div>

            </div>

        </template>
    </div>
</template>