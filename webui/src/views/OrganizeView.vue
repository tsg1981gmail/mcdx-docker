<template>
  <div>
    <el-card style="margin-bottom:16px">
      <template #header>整理（硬链接 / 复制）</template>
      <el-form label-width="120px" style="max-width:720px">
        <el-form-item label="源目录">
          <el-input v-model="source" placeholder="/media/movies" />
        </el-form-item>
        <el-form-item label="目标库目录">
          <el-input v-model="library" placeholder="/media/library" />
          <div class="hint">目标与源应在同一文件系统才能用硬链接；跨盘自动回退复制。建议源挂载只读。</div>
        </el-form-item>
        <el-form-item label="链接方式">
          <el-radio-group v-model="mode">
            <el-radio value="hardlink">硬链接（同盘，省空间）</el-radio>
            <el-radio value="copy">复制（跨盘）</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="并发数">
          <el-input-number v-model="concurrency" :min="1" :max="8" />
        </el-form-item>
        <el-form-item label="下载海报">
          <el-switch v-model="downloadPoster" />
        </el-form-item>
        <el-form-item>
          <el-button :loading="previewing" @click="preview">预览（检查数量/同盘）</el-button>
          <el-button type="primary" :loading="starting" :disabled="!previewItem.count" @click="start">开始整理</el-button>
        </el-form-item>
      </el-form>
      <el-alert v-if="previewItem.count !== undefined" type="info" :closable="false"
        :title="`共 ${previewItem.count} 个视频；${previewItem.same_filesystem ? '✅ 同文件系统，硬链接可用' : '⚠️ 跨文件系统，将用复制'}`" />
    </el-card>

    <el-card>
      <template #header>历史整理任务</template>
      <el-table :data="tasks" size="small">
        <el-table-column prop="title" label="任务" width="160" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="taskStatusType(row.status)" size="small">{{ taskStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="200">
          <template #default="{ row }"><el-progress :percentage="row.progress" /></template>
        </el-table-column>
        <el-table-column prop="detail" label="详情" min-width="160" />
        <el-table-column label="结果" min-width="220">
          <template #default="{ row }">
            <span v-if="row.result" style="font-size:12px">
              链接 {{ row.result.linked }} · 复制 {{ row.result.copied }} · 跳过 {{ row.result.skipped }} · 失败 {{ row.result.failed }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="130">
          <template #default="{ row }">
            <el-button v-if="row.status === 'running'" size="small" type="danger" @click="cancel(row.id)">取消</el-button>
            <el-button size="small" @click="remove(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, taskStatusText, taskStatusType } from '../api'

const source = ref('/media')
const library = ref('/media/library')
const mode = ref('hardlink')
const concurrency = ref(4)
const downloadPoster = ref(true)
const previewing = ref(false)
const starting = ref(false)
const previewItem = ref<any>({})
const tasks = ref<any[]>([])

async function refresh() { tasks.value = await api.tasks() }
async function preview() {
  previewing.value = true
  try {
    previewItem.value = await api.organizePreview(source.value, library.value)
  } finally {
    previewing.value = false
  }
}
async function start() {
  starting.value = true
  try {
    const r = await api.organizeStart({
      source: source.value, library: library.value, mode: mode.value,
      concurrency: concurrency.value, download_poster: downloadPoster.value,
    })
    if (!r.ok) alert(r.error || '启动失败')
    await refresh()
  } finally {
    starting.value = false
  }
}
function cancel(id: string) { api.cancelTask(id).then(refresh) }
function remove(id: string) { api.removeTask(id).then(refresh) }

onMounted(() => { refresh(); setInterval(refresh, 3000) })
</script>

<style scoped>
.hint { font-size: 12px; color: #888; margin-top: 4px; }
</style>