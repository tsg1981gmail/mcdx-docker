#!/usr/bin/env bash
set -euo pipefail

# ============ 配置 ============
export DISPLAY="${DISPLAY:-:99}"
SCREEN_W="${SCREEN_W:-1600}"
SCREEN_H="${SCREEN_H:-1000}"
VNC_PORT="${VNC_PORT:-5900}"
# websockify 只监听容器内回环，对外一律走 nginx(33333) 且要求登录
WS_PORT="${WS_PORT:-5901}"
WEB_PORT="${WEB_PORT:-33333}"

# ============ 网页登录账号密码（权限管理） ============
WEB_USER="${MDCX_WEB_USER:-admin}"
if [ -n "${MDCX_WEB_PASSWORD:-}" ]; then
  WEB_PASSWORD="$MDCX_WEB_PASSWORD"
else
  WEB_PASSWORD="$(openssl rand -hex 8)"
  echo "*********************************************"
  echo "* 未设置 MDCX_WEB_PASSWORD，已生成随机密码："
  echo "*   用户名: ${WEB_USER}"
  echo "*   密码:   ${WEB_PASSWORD}"
  echo "* 请登录 http://<服务器IP>:${WEB_PORT}/vnc.html 使用"
  echo "* 建议启动时通过环境变量 MDCX_WEB_USER / MDCX_WEB_PASSWORD 固定账号密码"
  echo "*********************************************"
fi
mkdir -p /etc/nginx/auth
SALT="$(openssl rand -hex 4)"
printf '%s:%s\n' "$WEB_USER" "$(openssl passwd -apr1 -salt "$SALT" "$WEB_PASSWORD")" > /etc/nginx/auth/.htpasswd
# nginx worker 以 nginx 用户运行，需可读该文件
chmod 644 /etc/nginx/auth/.htpasswd

# ============ 数据目录与配置标记 ============
mkdir -p /data
chown -R mdcx:mdcx /data 2>/dev/null || true
# MDCx.config 指向 /data/config.json，保证配置/缓存持久化在数据卷
if [ ! -f /app/MDCx.config ]; then
  printf '%s' '/data/config.json' > /app/MDCx.config
  chown mdcx:mdcx /app/MDCx.config
fi

cleanup() {
  echo "[mdcx-diy] 正在停止 ..."
  jobs -p | xargs -r kill 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# ============ 虚拟显示 (Xvfb) ============
Xvfb :99 -screen 0 "${SCREEN_W}x${SCREEN_H}x24" -nolisten tcp -ac &
sleep 1

# ============ VNC 服务 (x11vnc) ============
VNC_ARGS=(x11vnc -display :99 -forever -shared -rfbport "$VNC_PORT" \
          -noxdamage -xkb -ncache 10 -quiet)
if [ -n "${VNC_PASSWORD:-}" ]; then
  VNCPASS="/home/mdcx/.vncpasswd"
  x11vnc -storepasswd "$VNC_PASSWORD" "$VNCPASS"
  VNC_ARGS+=( -rfbauth "$VNCPASS" )
fi
"${VNC_ARGS[@]}" &

# ============ WebSocket 隧道 (websockify) ============
websockify 127.0.0.1:"$WS_PORT" localhost:"$VNC_PORT" &

# ============ 带登录认证的 Web 入口 (nginx, 对外 33333) ============
nginx -g "daemon off;" &

# ============ 主应用 (Qt, 前台运行) ============
su mdcx -s /bin/bash -c "cd /app && QT_SCALE_FACTOR=\${QT_SCALE_FACTOR:-1} exec python3 main.py" &
APP_PID=$!
wait "$APP_PID"
STATUS=$?
echo "[mdcx-diy] 主应用退出，code=$STATUS"
exit "$STATUS"