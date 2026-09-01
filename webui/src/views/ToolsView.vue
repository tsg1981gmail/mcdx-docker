<template>
  <div>
    <el-row :gutter="14">
      <el-col :span="12" v-for="card in cards" :key="card.key" style="margin-bottom:14px">
        <el-card>
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span>{{ card.title }}</span>
              <el-tag :type="card.ready ? 'success' : 'info'" size="small">{{ card.ready ? '可用' : '接入中' }}</el-tag>
            </div>
          </template>

          <!-- 单文件刮削（指定番号网址） -->
          <template v-if="card.key === 'single_scrape'">
            <el-input v-model="ss.file" placeholder="文件路径 /media/xxx.mp4" size="small" style="margin-bottom:6px" />
            <el-input v-model="ss.url" placeholder="番号网址（如 javbus/javdb 详情页 URL）" size="small" style="margin-bottom:6px" />
            <el-button size="small" type="primary" @click="doAppoint">刮削</el-button>
          </template>

          <!-- 检查演员缺失番号 -->
          <template v-if="card.key === 'missing'">
            <el-input v-model="ms.actors_name" placeholder="演员名（逗号分隔）" size="small" style="margin-bottom:6px" />
            <el-input v-model="ms.library" placeholder="本地资源库目录 /media/lib" size="small" style="margin-bottom:6px" />
            <el-checkbox v-model="ms.deep">深查（含 nfo 演员集合）</el-checkbox>
            <div style="margin-top:6px"><el-button size="small" type="primary" @click="doMissing">检查缺失番号</el-button></div>
          </template>

          <!-- 裁剪图片 -->
          <template v-if="card.key === 'poster_cut'">
            <el-input v-model="cut.image" placeholder="原图路径 /media/xxx.jpg" size="small" style="margin-bottom:6px" />
            <el-input v-model="cut.out" placeholder="输出路径 /media/xxx-poster.jpg" size="small" style="margin-bottom:6px" />
            <el-button size="small" type="primary" :loading="cutBusy" @click="doCut">裁剪为 2:3 封面</el-button>
          </template>

          <!-- 移动视频字幕 -->
          <template v-if="card.key === 'move_videos'">
            <el-input v-model="mv.path" placeholder="待刮削目录 /media/xxx" size="small" style="margin-bottom:6px" />
            <el-input v-model="mv.target" placeholder="目标子目录名（默认 Movie_moved）" size="small" style="margin-bottom:6px" />
            <el-button size="small" type="primary" @click="run('move-videos', mv)">开始移动</el-button>
          </template>

          <!-- 软链接助手 -->
          <template v-if="card.key === 'symlink_helper'">
            <el-input v-model="sl.netdisk_path" placeholder="网盘目录 /media/net" size="small" style="margin-bottom:6px" />
            <el-input v-model="sl.local_path" placeholder="本地目标目录 /media/local" size="small" style="margin-bottom:6px" />
            <el-checkbox v-model="sl.copy_files" size="small">同时复制 nfo/图片/字幕</el-checkbox>
            <div style="margin-top:6px"><el-button size="small" type="primary" @click="run('symlink-helper', sl)">一键创建软链接</el-button></div>
          </template>

          <!-- 演员库维护 -->
          <template v-if="card.key === 'actor_db'">
            <el-select v-model="adb.action" size="small" style="width:100%;margin-bottom:6px">
              <el-option label="剔除男优（clean_male）" value="clean_male" />
              <el-option label="校验 TMDB ID（verify_tmdb_ids）" value="verify_tmdb_ids" />
              <el-option label="从 AVdb 同步（sync_from_avdb）" value="sync_from_avdb" />
              <el-option label="更新 NFO 的 TMDB ID（需 nfo 目录）" value="update_nfo_tmdb_ids" />
            </el-select>
            <el-input v-if="adb.action === 'update_nfo_tmdb_ids'" v-model="adb.nfo_dir" placeholder="NFO 目录 /media/lib" size="small" style="margin-bottom:6px" />
            <el-button size="small" type="primary" @click="run('actor-db', adb)">开始维护</el-button>
          </template>

          <!-- 刮削缓存管理 -->
          <template v-if="card.key === 'scrape_cache'">
            <el-descriptions :column="2" size="small" border>
              <el-descriptions-item label="断点DB">{{ cache.db_exists ? '存在' : '无' }}</el-descriptions-item>
              <el-descriptions-item label="成功列表">{{ cache.success_count }}</el-descriptions-item>
              <el-descriptions-item label="剩余列表">{{ cache.remain_count }}</el-descriptions-item>
            </el-descriptions>
            <div style="margin-top:8px">
              <el-button size="small" @click="cacheAct('list')">刷新统计</el-button>
              <el-button size="small" type="danger" @click="cacheAct('clear')">清空断点缓存</el-button>
            </div>
          </template>

          <!-- Gfriends -->
          <template v-if="card.key === 'sync_gfriends'">
            <el-input v-model="gf.path" size="small" placeholder="Gfriends 仓库本地路径 /data/userdata/gfriends" style="margin-bottom:6px" />
            <el-button size="small" type="primary" @click="run('sync-gfriends', gf)">同步</el-button>
          </template>

          <!-- 接入中 -->
          <template v-if="!card.ready">
            <div style="font-size:12px;color:#999">{{ card.note || '该面板在后续版本接入' }}</div>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <template #header>工具任务</template>
      <el-table :data="toolTasks" size="small">
        <el-table-column prop="title" label="任务" width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="taskStatusType(row.status)" size="small">{{ taskStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="180">
          <template #default="{ row }"><el-progress :percentage="row.progress" /></template>
        </el-table-column>
        <el-table-column prop="detail" label="详情" min-width="200" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { api, http, taskStatusText, taskStatusType } from '../api'

const cut = reactive({ image: '', out: '' })
const mv = reactive({ path: '', target: 'Movie_moved' })
const sl = reactive({ netdisk_path: '', local_path: '', copy_files: false })
const adb = reactive({ action: 'clean_male', nfo_dir: '' })
const gf = reactive({ path: '/data/userdata/gfriends' })
const ss = reactive({ file: '', url: '' })
const ms = reactive({ actors_name: '', library: '', deep: true })
const cutBusy = ref(false)
const cache = reactive({ db_exists: false, success_count: 0, remain_count: 0 })
const toolTasks = ref<any[]>([])

const cards = [
  { key: 'single_scrape', title: '单文件刮削（指定番号网址）', ready: true },
  { key: 'poster_cut', title: '裁剪图片（封面图比例）', ready: true },
  { key: 'missing', title: '检查演员缺失番号', ready: true },
  { key: 'move_videos', title: '移动视频、字幕', ready: true },
  { key: 'symlink_helper', title: '软链接助手（网盘→本地）', ready: true },
  { key: 'actor_db', title: '演员库维护（actor_database.xlsx）', ready: true },
  { key: 'cover_backfill', title: '封面补图', ready: false, note: '依赖图片补全策略配置，后续版本接入' },
  { key: 'scrape_cache', title: '刮削缓存管理', ready: true },
  { key: 'sync_gfriends', title: 'Gfriends 同步', ready: true },
]

async function run(ep: string, body: any) {
  const r = await http.post(`/tools/${ep}`, body)
  if (!r.data.ok) alert(r.data.error || '启动失败')
  refresh()
}
async function doCut() {
  cutBusy.value = true
  try {
    const r = await http.post('/tools/poster-cut', cut)
    alert(r.data.ok ? `已生成 ${r.data.out}` : r.data.error)
  } finally {
    cutBusy.value = false
  }
}
async function doAppoint() {
  const r = await api.crawlerAppoint(ss.file, ss.url)
  if (!r.data.ok) alert(r.data.error || '启动失败')
  refresh()
}
async function doMissing() {
  const r = await http.post('/tools/missing', { actors_name: ms.actors_name, local_library: ms.library ? [ms.library] : [], deep: ms.deep })
  if (!r.data.ok) alert(r.data.error || '启动失败')
  refresh()
}
async function cacheAct(action: string) {
  const r = await http.post('/tools/cache', { action })
  if (r.data.ok) Object.assign(cache, r.data)
  else alert(r.data.error || '操作失败')
}
async function refresh() {
  toolTasks.value = (await api.tasks()).filter(t => t.kind === 'tools')
}
let timer: number | undefined
onMounted(() => { refresh(); cacheAct('list'); timer = window.setInterval(refresh, 3000) })
onUnmounted(() => window.clearInterval(timer))
</script>