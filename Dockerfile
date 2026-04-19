# Этап 1 (Сборка)
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Этап 2 (Финальный образ)
FROM python:3.12-slim

# Устанавливаем Tkinter и зависимости для GUI
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    libx11-6 \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /install /usr/local
COPY database.py models.py main.py ./
COPY .env ./

# Переменная для проброса графики
ENV DISPLAY=host.docker.internal:0

CMD ["python", "main.py"]