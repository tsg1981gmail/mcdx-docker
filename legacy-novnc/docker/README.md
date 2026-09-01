# mdcx-diy Docker 部署（网页访问，端口 33333）

mdcx-diy 是 Qt 桌面程序，容器内通过 **Xvfb + x11vnc + noVNC** 把整个 GUI 呈现在浏览器里：
访问 `http://<服务器IP>:33333` 即可在网页中操作完整界面（刮削、设置、工具等全部可用）。

```
浏览器 ──> nginx(33333, 账号密码登录) ──> noVNC 页面 + websockify ──> x11vnc ──> Xvfb ──> mdcx-diy(Qt)
```

## 1. 部署

在装有 Docker 的服务器上（本仓库根目录）：

```bash
# 构建并启动
docker compose up -d --build

# 查看运行状态 / 日志（首次启动会自动生成随机密码时也会打印在这里）
docker compose ps
docker compose logs -f
```

> 容器外只需开放 **33333** 端口（TCP）。

## 2. 网页访问与登录（权限管理）

- 浏览器打开：`http://<服务器IP>:33333/vnc.html`
- 登录账号密码由环境变量控制：
  | 变量 | 默认 | 说明 |
  |---|---|---|
  | `MDCX_WEB_USER` | `admin` | 网页登录用户名 |
  | `MDCX_WEB_PASSWORD` | 无 | 网页登录密码；**不设置则每次启动生成随机密码并打印在容器日志里** |
  | `VNC_PASSWORD` | 无 | 可选的 VNC 二层密码，与网页登录叠加 |
- 修改账号密码后 `docker compose up -d` 重建即可（配置主要在 `docker-compose.yml` 的 `environment` 段）。

## 3. 媒体目录与局域网共享（SMB·网页管理）

挂载局域网共享**不用敲命令**：浏览器打开 **`http://<服务器IP>:33333/manager/`**（与 mdcx-diy 网页同一个登录账号），页面有两个标签页：

**① SMB 局域网共享** —— 填：名称（容器内 `/media/` 下的目录名）· SMB 地址（`//IP/共享名`）· 用户名 · 密码 · SMB 版本（默认 3.0，老设备 2.0/1.0）。点"挂载"即可。

**② 宿主机文件夹** —— 把宿主机本地的目录（如 `/vol1/1000/video`）绑定进容器：填名称 + 宿主机绝对路径，可勾选只读。适合影片库在服务器本地盘的情况。

均可勾选"开机自动挂载"（写入 /etc/fstab）；页面可查看已挂载列表、一键卸载。挂载后立即出现在应用路径 `/media/<名称>`，无需重启容器。

- 挂载点为宿主机 `/vol1/smb/<名称>`，容器内 `/media/<名称>`（共享传播，无需重启容器）。
- 在网页应用里把"影片目录 / 输出目录"设为 `/media/<名称>`。
- 安全：管理服务只允许 docker 网桥与本机访问，局域网其它来源直接拒绝；对外必须经 33333 的登录认证。
- 备用命令行方式（与网页等效）：`sudo mdcx-smb add <名称> <//IP/共享名> [用户] [密码] [版本]`、`list`、`rm`；安装脚本 `docker/install-smb-web.sh` 重装/升级管理器。

### 容器数据持久化

配置、缓存等保存在命名卷 `mdcx-data`（挂载到容器 `/data`）。应用会自动把配置文件指向 `/data/config.json`，重建容器不丢失。

## 4. 更新 / 维护

```bash
git pull                        # 拉取上游更新（或重新上传源码）
docker compose up -d --build    # 重新构建并滚动重启
docker compose down             # 停止并删除容器（数据卷保留）
docker compose down -v          # 停止并删除容器 + 清空数据卷（慎用）
```

## 5. 常见问题

- **网页打不开 / 无法连接**：确认 33333 端口在防火墙放行；`docker compose ps` 显示 healthy。
- **忘了网页密码**：`docker compose logs` 里能看到未设置时生成的随机密码；或重新 `docker compose up -d --build` 并设置 `MDCX_WEB_PASSWORD`。
- **画面太小/太大**：调 `SCREEN_W`、`SCREEN_H`、`QT_SCALE_FACTOR` 环境变量后重建。
- **中文显示为方块**：镜像已内置 Noto CJK 中文字体，一般不会出现。
- **视频识别用哪个后端**：默认 PyAV（`av` 依赖），无需额外安装 ffmpeg。
- **应用崩溃自动重启**：Qt 主进程退出时容器随之退出，`restart: unless-stopped` 会自动拉起。

## 6. 关键文件

| 文件 | 作用 |
|---|---|
| `Dockerfile` | 镜像构建：Python 3.13 + PyQt6 依赖 + Xvfb/x11vnc/noVNC + nginx |
| `docker-compose.yml` | 端口 33333、数据卷、账号密码等环境变量 |
| `docker/entrypoint.sh` | 容器启动脚本（认证文件生成、各进程拉起） |
| `docker/nginx.conf` | 登录认证 + noVNC 静态页 + WebSocket 反向代理 |