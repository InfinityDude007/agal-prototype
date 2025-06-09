#!/bin/sh

envsubst '${NGINX_BACKEND_HOST} ${NGINX_FRONTEND_HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'
