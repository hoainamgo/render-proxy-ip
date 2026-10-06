FROM alpine:3.19

# Cài đặt curl, ca-certificates và tải Gost (Go Simple Tunnel v2.11.5)
RUN apk add --no-cache curl ca-certificates bash \
    && curl -L -o /usr/local/bin/gost.gz https://github.com/ginuerzh/gost/releases/download/v2.11.5/gost-linux-amd64-2.11.5.gz \
    && gzip -d /usr/local/bin/gost.gz \
    && chmod +x /usr/local/bin/gost

WORKDIR /app

ENV PORT=10000
ENV PROXY_USER=ksmart
ENV PROXY_PASS=98427189427194817294817294817294

EXPOSE 10000

# Khởi chạy WebSocket Proxy (chống bị Cloudflare CDN chặn CONNECT và tương thích 100% với Render)
CMD ["sh", "-c", "/usr/local/bin/gost -L ws://${PROXY_USER}:${PROXY_PASS}@:${PORT}"]
