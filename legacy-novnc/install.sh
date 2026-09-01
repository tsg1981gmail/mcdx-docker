#!/usr/bin/env bash
# ============================================================
# mdcx-diy 一键部署脚本（新机器）
# 用法:
#   ./install.sh              # 正常部署（有镜像包则离线加载，否则在线构建）
#   ./install.sh --build      # 强制在线构建（不加载镜像包）
#   ./install.sh --no-web     # 只起容器，不安装宿主机挂载管理器
# ============================================================
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
FORCE_BUILD=0
INSTALL_WEB=1
[ "${1:-}" = "--build" ] && FORCE_BUILD=1
[ "${1:-}" = "--no-web" ] && INSTALL_WEB=0

echo "==> 检查 Docker"
if docker info >/dev/null 2>&1; then
  DOCKER(){ docker "$@"; }
  DCOMPOSE(){ docker compose "$@"; }
else
  echo "当前用户无 Docker 权限，使用 sudo（会提示输入 sudo 密码）"
  if ! sudo docker info >/dev/null 2>&1; then
    echo "错误: 无法连接 Docker 守护进程，请确认 Docker 已安装并启动"; exit 1
  fi
  DOCKER(){ sudo docker "$@"; }
  DCOMPOSE(){ sudo docker compose "$@"; }
fi
SUDO(){ if [ "$(id -u)" = 0 ]; then "$@"; else sudo "$@"; fi; }

echo "==> 生成 .env（不存在时）"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "    已生成 .env，请用编辑器修改网页登录密码（MDCX_WEB_PASSWORD）"
fi

echo "==> 加载镜像/构建镜像"
if [ "$FORCE_BUILD" = 0 ] && [ -f mdcx-diy-image.tar.gz ]; then
  echo "    发现离线镜像包，正在加载 ..."
  DOCKER load -i mdcx-diy-image.tar.gz >/dev/null
  BUILD_FLAG=""
else
  echo "    在线构建镜像（首次需联网，约 5-10 分钟）..."
  BUILD_FLAG="--build"
fi

echo "==> 安装宿主机挂载管理器（网页 /manager/ 用）"
if [ "$INSTALL_WEB" = 1 ]; then
  SMB_BASE="$(sed -n 's/^MDCX_SMB_BASE=//p' .env 2>/dev/null | head -1)"
  [ -n "$SMB_BASE" ] || SMB_BASE=/vol1/smb
  SUDO bash docker/install-smb-web.sh "$SMB_BASE"
else
  SMB_BASE="$(sed -n 's/^MDCX_SMB_BASE=//p' .env 2>/dev/null | head -1)"
  SUDO mkdir -p "${SMB_BASE:-/vol1/smb}" 2>/dev/null || true
fi

echo "==> 启动容器"
DCOMPOSE up -d $BUILD_FLAG

sleep 8
# 优先取公网出口 IP（VPS 上 hostname -I 常列出 docker 内网地址）
IP="$(ip route get 1.1.1.1 2>/dev/null | sed -n 's/.*src \([0-9.]*\).*/\1/p' | head -1)"
[ -n "$IP" ] || IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
USER="$(sed -n 's/^MDCX_WEB_USER=//p' .env | head -1)"; [ -n "$USER" ] || USER=admin
PASS="$(sed -n 's/^MDCX_WEB_PASSWORD=//p' .env | head -1)"; [ -n "$PASS" ] || PASS=change-me
PORT="$(sed -n 's/^MDCX_WEB_PORT=//p' .env | head -1)"; [ -n "$PORT" ] || PORT=33333

echo
echo "=========================================================="
echo " 部署完成！使用方法："
echo "   应用界面: http://${IP}:${PORT}/vnc.html"
echo "   挂载管理: http://${IP}:${PORT}/manager/"
echo "   登录账号: ${USER} / ${PASS}"
echo "   挂载的共享/文件夹出现在容器 /media/<名称>"
echo "  （修改 .env 里的密码后: $(basename "$0") 重跑 或 docker compose up -d --build）"
echo "=========================================================="