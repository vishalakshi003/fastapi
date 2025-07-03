FROM python:3.11-slim

RUN mkdir /app
COPY requirements.txt /app

WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x init-db.sh
 
CMD ["./init-db.sh"]

# CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
