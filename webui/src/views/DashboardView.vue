<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="12">
        <el-card>
          <template #header>服务状态</template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="服务">{{ health?.service ?? '—' }}</el-descriptions-item>
            <el-descriptions-item label="版本">{{ health?.version ?? '—' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>最新任务</template>
          <el-table :data="tasks.slice(0, 8)" size="small">
            <el-table-column prop="title" label="任务" />
            <el-table-column prop="status" label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="taskStatusType(row.status)" size="small">{{ taskStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="progress" label="进度" width="120">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" :status="row.status === 'failed' ? 'exception' : undefined" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, taskStatusText, taskStatusType } from '../api'

const health = ref<any>(null)
const tasks = ref<any[]>([])

onMounted(async () => {
  const r = await api.health()
  health.value = r.data
  tasks.value = await api.tasks()
})
</script>