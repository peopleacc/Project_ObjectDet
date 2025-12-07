# ---- Build Stage ----
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---- Final Run Stage ----
FROM python:3.11-slim

WORKDIR /app

# runtime dependency only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

ENV PORT=8000
EXPOSE 8000

# bersihkan cache python
RUN rm -rf /root/.cache

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
