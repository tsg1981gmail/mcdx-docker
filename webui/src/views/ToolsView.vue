<template>
  <div>
    <el-card>
      <template #header>工具（迁移自 mdcx/tools，无头运行）</template>
      <el-table :data="tools" size="small">
        <el-table-column prop="name" label="工具" width="200" />
        <el-table-column prop="desc" label="说明" min-width="260" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.ready ? 'success' : 'info'" size="small">{{ row.ready ? '可用' : '接入中' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button v-if="row.action" size="small" :loading="row.busy" @click="run(row)">{{ row.action }}</el-button>
            <span v-else style="font-size:12px;color:#999">后续版本</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { http } from '../api'

const tools = ref<any[]>([
  { name: 'Gfriends 同步', key: 'sync_gfriends', desc: '拉取演员头像库 Gfriends 仓库更新（需配置本地路径）', ready: true, action: '同步', busy: false },
  { name: '演员库工具', key: 'actor_db', desc: '演员库合并/TMDB 翻译/男优剔除/校验（xlsx）', ready: false, action: '', busy: false },
  { name: '字幕检查', key: 'subtitle', desc: '为无字幕影片从字幕目录复制/重命名', ready: false, action: '', busy: false },
  { name: '缺失检查', key: 'missing', desc: '扫描本地库对比网络番号输出缺失列表', ready: false, action: '', busy: false },
  { name: 'Emby 演员管理', key: 'emby_actor', desc: 'Emby/Jellyfin 演员信息与头像补全', ready: false, action: '', busy: false },
  { name: 'Wiki 演员刮削', key: 'wiki', desc: 'Wikidata+wiki 演员信息批量刮削', ready: false, action: '', busy: false },
])

async function run(row: any) {
  if (row.key !== 'sync_gfriends') return
  row.busy = true
  try {
    const r = await http.post('/tools/sync-gfriends', { path: '/data/userdata/gfriends' })
    alert(r.data?.ok ? r.data.message : r.data?.error || '失败')
  } finally {
    row.busy = false
  }
}
</script>