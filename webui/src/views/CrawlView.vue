<template>
  <div>
    <el-card style="margin-bottom:16px">
      <template #header>批量刮削</template>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <el-input v-model="path" placeholder="/media/movies（递归扫描目录下的视频）" style="width:360px" />
        <el-button :loading="previewing" @click="preview">预览</el-button>
        <el-button type="primary" :loading="starting" :disabled="!previewItem.count" @click="start">开始刮削</el-button>
        <el-tag v-if="previewItem.count" type="info">{{ previewItem.count }} 个视频</el-tag>
      </div>
    </el-card>

    <el-card>
      <template #header>任务</template>
      <el-table :data="tasks" size="small">
        <el-table-column prop="title" label="任务" width="160" />
        <el-table-column prop="id" label="ID" width="150" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="taskStatusType(row.status)" size="small">{{ taskStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="220">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :status="row.status === 'failed' ? 'exception' : undefined" />
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="详情" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="130">
          <template #default="{ row }">
            <el-button v-if="row.status === 'running'" size="small" type="danger" @click="cancel(row.id)">取消</el-button>
            <el-button size="small" @click="remove(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card v-if="previewItem.sample?.length" style="margin-top:16px">
      <template #header>预览（前 50 个）</template>
      <el-table :data="previewItem.sample.map((p: string) => ({ p }))" size="small">
        <el-table-column prop="p" label="文件" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, taskStatusText, taskStatusType } from '../api'

const path = ref('/media')
const previewing = ref(false)
const starting = ref(false)
const previewItem = ref<any>({})
const tasks = ref<any[]>([])

async function refresh() {
  tasks.value = await api.tasks()
}
async function preview() {
  previewing.value = true
  try {
    previewItem.value = await api.crawlerPreview(path.value)
  } finally {
    previewing.value = false
  }
}
async function start() {
  starting.value = true
  try {
    const r = await api.crawlerStart(path.value)
    if (!r.ok) alert(r.error || '启动失败')
    else previewItem.value = {}
    await refresh()
  } finally {
    starting.value = false
  }
}
function cancel(id: string) { api.cancelTask(id).then(refresh) }
function remove(id: string) { api.removeTask(id).then(refresh) }

onMounted(() => { refresh(); setInterval(refresh, 3000) })
</script>