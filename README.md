# mcdx-docker

基于 [mdcx-diy](https://github.com/cdlongbow/mdcx-diy) 的 **原生 Web 刮削与整理** 应用，Docker 一键部署。

- 🖥️ **原生网页界面**（Vue3 + Element Plus，FastAPI 后端）——不再需要 noVNC 套壳
- 🔗 **硬链接整理**：把刮削好的影片按命名模板整理进媒体库，**同盘硬链接、跨盘自动回退复制**
- 🗂️ 目录扫描 / 批量刮削（复用 mdcx 全部爬虫与元数据处理）/ nfo 与海报写入 / 任务进度与取消
- ⚙️ 网页直接读写 mdcx 配置（`config.json`），工具页（演员库等逐步接入）
- 🐳 镜像发布到 **GitHub Container Registry**（GHCR），免构建直接拉取

> 完整保留 mdcx 核心能力（35+ 站点刮削、命名模板、翻译/LLM、演员库），只是把界面换成了网页。
> 旧版"浏览器内嵌桌面（noVNC）"部署见 [`legacy-novnc/`](legacy-novnc/)，不再维护。

---

## 快速安装（Docker）

### 方式 A：拉取现成镜像（推荐）

```bash
git clone https://github.com/tsg1981gmail/mcdx-docker.git
cd mcdx-docker
cp .env.example .env          # 按需修改端口/挂载目录
docker compose up -d          # 自动从 GHCR 拉取 ghcr.io/tsg1981gmail/mcdx-docker
```

### 方式 B：本地构建

```bash
docker compose up -d --build
```

### 打开

浏览器访问 **`http://<主机IP>:33333`**（端口可在 `.env` 的 `MDCX_WEB_PORT` 修改）。

---

## 媒体目录与硬链接整理

容器内统一以 **`/media`** 作为挂载区：把宿主机目录（本地目录、SMB 局域网共享、NFS、NAS 目录均可）挂载到它下面即可：

```yaml
# docker-compose.yml volumes 段
- type: bind
  source: ${MDCX_SMB_BASE:-/vol1/smb}   # 改成你的宿主机目录，如 /srv/media
  target: /media
```

然后在网页 **整理页** 配置：

- **源目录**：`/media/xxx`（原始影片，建议挂载为只读）
- **目标库目录**：`/media/library`（整理结果库）
- **链接方式**：硬链接（同盘，省空间）/ 复制（跨盘）

整理逻辑：扫描源目录 → 逐个刮削（番号解析、多站抓取、翻译）→ 按命名模板渲染目标路径 → **`os.link` 硬链接，跨文件系统（EXDEV）自动回退为原子复制** → 写入 nfo / 海报。源文件保持不动（保种），目标已存在且同源自动跳过。

> ⚠️ 硬链接要求源与目标库在同一文件系统。跨盘时自动用复制，注意空间占用。

---

## 配置说明（.env）

| 变量 | 默认 | 说明 |
|---|---|---|
| `MDCX_WEB_PORT` | `33333` | 网页端口 |
| `MDCX_SMB_BASE` | `/vol1/smb` | 宿主机媒体挂载区（对应容器 `/media`） |
| `MDCX_LIBRARY_ROOT` | `/media` | 整理目标库根目录（容器内路径） |
| `MDCX_LOG_LEVEL` | `INFO` | 日志级别 |
| `TZ` | `Asia/Shanghai` | 时区 |

mdcx 应用配置（站点优先级、命名模板、翻译/LLM 密钥、代理等）在网页 **设置** 页直接读写，保存在数据卷 `/data/config.json`。

---

## 页面功能

| 页面 | 功能 |
|---|---|
| 任务总览 | 服务状态、任务列表与进度 |
| 目录扫描 | 浏览 `/media`，扫描视频文件清单 |
| 批量刮削 | 选择目录 → 批量刮削（进度/取消） |
| 整理 / 硬链接 | 源目录 → 目标库，硬链接/复制，结果统计 |
| 工具 | Gfriends 同步等（陆续接入演员库/字幕/缺失检查） |
| 设置 | 读写 mdcx `config.json`（敏感字段打码） |

---

## 常见问题

- **刮削无结果（no_meta）**：多为服务器网络无法访问刮削站点（部分站点需要代理）。在网页设置里配置 `use_proxy`/`proxy` 后重试。
- **硬链接失败**：跨盘时自动复制，属正常策略；若同盘仍失败，检查挂载是否只读、文件系统是否支持硬链接（NFS/fuse 网络盘不支持）。
- **改端口/挂载后**：`docker compose up -d` 重建即可；数据在 `mdcx-data` 卷中不丢失。

## 开发构建

```bash
# 前端
cd webui && npm install && npm run build   # 产物 webui/dist 已提交

# 后端/镜像
docker build -t mcdx-docker .               # 或 docker compose up -d --build
```

## 协议与致谢

- 本项目衍生自 [mdcx-diy](https://github.com/cdlongbow/mdcx-diy)（GPL-3.0），同样以 **GPL-3.0** 开源：见 [LICENSE](LICENSE)。
- 感谢 mdcx-diy 作者与 Hazard804 原版 MDCx 项目。