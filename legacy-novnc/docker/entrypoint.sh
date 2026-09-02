#!/usr/bin/env bash
set -euo pipefail

# ============ 配置 ============
export DISPLAY="${DISPLAY:-:99}"
SCREEN_W="${SCREEN_W:-1920}"
SCREEN_H="${SCREEN_H:-1080}"
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

# ============ 小屏友好首页：自动带缩放进入 noVNC ============
# NOVNC_SCALE=fit 自适应窗口 / 0.5~1.5 固定比例 / 空=默认。
# 另附 noVNC 缩放操作提示（底部工具栏“缩放”菜单；Ctrl+Alt+滚轮即时缩放）。
NOVNC_SCALE="${NOVNC_SCALE:-fit}"
cat > /usr/share/novnc/index.html <<HTML
<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8">
<meta http-equiv="refresh" content="0;url=/vnc.html?scale=${NOVNC_SCALE}&autoconnect=1">
<title>mdcx-diy 桌面</title></head>
<body style="font-family:system-ui;background:#111;color:#ddd;display:flex;flex-direction:column;align-items:center;gap:14px;padding:80px 20px">
<h2>正在进入原版桌面界面…</h2>
<p>缩放方式（进入后任意时刻可用）：
  <b>双指捏合</b>（触控板/触摸屏）｜底部工具栏「缩放/Local Scaling」按钮｜<b>Ctrl+Alt+滚轮</b>
</p>
<p style="font-size:13px;color:#999">选中文字/输入框时同样可缩放（按钮与捏合由浏览器处理，不会被界面抢走）。</p>
<p>初始缩放：${NOVNC_SCALE}
  <a href="/vnc.html?scale=fit&autoconnect=1">自适应</a> ·
  <a href="/vnc.html?scale=1.0&autoconnect=1">100%</a> ·
  <a href="/vnc.html?scale=0.8&autoconnect=1">80%</a>
</p>
<p><a href="/vnc.html?scale=${NOVNC_SCALE}&autoconnect=1">手动进入</a></p>
</body>
</html>
HTML

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

# ============ 进程看门狗：核心服务掉线自动拉起，防止“页面一直在加载” ============
(
  while : ; do
    pgrep -f "Xvfb :99" >/dev/null || { echo "[mdcx] Xvfb 掉线，重新拉起"; Xvfb :99 -screen 0 "${SCREEN_W}x${SCREEN_H}x24" -nolisten tcp -ac >/dev/null 2>&1 & sleep 1; }
    pgrep -f "x11vnc -display :99" >/dev/null || { echo "[mdcx] x11vnc 掉线，重新拉起"; "${VNC_ARGS[@]}" >/dev/null 2>&1 & }
    pgrep -f "websockify 127.0.0.1" >/dev/null || { echo "[mdcx] websockify 掉线，重新拉起"; websockify 127.0.0.1:"$WS_PORT" localhost:"$VNC_PORT" >/dev/null 2>&1 & }
    sleep 15
  done
) &

# ============ 主应用 (Qt, 前台运行) ============
su mdcx -s /bin/bash -c "cd /app && QT_SCALE_FACTOR=\${QT_SCALE_FACTOR:-1} exec python3 main.py" &
APP_PID=$!
wait "$APP_PID"
STATUS=$?
echo "[mdcx-diy] 主应用退出，code=$STATUS"
exit "$STATUS"