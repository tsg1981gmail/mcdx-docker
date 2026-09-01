# ============================================================
# mdcx-web：原生 Web 应用镜像（纯网页，无 noVNC/Xvfb）
# 前端已构建产物 webui/dist 直接打入镜像（免去构建期 npm 联网）。
# 如需从源码重建前端：先在 webui/ 执行 npm install && npm run build。
# ============================================================
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_RETRIES=5 \
    PIP_TIMEOUT=60 \
    HTTP_PROXY= \
    HTTPS_PROXY= \
    ALL_PROXY= \
    NO_PROXY=

# mdcx core 依赖（PyQt6 在 core 链中仅当 QtCore/QtGui 层 import，需 GL 基础库）
# 使用清华 Debian 源（默认源在部分网络环境不可达）
RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    printf 'Types: deb\nURIs: https://mirrors.tuna.tsinghua.edu.cn/debian\nSuites: trixie trixie-updates\nComponents: main contrib non-free non-free-firmware\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg\n' > /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl tini ffmpeg \
        libgl1 libegl1 \
        libglib2.0-0 libfontconfig1 libxkbcommon0 libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY mdcx mdcx
COPY resources resources
RUN pip install --no-cache-dir .

COPY mdcx_web mdcx_web
COPY webui/dist webui/dist
RUN pip install --no-cache-dir -r mdcx_web/requirements-web.txt

RUN useradd -m -u 1000 mdcx \
    && mkdir -p /data /media \
    && chown -R mdcx:mdcx /app /data

ENV MDCX_DATA_DIR=/data \
    MDCX_MEDIA_DIR=/media \
    MDCX_WEB_PORT=8000

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/api/system/health >/dev/null || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-m", "uvicorn", "mdcx_web.main:app", "--host", "0.0.0.0", "--port", "8000"]