<script setup>
import { Button } from '@/components/ui/button'
import {
	BookOpen,
	Calendar,
	ClipboardCheck,
	FileChartColumnIncreasing,
	GraduationCap,
	Home,
	LogOut,
	PanelLeft,
	Scroll,
	Users
} from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { toast } from 'vue-sonner'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const collapsed = ref(false)

function handleLogout() {
	auth.logout()
	toast.success('Logged out successfully.')
	router.push('/login')
}

// Map human-readable headers to current matching router string rules
const currentHeaderTitle = computed(() => {
	const path = route.path
	if (path.startsWith('/students')) return 'Student Management'
	if (path.startsWith('/courses')) return 'Courses & Offerings'
	if (path.startsWith('/schedule')) return 'Class Schedule Matrix'
	if (path.startsWith('/attendance')) return 'Attendance Matrix Tracking'
	if (path.startsWith('/grades')) return 'Gradebook Analysis'
	if (path.startsWith('/reports')) return 'Reports Engine'
	if (path.startsWith('/audit')) return 'Security Audit Log'
	return 'Dashboard Overview'
})

const navItems = [
	{ name: 'Dashboard', path: '/dashboard', icon: Home },
	{ name: 'Students', path: '/students', icon: Users },
	{ name: 'Courses', path: '/courses', icon: BookOpen },
	{ name: 'Schedule', path: '/schedule', icon: Calendar },
	{ name: 'Attendance', path: '/attendance', icon: ClipboardCheck },
	{ name: 'Grades', path: '/grades', icon: GraduationCap },
	{ name: 'Reports', path: '/reports', icon: FileChartColumnIncreasing },
	{ name: 'Audit Log', path: '/audit', icon: Scroll },
]
</script>

<template>
	<div class="min-h-screen flex overflow-hidden w-full bg-neutral-50 text-neutral-900">

		<!-- Mobile overlay -->
		<div v-if="!collapsed" @click="collapsed = true" class="fixed inset-0 bg-black/50 z-40 md:hidden"></div>

		<!-- Sidebar -->
		<aside :class="collapsed ? 'w-16' : 'w-64'"
			class="bg-neutral-900 text-neutral-100 flex flex-col transition-all duration-300 overflow-hidden min-h-screen fixed left-0 top-0 bottom-0 z-50">

			<!-- Logo Panel -->
			<div class="h-16 flex items-center border-b border-neutral-700 px-4 shrink-0"
				:class="collapsed ? 'justify-center' : 'justify-between'">
				<span v-if="!collapsed" class="font-bold text-lg tracking-tight text-white">Skool</span>
				<button @click="collapsed = !collapsed"
					class="text-neutral-400 hover:text-white p-1.5 rounded hover:bg-neutral-800 transition-colors">
					<PanelLeft class="w-5 h-5" />
				</button>
			</div>

			<!-- Navigation System Area -->
			<nav class="flex-1 p-2 flex flex-col gap-1 overflow-y-auto">
				<RouterLink v-for="item in navItems" :key="item.path" :to="item.path" v-slot="{ isActive }">
					<div :class="[
						collapsed ? 'justify-center' : '',
						isActive ? 'bg-neutral-800 text-white font-medium shadow-2xs' : 'text-neutral-400 hover:bg-neutral-800/60 hover:text-neutral-200'
					]" class="flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-all duration-150 cursor-pointer">
						<component :is="item.icon" class="w-4 h-4 shrink-0" />
						<span v-if="!collapsed" class="truncate">{{ item.name }}</span>
					</div>
				</RouterLink>
			</nav>

			<!-- User Profile & Action Footer Panel -->
			<div class="p-2 border-t border-neutral-700 flex flex-col gap-2 shrink-0 bg-neutral-950/40">
				<div v-if="!collapsed" class="px-3 py-1.5 text-sm">
					<div class="font-medium text-neutral-200 truncate">{{ auth.teacher?.username || 'Teacher Account' }}
					</div>
					<div class="text-xs text-neutral-500 truncate mt-0.5">{{ auth.teacher?.school_name }}</div>
				</div>
				<Button variant="secondary" :class="collapsed ? 'justify-center px-0' : ''"
					class="w-full cursor-pointer h-9 text-xs" @click="handleLogout">
					<span v-if="!collapsed">Logout Session</span>
					<LogOut v-else class="w-4 h-4" />
				</Button>
			</div>

		</aside>

		<!-- Main Workspace Area Wrapper -->
		<div :class="collapsed ? 'pl-16' : 'pl-64'" class="flex-1 flex flex-col min-w-0 transition-all duration-300">

			<!-- Dynamic View Header Component -->
			<header class="h-16 bg-white border-b border-neutral-200 flex items-center px-6 shrink-0 shadow-xs">
				<h1 class="font-semibold text-base text-neutral-800 tracking-tight">
					{{ currentHeaderTitle }}
				</h1>
			</header>

			<!-- Core Active Router Layout Body -->
			<main class="flex-1 p-6 overflow-y-auto">
				<div class="max-w-7xl mx-auto w-full animate-in fade-in-50 duration-200">
					<RouterView />
				</div>
			</main>
		</div>

	</div>
</template>