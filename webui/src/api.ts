import axios from 'axios'

export const http = axios.create({ baseURL: '/api', timeout: 30000 })

export interface TaskSnapshot {
  id: string
  kind: string
  title: string
  status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled'
  progress: number
  detail: string
  total: number
  done: number
  error: string
  created: number
  updated: number
  result: unknown
}

export const api = {
  health: () => http.get('/system/health'),
  tasks: () => http.get('/tasks').then(r => r.data.tasks as TaskSnapshot[]),
  cancelTask: (id: string) => http.post(`/tasks/${id}/cancel`),
  removeTask: (id: string) => http.post(`/tasks/${id}/remove`),
  listDir: (path: string) => http.get('/files/list', { params: { path } }).then(r => r.data),
  scan: (path: string) => http.post('/scan/scan', { path, deep: true, limit: 5000 }).then(r => r.data),
  configGet: () => http.get('/config').then(r => r.data),
  configPut: (payload: any) => http.put('/config', payload).then(r => r.data),
  crawlerPreview: (path: string) => http.get('/crawl/preview', { params: { path } }).then(r => r.data),
  crawlerStart: (path: string, mode: string = 'common') => http.post('/crawl/start', { path, mode, title: '批量刮削' }).then(r => r.data),
  crawlerStartFiles: (files: string[], mode: string = 'common', force: boolean = false) => http.post('/crawl/start', { files, mode, force, title: '单文件刮削' }).then(r => r.data),
  organizePreview: (source: string, library: string) => http.post('/organize/preview', { source, library, mode: 'hardlink' }).then(r => r.data),
  organizeStart: (payload: any) => http.post('/organize/start', payload).then(r => r.data),
}

export function taskStatusText(s: TaskSnapshot['status']) {
  return { pending: '等待中', running: '进行中', success: '成功', failed: '失败', cancelled: '已取消' }[s]
}

export function taskStatusType(s: TaskSnapshot['status']) {
  return { pending: 'info', running: 'primary', success: 'success', failed: 'danger', cancelled: 'info' }[s] as any
}