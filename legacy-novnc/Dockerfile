# mdcx-diy 容器化镜像：Qt 桌面应用 + Xvfb + x11vnc + noVNC，浏览器访问 33333 端口（需账号密码登录）
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# Qt6/xcb 运行库 + 虚拟显示/VNC/noVNC + 认证代理(nginx) + 中文字体 + 工具
# libqt6gui6：其依赖拉齐 Qt xcb 平台插件所需的全部 libxcb-* 系统库
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl tini openssl procps \
        nginx-light \
        libqt6gui6 \
        libgl1 libegl1 libxkbcommon0 libdbus-1-3 \
        libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-shape0 \
        libxcb-xinerama0 libxcb-render-util0 libxfixes3 libxi6 \
        libxrender1 libxext6 libsm6 libice6 libx11-xcb1 \
        libfontconfig1 libglib2.0-0 shared-mime-info \
        fonts-noto-cjk \
        xvfb x11vnc novnc websockify \
    && rm -rf /var/lib/apt/lists/*

# 升级 noVNC 到 1.5.0：内置双指捏合缩放、更好的缩放控件（旧 Debian 1.1.0 无触控缩放）。覆盖系统包。
COPY novnc/ /usr/share/novnc/

WORKDIR /app

# 安装 Python 依赖（pyproject.toml 固定版本，均为 manylinux wheel）
COPY pyproject.toml README.md LICENSE ./
COPY mdcx mdcx
COPY main.py ./
COPY resources resources

RUN pip install --no-cache-dir . \
    && useradd -m -u 1000 mdcx \
    && mkdir -p /data /etc/nginx/auth \
    && chown -R mdcx:mdcx /app /data

COPY docker/entrypoint.sh /usr/local/bin/mdcx-entrypoint
COPY docker/healthcheck.sh /usr/local/bin/mdcx-healthcheck
COPY docker/nginx.conf /etc/nginx/nginx.conf
RUN chmod +x /usr/local/bin/mdcx-entrypoint /usr/local/bin/mdcx-healthcheck

EXPOSE 33333
HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
  CMD ["/usr/local/bin/mdcx-healthcheck"]

ENTRYPOINT ["/usr/local/bin/mdcx-entrypoint"]