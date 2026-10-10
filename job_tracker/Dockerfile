FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]