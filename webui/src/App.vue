<template>
  <el-container class="app-root">
    <el-aside width="210px" class="sidebar">
      <div class="brand">
        <span class="brand-title">mdcx-web</span>
        <span class="brand-sub">刮削 · 整理 · 硬链接</span>
      </div>
      <el-menu :default-active="route.path" router class="menu">
        <el-menu-item index="/dashboard"><el-icon><Odometer /></el-icon>任务总览</el-menu-item>
        <el-menu-item index="/scan"><el-icon><FolderOpened /></el-icon>目录扫描</el-menu-item>
        <el-menu-item index="/crawl"><el-icon><Search /></el-icon>批量刮削</el-menu-item>
        <el-menu-item index="/organize"><el-icon><Link /></el-icon>整理 / 硬链接</el-menu-item>
        <el-menu-item index="/tools"><el-icon><Tools /></el-icon>工具</el-menu-item>
        <el-menu-item index="/settings"><el-icon><Setting /></el-icon>设置</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>mdcx-web 控制台</span>
        <span class="header-right">服务：本地</span>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style>
html, body, #app { height: 100%; margin: 0; }
.app-root { height: 100%; }
.sidebar { background: #1d2b3a; }
.brand { padding: 20px 16px 14px; color: #fff; }
.brand-title { font-size: 18px; font-weight: 700; display: block; }
.brand-sub { font-size: 12px; opacity: .7; }
.menu { border-right: none; background: transparent; --el-menu-bg-color: transparent; --el-menu-text-color: #c3ccd6; --el-menu-active-color: #409eff; }
.header { background: #fff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; }
.header-right { font-size: 13px; color: #888; }
</style>