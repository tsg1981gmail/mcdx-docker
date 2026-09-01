#!/usr/bin/env bash
# 安装 mdcx-diy 挂载管理器（root 运行）
# 用法: sudo ./install-smb-web.sh [挂载区目录]
# 挂载区默认 /vol1/smb，其它机器可用参数或环境变量 MDCX_SMB_BASE 指定
set -euo pipefail

SMB_BASE="${1:-${MDCX_SMB_BASE:-/vol1/smb}}"
APP_DIR="/opt/mdcx-smb-web"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/smb-web.py"

mkdir -p "$SMB_BASE"
echo "==> 挂载区: $SMB_BASE"

echo "==> 复制服务到 $APP_DIR"
mkdir -p "$APP_DIR"
install -m 0644 "$SRC" "$APP_DIR/smb-web.py"

echo "==> 写入 systemd 单元"
cat > /etc/systemd/system/mdcx-smb-web.service <<EOF
[Unit]
Description=mdcx-diy 挂载网页管理器
After=network.target

[Service]
Environment=MDCX_SMB_BASE=$SMB_BASE
ExecStart=/usr/bin/python3 $APP_DIR/smb-web.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "==> 启动并设置开机自启"
systemctl daemon-reload
systemctl enable --now mdcx-smb-web
systemctl --no-pager status mdcx-smb-web --full | head -5 || true
echo
echo "完成。浏览器访问（需要 mdcx-diy 网页登录账号）："
echo "  http://<服务器IP>:33333/manager/"
echo "（nginx 由容器提供；若容器尚未重建，请先 docker compose up -d --build）"