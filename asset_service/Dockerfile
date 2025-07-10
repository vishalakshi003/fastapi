FROM python:3.11-slim

RUN mkdir /app
COPY asset_service/requirements.txt /app/

COPY asset_service/init-db.sh /app/init-db.sh 

WORKDIR /app

# COPY . /app
COPY asset_service/ ./
COPY shared /app/shared

RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && apt-get clean
 

# Set PYTHONPATH to include shared
ENV PYTHONPATH="${PYTHONPATH}:/app/shared:/app"


RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x init-db.sh
 
CMD ["./init-db.sh"]

# CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
