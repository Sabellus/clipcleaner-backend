FROM python:3.11-slim

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/* && pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
RUN uv sync --active --compile-bytecode

COPY . .

CMD /bin/sh -c "python app/scripts/wait_for_db.py && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"