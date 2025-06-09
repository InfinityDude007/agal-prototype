#!/bin/sh

uvicorn server.main:app --host 0.0.0.0 --port 8000 &

envsubst '${NGINX_BACKEND_HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'
