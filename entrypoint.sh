#!/bin/sh
echo "🚀 Khởi động Gost Proxy trên 127.0.0.1:10001..."
/usr/local/bin/gost -L ws://${PROXY_USER}:${PROXY_PASS}@127.0.0.1:10001 &

echo "🌐 Khởi động Nginx Gateway trên Port 10000 (HTTP 200 OK & WebSocket)..."
exec nginx -g "daemon off;"
