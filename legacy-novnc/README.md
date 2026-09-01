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