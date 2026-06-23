#!/bin/bash
PORT="${PORT:-8501}"
streamlit run app.py \
  --server.port "$PORT" \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.enableStaticServing true
