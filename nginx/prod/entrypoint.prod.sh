#!/bin/sh

set -x

ls -lh /app/server
cat /app/server/main.py | head -20

uvicorn server.main:app --host 0.0.0.0 --port 8000 &
sleep 2

ps aux

envsubst '${NGINX_BACKEND_HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'
