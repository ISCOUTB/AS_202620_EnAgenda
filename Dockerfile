FROM python:3.13-slim

WORKDIR /app

COPY requerimiento.txt .

RUN pip install --no-cache-dir -r requerimiento.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:app.web:app"]
