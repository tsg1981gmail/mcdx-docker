<template>
  <div>
    <el-card style="margin-bottom:16px">
      <template #header>目录浏览（/media 挂载区 + /data）</template>
      <div style="display:flex;gap:8px">
        <el-input v-model="path" style="width:400px" />
        <el-button @click="load">打开</el-button>
        <el-button type="primary" :loading="scanning" @click="scan">扫描影片</el-button>
      </div>
      <el-table :data="items" size="small" @row-dblclick="open" style="margin-top:12px">
        <el-table-column label="名称">
          <template #default="{ row }">
            <el-icon v-if="row.is_dir"><Folder /></el-icon>
            <el-icon v-else><Document /></el-icon>
            <span style="margin-left:6px">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="is_dir" label="类型" width="80">
          <template #default="{ row }">{{ row.is_dir ? '目录' : row.is_link ? '链接' : '文件' }}</template>
        </el-table-column>
        <el-table-column label="大小" width="110">
          <template #default="{ row }">{{ row.is_dir ? '—' : fmtSize(row.size) }}</template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card v-if="scanResult.items?.length">
      <template #header>扫描结果：{{ scanResult.listed }} / {{ scanResult.found }} 个视频</template>
      <el-table :data="scanResult.items" size="small" max-height="420">
        <el-table-column prop="name" label="文件" width="260" show-overflow-tooltip />
        <el-table-column prop="dir" label="目录" min-width="260" show-overflow-tooltip />
        <el-table-column prop="size_h" label="大小" width="100" />
        <el-table-column prop="mtime" label="修改时间" width="150" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api'

const path = ref('/media')
const items = ref<any[]>([])
const scanning = ref(false)
const scanResult = ref<any>({})

function fmtSize(n: number) {
  if (n < 1024) return n + ' B'
  if (n < 1024 ** 2) return (n / 1024).toFixed(1) + ' KB'
  if (n < 1024 ** 3) return (n / 1024 ** 2).toFixed(1) + ' MB'
  return (n / 1024 ** 3).toFixed(2) + ' GB'
}
async function load() {
  const d = await api.listDir(path.value)
  if (d.ok) items.value = d.items
}
async function scan() {
  scanning.value = true
  try {
    const r = await api.scan(path.value)
    if (r.ok) scanResult.value = r
    else alert(r.error || '扫描失败')
  } finally {
    scanning.value = false
  }
}
function open(row: any) {
  if (!row.is_dir) return
  path.value = path.value.replace(/\/+$/, '') + '/' + row.name
  load()
}
onMounted(load)
</script>