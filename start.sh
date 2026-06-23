#!/bin/bash
export PORT="${PORT:-10000}"
envsubst '$PORT' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/app.conf
rm /etc/nginx/conf.d/default.conf
streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &
nginx -g 'daemon off;'
