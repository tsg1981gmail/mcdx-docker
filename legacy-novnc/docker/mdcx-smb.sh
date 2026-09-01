#!/usr/bin/env bash
# mdcx-smb —— 自行管理局域网 SMB 共享挂载（挂载后自动出现在容器 /media/<名称> 内）
# 用法：
#   sudo mdcx-smb add <名称> <//IP/共享名> [用户名] [密码] [SMB版本]
#   sudo mdcx-smb list
#   sudo mdcx-smb rm  <名称>
# 示例：
#   sudo mdcx-smb add movies //192.168.1.5/Movies myuser mypass 3.0
#   sudo mdcx-smb add movies //192.168.1.5/Movies          # 回车后交互输入用户名/密码
# 说明：
#   - 挂载到宿主机 /vol1/smb/<名称>，容器内经共享传播自动可见于 /media/<名称>
#   - 应用内 mdcx 用户 uid=1000/gid=1000，可读写共享
#   - 默认 SMB 3.0；老设备可加第 5 个参数指定 2.0 / 1.0
set -euo pipefail

BASE="${MDCX_SMB_BASE:-/vol1/smb}"
ACTION="${1:-help}"

case "$ACTION" in
  add)
    [ $# -ge 3 ] || { echo "用法: sudo mdcx-smb add <名称> <//IP/共享名> [用户名] [密码] [SMB版本]"; exit 1; }
    NAME="$2"; SRC="$3"
    USER="${4:-}"
    PASS="${5:-}"
    VERS="${6:-3.0}"
    [ -n "$USER" ] || { read -r -p "SMB 用户名: " USER; }
    [ -n "$PASS" ] || { read -r -s -p "SMB 密码: " PASS; echo; }
    TARGET="$BASE/$NAME"
    mkdir -p "$TARGET"
    if mountpoint -q "$TARGET"; then
      echo "已挂载，跳过: $TARGET"
    else
      mount.cifs "$SRC" "$TARGET" -o "username=$USER,password=$PASS,vers=$VERS,uid=1000,gid=1000,iocharset=utf8,file_mode=0664,dir_mode=0775,noserverino"
      echo "OK: $SRC -> $TARGET  （容器内路径 /media/$NAME）"
      echo "（如需开机自动挂载，把该 mount.cifs 命令加入 /etc/fstab 或系统启动脚本）"
    fi
    ;;
  list)
    echo "== 已挂载的局域网共享（/vol1/smb 下）:"
    mount | grep "$BASE" || echo "（无）"
    echo "== 容器内可见路径:  /media/<名称>"
    ;;
  rm)
    [ $# -ge 2 ] || { echo "用法: sudo mdcx-smb rm <名称>"; exit 1; }
    TARGET="$BASE/$2"
    if mountpoint -q "$TARGET"; then
      umount "$TARGET" && echo "已卸载: $TARGET"; rmdir "$TARGET" 2>/dev/null || true
    else
      echo "未挂载: $TARGET"; rmdir "$TARGET" 2>/dev/null || true
    fi
    ;;
  *)
    echo "用法: sudo mdcx-smb {add|list|rm}"
    echo "  add <名称> <//IP/共享名> [用户名] [密码] [SMB版本]"
    ;;
esac