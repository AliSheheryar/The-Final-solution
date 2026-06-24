#!/bin/bash
export PORT="${PORT:-8080}"
envsubst '$PORT' < /app/nginx.conf.template > /etc/nginx/conf.d/default.conf
streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &
sleep 3
nginx -g 'daemon off;'
