FROM python:3.11-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# ждём БД, прогоняем миграции, потом стартуем API
CMD /bin/sh -c "python -m app.scripts.wait_for_db && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"