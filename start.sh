#!/bin/bash
streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false &
nginx -g 'daemon off;'
