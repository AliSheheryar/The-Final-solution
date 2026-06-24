FROM python:3.11-slim

RUN apt-get update && apt-get install -y nginx gettext-base && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .streamlit .streamlit
COPY nginx.conf.template .
COPY start.sh .
RUN chmod +x start.sh
RUN rm -f /etc/nginx/sites-enabled/default

CMD ["./start.sh"]
