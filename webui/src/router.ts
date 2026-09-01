import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/main' },
    { path: '/main', component: () => import('./views/MainView.vue') },
    { path: '/dashboard', component: () => import('./views/DashboardView.vue') },
    { path: '/scan', component: () => import('./views/ScanView.vue') },
    { path: '/crawl', component: () => import('./views/CrawlView.vue') },
    { path: '/organize', component: () => import('./views/OrganizeView.vue') },
    { path: '/tools', component: () => import('./views/ToolsView.vue') },
    { path: '/settings', component: () => import('./views/SettingsView.vue') },
  ],
})