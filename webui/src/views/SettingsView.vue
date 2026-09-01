<template>
  <el-card>
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>设置（/data/config.json，与原版设置页分组对应）</span>
        <div>
          <el-button type="primary" :loading="saving" @click="saveForm">保存</el-button>
          <el-button @click="load">重新读取</el-button>
        </div>
      </div>
    </template>

    <el-tabs v-model="mode">
      <el-tab-pane label="常用设置" name="form">
        <el-form label-width="150px" size="small">
          <el-divider content-position="left">刮削目录</el-divider>
          <el-form-item label="待刮削目录（;分隔）">
            <el-input v-model="f.media_path" placeholder="D:\Media\Input 或 /media/src" />
          </el-form-item>
          <el-form-item label="成功输出目录">
            <el-input v-model="f.success_output_folder" />
          </el-form-item>
          <el-form-item label="失败输出目录">
            <el-input v-model="f.failed_output_folder" />
          </el-form-item>

          <el-divider content-position="left">刮削模式</el-divider>
          <el-form-item label="刮削模式">
            <el-radio-group v-model="f.main_mode">
              <el-radio :value="1">正常模式</el-radio>
              <el-radio :value="2">整理模式</el-radio>
              <el-radio :value="3">更新模式</el-radio>
              <el-radio :value="4">读取模式</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="刮削方式">
            <el-select v-model="f.scrape_like" style="width:220px">
              <el-option label="信息优先" value="info" />
              <el-option label="速度优先" value="speed" />
              <el-option label="单站刮削" value="single" />
            </el-select>
          </el-form-item>
          <el-form-item label="多线程刮削数">
            <el-input-number v-model="f.thread_number" :min="1" :max="200" />
          </el-form-item>
          <el-form-item label="成功后软硬链接">
            <el-select v-model="f.soft_link" style="width:220px">
              <el-option label="移动（默认）" :value="0" />
              <el-option label="创建软链接" :value="1" />
              <el-option label="创建硬链接" :value="2" />
            </el-select>
          </el-form-item>
          <el-form-item label="成功移动 / 重命名">
            <el-switch v-model="f.success_file_move" active-text="移动" inactive-text="不移动" />
            <el-switch v-model="f.success_file_rename" active-text="重命名" inactive-text="不重命名" style="margin-left:12px" />
          </el-form-item>
          <el-form-item label="失败移动 / 删除空文件夹">
            <el-switch v-model="f.failed_file_move" active-text="移动失败文件" />
            <el-switch v-model="f.del_empty_folder" active-text="删除空文件夹" style="margin-left:12px" />
          </el-form-item>

          <el-divider content-position="left">刮削网站</el-divider>
          <el-form-item v-for="g in SITE_GROUPS" :key="g.key" :label="g.label">
            <el-input v-model="siteTexts[g.key]" placeholder="站点名，逗号分隔" />
          </el-form-item>
          <el-form-item label="固定刮削类型">
            <el-select v-model="f.fixed_scraping_type" style="width:220px">
              <el-option label="自动" value="auto" />
              <el-option label="有码" value="youma" />
              <el-option label="无码" value="wuma" />
              <el-option label="素人" value="suren" />
              <el-option label="FC2" value="fc2" />
              <el-option label="欧美" value="oumei" />
              <el-option label="国产" value="guochan" />
            </el-select>
          </el-form-item>

          <el-divider content-position="left">命名规则</el-divider>
          <el-form-item label="目录模板 folder_name">
            <el-input v-model="f.folder_name" />
          </el-form-item>
          <el-form-item label="文件模板 naming_file">
            <el-input v-model="f.naming_file" />
          </el-form-item>
          <el-form-item label="NFO 标题模板 naming_media">
            <el-input v-model="f.naming_media" />
          </el-form-item>

          <el-divider content-position="left">翻译 / LLM</el-divider>
          <el-form-item label="翻译引擎（逗号分隔）">
            <el-input v-model="f.translate_by" />
          </el-form-item>
          <el-form-item label="LLM URL">
            <el-input v-model="f.translate_llm_url" placeholder="https://api.deepseek.com/v1" />
          </el-form-item>
          <el-form-item label="LLM 模型">
            <el-input v-model="f.translate_llm_model" placeholder="deepseek-chat" />
          </el-form-item>
          <el-form-item label="LLM Key（留空不改）">
            <el-input v-model="f.translate_llm_key" type="password" show-password placeholder="已设置则留空" />
          </el-form-item>

          <el-divider content-position="left">网络 / 代理</el-divider>
          <el-form-item label="使用代理">
            <el-switch v-model="f.use_proxy" />
          </el-form-item>
          <el-form-item label="代理地址">
            <el-input v-model="f.proxy" placeholder="http://127.0.0.1:7890" />
          </el-form-item>
          <el-form-item label="全部走代理">
            <el-switch v-model="f.proxy_route_all" />
          </el-form-item>

          <el-divider content-position="left">Emby / Jellyfin</el-divider>
          <el-form-item label="启用 Emby 集成">
            <el-switch v-model="f.emby_on" />
          </el-form-item>
          <el-form-item label="Emby URL">
            <el-input v-model="f.emby_url" />
          </el-form-item>
          <el-form-item label="API Key（留空不改）">
            <el-input v-model="f.emby_api_key" type="password" show-password placeholder="已设置则留空" />
          </el-form-item>
        <el-divider content-position="left">更新模式规则</el-divider>
          <el-form-item label="更新模式">
            <el-select v-model="f.update_mode" style="width:180px">
              <el-option label="A" value="a" />
              <el-option label="B" value="b" />
              <el-option label="C（仅文件）" value="c" />
              <el-option label="D" value="d" />
            </el-select>
          </el-form-item>
          <el-form-item label="A/B/C/D 目录">
            <el-switch v-model="f.update_a_folder" active-text="更新A(上层)" />
            <el-switch v-model="f.update_b_c" active-text="更新B和C(目录+文件)" style="margin-left:12px" />
            <el-switch v-model="f.update_d_folder" active-text="创建D目录" style="margin-left:12px" />
          </el-form-item>
          <el-form-item label="C 文件模板">
            <el-input v-model="f.update_c_filetemplate" />
          </el-form-item>
          <el-form-item label="标题模板">
            <el-input v-model="f.update_titletemplate" />
          </el-form-item>

          <el-divider content-position="left">图片下载 / 保留</el-divider>
          <el-form-item label="下载文件">
            <el-select v-model="f.download_files" multiple collapse-tags style="width:100%">
              <el-option v-for="v in DL_FILES" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item label="保留旧文件">
            <el-select v-model="f.keep_files" multiple collapse-tags style="width:100%">
              <el-option v-for="v in KEEP_FILES" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>

          <el-divider content-position="left">写入 NFO 的字段</el-divider>
          <el-form-item label="NFO 字段">
            <el-select v-model="f.nfo_include_new" multiple collapse-tags style="width:100%">
              <el-option v-for="v in NFO_INCLUDE" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>

          <el-divider content-position="left">水印设置</el-divider>
          <el-form-item label="启用海报水印">
            <el-switch v-model="f.poster_mark" />
          </el-form-item>
          <el-form-item label="水印字号">
            <el-input-number v-model="f.mark_size" :min="1" :max="100" />
          </el-form-item>

          <el-divider content-position="left">站点自定义 URL</el-divider>
          <el-form-item label="站点|URL（每行一个）">
            <el-input v-model="f.site_custom" type="textarea" :rows="5" placeholder="javbus|https://我的镜像/cist" />
          </el-form-item>

          <el-divider content-position="left">API Token（留空不改）</el-divider>
          <el-form-item label="theporndb 令牌">
            <el-input v-model="f.theporndb_api_token" type="password" show-password placeholder="已设置则留空" />
          </el-form-item>
          <el-form-item label="TMDB API Key">
            <el-input v-model="f.tmdb_api_key" type="password" show-password placeholder="已设置则留空" />
          </el-form-item>
        </el-form>
        <el-alert type="info" :closable="false"
          title='未覆盖的配置项（图片下载/水印/更新规则/NFO字段/站点自定义URL等）请用"高级(JSON)"编辑。' />
      </el-tab-pane>

      <el-tab-pane label="高级（JSON）" name="json">
        <el-input v-model="json" type="textarea" :rows="24" style="font-family:monospace" />
        <el-tag v-if="saveMsg" :type="saveOk ? 'success' : 'danger'" style="margin-top:10px">{{ saveMsg }}</el-tag>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../api'

const mode = ref('form')
const saving = ref(false)
const json = ref('')
const saveMsg = ref('')
const saveOk = ref(false)

const SITE_GROUPS = [
  { key: 'website_youma', label: '有码网站' },
  { key: 'website_wuma', label: '无码网站' },
  { key: 'website_suren', label: '素人网站' },
  { key: 'website_fc2', label: 'FC2 网站' },
  { key: 'website_oumei', label: '欧美网站' },
  { key: 'website_guochan', label: '国产网站' },
]

const f = reactive<any>({
  media_path: '', success_output_folder: '', failed_output_folder: '',
  main_mode: 1, scrape_like: 'info', thread_number: 50, soft_link: 0,
  success_file_move: true, success_file_rename: true, failed_file_move: true, del_empty_folder: false,
  fixed_scraping_type: 'auto', folder_name: '', naming_file: '', naming_media: '',
  translate_by: '', translate_llm_url: '', translate_llm_model: '', translate_llm_key: '',
  use_proxy: false, proxy: '', proxy_route_all: false,
  emby_on: false, emby_url: '', emby_api_key: '',
  update_mode: 'c', update_a_folder: false, update_b_c: true, update_d_folder: false,
  update_c_filetemplate: '', update_titletemplate: '',
  download_files: [], keep_files: [], nfo_include_new: [],
  poster_mark: false, mark_size: 20, site_custom: '',
  theporndb_api_token: '', tmdb_api_key: '',
})
const DL_FILES = ['poster','thumb','fanart','extrafanart','trailer','nfo','extrafanart_extras','extrafanart_copy','theme_videos','ignore_pic_fail','ignore_youma','poster_auto_best','ignore_wuma','ignore_oumei','ignore_fc2','ignore_guochan','ignore_size']
const KEEP_FILES = ['poster','thumb','fanart','extrafanart','trailer','nfo','extrafanart_copy','theme_videos']
const NFO_INCLUDE = ['sorttitle','originaltitle','title_cd','outline','plot_','originalplot','outline_no_cdata','release_','releasedate','premiered','country','mpaa','customrating','year','runtime','wanted','score','criticrating','actor','actor_all','actor_tmdbid','director','series','tag','genre','actor_set','series_set','studio','maker','publisher','label','poster','cover','trailer','website']
const siteTexts = reactive<any>({})

async function load() {
  const d = await api.configGet()
  if (!d.ok) return
  const c = d.config
  f.media_path = c.media_path ?? ''
  f.success_output_folder = c.success_output_folder ?? ''
  f.failed_output_folder = c.failed_output_folder ?? ''
  f.main_mode = c.main_mode ?? 1
  f.scrape_like = c.scrape_like ?? 'info'
  f.thread_number = c.thread_number ?? 50
  f.soft_link = c.soft_link ?? 0
  f.success_file_move = !!c.success_file_move
  f.success_file_rename = !!c.success_file_rename
  f.failed_file_move = !!c.failed_file_move
  f.del_empty_folder = !!c.del_empty_folder
  f.fixed_scraping_type = c.fixed_scraping_type ?? 'auto'
  f.folder_name = c.folder_name ?? ''
  f.naming_file = c.naming_file ?? ''
  f.naming_media = c.naming_media ?? ''
  const tc = c.translate_config ?? {}
  f.translate_by = (tc.translate_by || []).join(',')
  f.translate_llm_url = tc.llm_url ?? ''
  f.translate_llm_model = tc.llm_model ?? ''
  f.translate_llm_key = ''   // 打码不回显
  f.use_proxy = !!c.use_proxy
  f.proxy = c.proxy ?? ''
  f.proxy_route_all = !!c.proxy_route_all
  f.emby_on = !!c.emby_on
  f.emby_url = c.emby_url ?? ''
  f.emby_api_key = ''
  f.update_mode = c.update_mode ?? 'c'
  f.update_a_folder = !!c.update_a_folder
  f.update_b_c = !!c.update_b_c
  f.update_d_folder = !!c.update_d_folder
  f.update_c_filetemplate = c.update_c_filetemplate ?? ''
  f.update_titletemplate = c.update_titletemplate ?? ''
  f.download_files = [...(c.download_files || [])]
  f.keep_files = [...(c.keep_files || [])]
  f.nfo_include_new = [...(c.nfo_include_new || [])]
  f.poster_mark = !!c.poster_mark
  f.mark_size = c.mark_size ?? 20
  f.site_custom = Object.entries(c.site_configs || {})
    .map(([k, v]: any) => (v?.custom_url ? `${k}|${v.custom_url}` : '')).filter(Boolean).join('\n')
  f.theporndb_api_token = ''
  f.tmdb_api_key = ''
  for (const g of SITE_GROUPS) siteTexts[g.key] = (c[g.key] || []).join(',')
  json.value = JSON.stringify(c, null, 2)
}

async function saveForm() {
  saving.value = true
  try {
    const patch: any = {
      media_path: f.media_path, success_output_folder: f.success_output_folder,
      failed_output_folder: f.failed_output_folder,
      main_mode: f.main_mode, scrape_like: f.scrape_like, thread_number: f.thread_number,
      soft_link: f.soft_link, success_file_move: f.success_file_move,
      success_file_rename: f.success_file_rename, failed_file_move: f.failed_file_move,
      del_empty_folder: f.del_empty_folder,
      fixed_scraping_type: f.fixed_scraping_type,
      folder_name: f.folder_name, naming_file: f.naming_file, naming_media: f.naming_media,
      use_proxy: f.use_proxy, proxy: f.proxy, proxy_route_all: f.proxy_route_all,
      emby_on: f.emby_on, emby_url: f.emby_url,
    }
    for (const g of SITE_GROUPS) {
      patch[g.key] = siteTexts[g.key].split(/[,，\s]+/).filter(Boolean)
    }
    patch.translate_config = {
      translate_by: f.translate_by.split(/[,，\s]+/).filter(Boolean),
      llm_url: f.translate_llm_url, llm_model: f.translate_llm_model,
    }
    if (f.translate_llm_key) patch.translate_config.llm_key = f.translate_llm_key
    if (f.emby_api_key) patch.emby_api_key = f.emby_api_key
    patch.update_mode = f.update_mode
    patch.update_a_folder = f.update_a_folder
    patch.update_b_c = f.update_b_c
    patch.update_d_folder = f.update_d_folder
    patch.update_c_filetemplate = f.update_c_filetemplate
    patch.update_titletemplate = f.update_titletemplate
    patch.download_files = f.download_files
    patch.keep_files = f.keep_files
    patch.nfo_include_new = f.nfo_include_new
    patch.poster_mark = f.poster_mark
    patch.mark_size = f.mark_size
    const siteCustom: any = {}
    for (const line of f.site_custom.split('\n')) {
      const [k, ...rest] = line.split('|')
      const v = rest.join('|').trim()
      if (k && v) siteCustom[k.trim()] = { custom_url: v }
    }
    patch.site_configs = siteCustom
    if (f.theporndb_api_token) patch.theporndb_api_token = f.theporndb_api_token
    if (f.tmdb_api_key) patch.tmdb_api_key = f.tmdb_api_key
    const r = await api.configPut(patch)
    saveOk.value = r.ok
    saveMsg.value = r.ok ? '已保存' : (r.error || '保存失败')
    if (r.ok) await load()
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>