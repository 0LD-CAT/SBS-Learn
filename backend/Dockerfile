FROM python:3.13-slim

WORKDIR /app

COPY backend/config/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY alembic.ini /app/alembic.ini
COPY backend ./backend

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]