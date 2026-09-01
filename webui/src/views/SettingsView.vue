<template>
  <el-card>
    <template #header>设置（/data/config.json，mdcx 配置）</template>
    <div style="margin-bottom:10px;font-size:13px;color:#666">
      配置路径：{{ info.config_path }} · 数据目录：{{ info.data_folder }}
    </div>
    <el-button type="primary" @click="save" style="margin-bottom:10px">保存配置（校验 + 原子写入）</el-button>
    <el-button @click="load" style="margin-bottom:10px">重新读取</el-button>
    <el-input v-model="json" type="textarea" :rows="24" style="font-family:monospace" />
    <el-tag v-if="saveMsg" :type="saveOk ? 'success' : 'danger'" style="margin-top:10px">{{ saveMsg }}</el-tag>
    <div style="margin-top:14px;font-size:12px;color:#888">
      ⚠️ 敏感字段在读取时已打码；保存时请填入真实值<br>
      常用键：media_path（源，分号分隔）、success_output_folder（输出）、folder_name（目录模板）、
      naming_file（文件模板）、website_youma / website_wuma（站点优先级）、translate_config（翻译/LLM）、
      proxy / use_proxy（网络）、soft_link（0 移动 / 1 软链 / 2 硬链）
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api'

const json = ref('')
const info = ref<any>({})
const saveMsg = ref('')
const saveOk = ref(false)

async function load() {
  const d = await api.configGet()
  if (!d.ok) { alert(d.error || '读取失败'); return }
  info.value = d
  json.value = JSON.stringify(d.config, null, 2)
}
async function save() {
  saveMsg.value = ''
  let payload: any
  try { payload = JSON.parse(json.value) } catch {
    saveMsg.value = 'JSON 语法错误'; saveOk.value = false; return
  }
  const r = await api.configPut(payload)
  saveOk.value = r.ok
  saveMsg.value = r.ok ? `已保存（${r.config_path}）${r.errors?.length ? '，有迁移提示: ' + r.errors.join('; ') : ''}` : r.error || '保存失败'
}

onMounted(load)
</script>