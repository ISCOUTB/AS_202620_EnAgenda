FROM python:3.13-slim

WORKDIR /app

COPY requerimiento.txt .

RUN pip install --no-cache-dir -r requerimiento.txt

COPY . .

<<<<<<< HEAD
ENV PORT=10000

EXPOSE 10000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} app.web:app"]
=======
EXPOSE 10000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:app.web:app"]
>>>>>>> 387b4b3a21341cba9b6635151adf980c027e23be
