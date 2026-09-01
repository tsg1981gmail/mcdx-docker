#!/usr/bin/env bash
# 健康检查：nginx 在 33333 端口已响应即可（401 = 认证已生效，200 = 已登录会话）
code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://127.0.0.1:33333/ 2>/dev/null || true)"
case "$code" in
  401|200) exit 0 ;;
  *) exit 1 ;;
esac