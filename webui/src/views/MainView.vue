<template>
  <el-tabs v-model="tab" type="border-card">
    <!-- ============ 影片刮削（原版主打页）============ -->
    <el-tab-pane label="影片刮削" name="scrape">
      <!-- 刮削目录 + 模式 + 操作 -->
      <div class="action-bar">
        <el-input v-model="path" placeholder="刮削目录（容器内 /media 下路径）" style="width:340px" @keyup.enter="loadFiles" />
        <el-button @click="loadFiles">浏览</el-button>
        <el-radio-group v-model="mode" style="margin-left:12px">
          <el-radio-button value="common">正常模式</el-radio-button>
          <el-radio-button value="sort">整理模式</el-radio-button>
          <el-radio-button value="update">更新模式</el-radio-button>
          <el-radio-button value="read">读取模式</el-radio-button>
        </el-radio-group>
        <el-button type="primary" :loading="starting" :disabled="busy" style="margin-left:12px" @click="startCrawl">开始刮削</el-button>
        <el-button type="danger" :disabled="!busy" @click="cancel">停止</el-button>
        <el-tag v-if="busy" type="warning" style="margin-left:8px">{{ task?.detail }}</el-tag>
      </div>

      <!-- 文件表格（右键菜单） -->
      <div class="table-wrap" @contextmenu.prevent="closeMenu">
        <el-collapse style="margin-bottom:10px">
        <el-collapse-item title="站点优先级（逐字段，对应原版「字段刮削网站」）">
          <el-table :data="fcRows" size="small" max-height="260">
            <el-table-column prop="field" label="字段" width="110" />
            <el-table-column label="来源网站优先级（逗号分隔，越前越优先）" min-width="280">
              <template #default="{ row }">
                <el-input v-model="row.site_prority_text" size="small" placeholder="javbus,javdb,missav..." @change="fcDirty = true" />
              </template>
            </el-table-column>
            <el-table-column label="语言" width="120">
              <template #default="{ row }">
                <el-select v-model="row.language" size="small">
                  <el-option label="未指定" value="undefined" />
                  <el-option label="中文简体" value="zh_cn" />
                  <el-option label="中文繁体" value="zh_tw" />
                  <el-option label="日文" value="jp" />
                  <el-option label="英文" value="en" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="翻译" width="70">
              <template #default="{ row }"><el-switch v-model="row.translate" size="small" @change="fcDirty = true" /></template>
            </el-table-column>
            <el-table-column label="跳过" width="70">
              <template #default="{ row }"><el-switch v-model="row.skip" size="small" @change="fcDirty = true" /></template>
            </el-table-column>
          </el-table>
          <el-button size="small" type="primary" style="margin-top:8px" :disabled="!fcDirty" @click="saveFieldConfig">保存字段站点优先级</el-button>
        </el-collapse-item>
      </el-collapse>
        <el-table :data="files" size="small" height="320" @row-contextmenu="onContext" :row-class-name="rowClass">
          <el-table-column prop="name" label="文件名称" min-width="220" show-overflow-tooltip />
          <el-table-column prop="dir" label="目录" min-width="220" show-overflow-tooltip />
          <el-table-column prop="size_h" label="大小" width="100" />
          <el-table-column prop="mtime" label="修改时间" width="150" />
        </el-table>
        <div v-if="menu.show" class="ctx-menu" :style="{ left: menu.x + 'px', top: menu.y + 'px' }">
          <div class="ctx-item" @click="ctxForceScrape">强制重新刮削（选中文件）</div>
          <div class="ctx-item" @click="ctxOpenDir">加入刮削列表（整目录）</div>
          <div class="ctx-item" @click="menu.show = false">取消</div>
        </div>
      </div>

      <!-- 结果三列表 + 日志 -->
      <el-tabs v-model="resultTab" class="result-tabs">
        <el-tab-pane label="成功" name="succ">
          <el-table :data="succItems" size="mini" height="180">
            <el-table-column prop="number" label="番号" width="140" />
            <el-table-column prop="show_name" label="名称" min-width="260" show-overflow-tooltip />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="失败" name="fail">
          <el-table :data="failItems" size="mini" height="180">
            <el-table-column prop="number" label="番号" width="140" />
            <el-table-column prop="show_name" label="名称" min-width="260" show-overflow-tooltip />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="剩余" name="remain">
          <el-table :data="remainItems" size="mini" height="180">
            <el-table-column prop="path" label="文件" min-width="380" show-overflow-tooltip />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="日志" name="log">
          <div class="log-console">
            <div v-for="(line, i) in logLines" :key="i" class="log-line">{{ line }}</div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>

    <!-- ============ 工具 ============ -->
    <el-tab-pane label="工具" name="tools">
      <ToolsView />
    </el-tab-pane>

    <!-- ============ 设置 ============ -->
    <el-tab-pane label="设置" name="settings">
      <SettingsView />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { api, TaskSnapshot } from '../api'
import ToolsView from './ToolsView.vue'
import SettingsView from './SettingsView.vue'

const tab = ref('scrape')
const resultTab = ref('succ')
const path = ref('/media')
const mode = ref('common')
const starting = ref(false)
const busy = ref(false)
const task = ref<TaskSnapshot | null>(null)
const files = ref<any[]>([])
const succItems = ref<any[]>([])
const failItems = ref<any[]>([])
const remainItems = ref<any[]>([])
const logLines = ref<string[]>([])
const menu = reactive({ show: false, x: 0, y: 0, file: null as any })
const fcRows = ref<any[]>([])
const fcDirty = ref(false)

let timer: number | undefined

function rowClass({ row }: any) { return rowsSelected.value.includes(row.name) ? 'row-sel' : '' }
const rowsSelected = ref<string[]>([])

async function loadFiles() {
  const r = await api.scan(path.value)
  if (r.ok) files.value = r.items
  else alert(r.error || '读取失败')
  loadFieldConfig()
}
async function loadFieldConfig() {
  const d = await api.configGet()
  const fc = d.data?.config?.field_configs || {}
  fcRows.value = Object.entries(fc).map(([field, v]: any) => ({
    field,
    site_prority_text: (v.site_prority || []).join(','),
    language: v.language || 'undefined',
    translate: !!v.translate,
    skip: !!v.skip,
  }))
  fcDirty.value = false
}
async function saveFieldConfig() {
  const field_configs: any = {}
  for (const row of fcRows.value) {
    field_configs[row.field] = {
      site_prority: row.site_prority_text.split(/[,，\s]+/).filter(Boolean),
      language: row.language,
      translate: row.translate,
      skip: row.skip,
    }
  }
  const r = await api.configPut({ field_configs })
  if (!r.ok) alert(r.error || '保存失败')
  fcDirty.value = false
}
async function refresh() {
  const tasks = await api.tasks()
  const t = tasks.find(x => x.kind === 'crawl')
  if (!t) {
    busy.value = false
    return
  }
  task.value = t
  busy.value = ['running', 'pending'].includes(t.status)
  if (t.result) {
    const r = t.result as any
    succItems.value = (r.records || []).filter((x: any) => x.status === 'succ')
    failItems.value = (r.records || []).filter((x: any) => x.status === 'fail')
    remainItems.value = (r.remain_list || []).map((p: string) => ({ path: p }))
  }
  if (t.status === 'running' || t.status === 'pending') {
    if (t.detail) logLines.value.push(`[${new Date(t.updated * 1000).toLocaleTimeString()}] ${t.detail}`)
  }
  if (t.status === 'success') {
    logLines.value.push(`[${new Date().toLocaleTimeString()}] ✅ 刮削完成：${JSON.stringify(t.result || {})}`)
    starting.value = false
  }
  if (t.status === 'failed' || t.status === 'cancelled') {
    logLines.value.push(`[${new Date().toLocaleTimeString()}] ⏹ ${t.status}: ${t.error || ''}`)
    starting.value = false
  }
}
async function startCrawl() {
  starting.value = true
  const r = await api.crawlerStart(path.value, mode.value)
  if (!r.ok) { alert(r.error || '启动失败'); starting.value = false }
  logLines.value.push(`[${new Date().toLocaleTimeString()}] ▶ 开始 ${modeName(mode.value)}：${r.ok ? r.task_id : ''}`)
  setTimeout(refresh, 1000)
}
function modeName(m: string) {
  return { common: '正常模式', sort: '整理模式', update: '更新模式', read: '读取模式' }[m as any] || m
}
function cancel() { api.cancelTask(task.value!.id).then(() => logLines.value.push('⏹ 已请求停止')) }

function onContext(row: any, _col: any, e: MouseEvent) {
  menu.file = row
  menu.show = true
  menu.x = e.clientX
  menu.y = e.clientY
}
function closeMenu() { menu.show = false }
async function ctxForceScrape() {
  menu.show = false
  if (!menu.file) return
  const r = await api.crawlerStartFiles([`${menu.file.dir}/${menu.file.name}`], 'common', true)
  if (!r.ok) alert(r.error || '启动失败')
}
async function ctxOpenDir() {
  menu.show = false
  const dir = menu.file?.dir || path.value
  const r = await api.crawlerStart(dir, mode.value)
  if (!r.ok) alert(r.error || '启动失败')
}

onMounted(() => { loadFiles(); refresh(); timer = window.setInterval(refresh, 2500) })
onUnmounted(() => window.clearInterval(timer))
</script>

<style scoped>
.action-bar { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.table-wrap { position: relative; margin-bottom: 10px; }
.ctx-menu { position: fixed; z-index: 3000; background: #fff; border: 1px solid #d9dce0; border-radius: 6px; box-shadow: 0 4px 14px rgba(0,0,0,.15); padding: 4px 0; }
.ctx-item { padding: 7px 18px; font-size: 13px; cursor: pointer; }
.ctx-item:hover { background: #ecf5ff; color: #409eff; }
.result-tabs { margin-top: 6px; }
.log-console { height: 180px; overflow-y: auto; background: #0f172a; color: #cbd5e1; font: 12px/1.6 SFMono-Regular, Consolas, monospace; padding: 8px; border-radius: 6px; }
.log-line { white-space: pre-wrap; word-break: break-all; }
:deep(.row-sel) { background: #ecf5ff; }
</style>