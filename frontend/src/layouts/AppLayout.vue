<script setup>
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import { Home, PanelLeft, LogOut } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const collapsed = ref(false)

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen flex overflow-hidden">

    <!-- Mobile overlay -->
    <div v-if="!collapsed" @click="collapsed = true" class="fixed inset-0 bg-black/50 z-40 md:hidden"></div>

    <!-- Sidebar -->
    <aside
      :class="collapsed ? 'w-16' : 'w-64'"
      class="bg-neutral-900 text-neutral-100 flex flex-col transition-all duration-300 overflow-hidden min-h-screen fixed z-50">

      <!-- Logo -->
      <div class="h-16 flex items-center border-b border-neutral-700 px-4"
        :class="collapsed ? 'justify-center' : 'justify-between'">
        <span v-if="!collapsed" class="font-bold text-lg">Chalkboard</span>
        <button @click="collapsed = !collapsed" class="text-neutral-400 hover:text-white p-1 rounded hover:bg-neutral-800">
          <PanelLeft class="w-5 h-5" />
        </button>
      </div>

      <!-- Nav -->
      <nav class="flex-1 p-2 flex flex-col gap-1">
        <a href="/dashboard"
          :class="collapsed ? 'justify-center' : ''"
          class="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-neutral-800 transition-colors">
          <Home class="w-4 h-4 shrink-0" />
          <span v-if="!collapsed">Dashboard</span>
        </a>
      </nav>

      <!-- Footer -->
      <div class="p-2 border-t border-neutral-700 flex flex-col gap-2">
        <div v-if="!collapsed" class="px-3 py-2 text-sm text-neutral-400">
          {{ auth.teacher?.username }}
          <div class="text-xs text-neutral-500">{{ auth.teacher?.school_name }}</div>
        </div>
        <Button variant="secondary"
          :class="collapsed ? 'justify-center px-0' : ''"
          class="w-full cursor-pointer"
          @click="handleLogout">
          <span v-if="!collapsed">Logout</span>
          <LogOut v-else class="w-4 h-4" />
        </Button>
      </div>

    </aside>

    <!-- Main area -->
    <div :class="collapsed ? 'ml-16' : 'ml-64'" class="flex-1 flex flex-col min-w-0 transition-all duration-300">
      <header class="h-16 bg-white border-b flex items-center px-6">
        <span class="font-medium text-sm text-neutral-600">Dashboard</span>
      </header>
      <main class="flex-1 p-6 bg-gray-50">
        <RouterView />
      </main>
    </div>

  </div>
</template>