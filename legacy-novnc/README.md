# legacy-novnc —— 旧版部署（浏览器内嵌桌面 GUI）

早期方案：容器内跑 Xvfb + x11vnc + noVNC，把 Qt 桌面界面搬进浏览器。
已被仓库根目录的**原生 Web 应用**取代，此处仅保留供参考/回退。

用法（如仍需使用）：

```bash
docker compose -f legacy-novnc/docker-compose.yml up -d --build
# 访问 http://<主机IP>:33333/vnc.html（账号密码见其 .env 配置）
```

关键文件：

- `Dockerfile` / `docker-compose.yml` — noVNC 镜像与编排
- `docker/entrypoint.sh` — 启动脚本（含网页登录认证生成）
- `docker/nginx.conf` — 登录认证 + noVNC 反代
- `docker/smb-web.py` + `install-smb-web.sh` — 宿主机挂载管理器（网页 `/manager/`）
- `docker/mdcx-smb.sh` — 命令行挂载助手

> 宿主机挂载管理器（mdcx-smb-web）与 `/media` 挂载区机制在新版中继续沿用，
> 可参考 README 的"媒体目录与硬链接整理"一节。
## 小屏缩放（noVNC 1.5.0，已升级开箱即用）

- **双指捏合缩放**（触控板/触摸屏）：镜内置 noVNC 1.5.0，原生支持 pinch 手势缩放。
- **底部工具栏「缩放 / Local Scaling」**：随时点选（自适应/100%/自定义比例）——由浏览器处理，**在输入框选中文字时同样有效**，不会被远程界面抢走。
- **Ctrl+Alt+滚轮**：立即缩放。
- **固定比例**：`/vnc.html?scale=0.8`、`&scale=1.0`、`&scale=fit`。
- **调桌面分辨率**：`.env` 的 `SCREEN_W/SCREEN_H`（默认 1920×1080）；`NOVNC_SCALE=fit|0.8|1.0` 控制初始缩放。
