#!/bin/sh
echo "🚀 Khởi động Gost Proxy trên 127.0.0.1:10001 (path=/ws)..."
/usr/local/bin/gost -L "ws://${PROXY_USER}:${PROXY_PASS}@127.0.0.1:10001?path=/ws" &

echo "🌐 Khởi động Nginx Gateway trên Port 10000..."
exec nginx -g "daemon off;"
