# ── Stage 1 : builder ──────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Installer les dépendances système nécessaires pour psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2 : image finale ─────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Dépendances runtime seulement
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copier les packages installés depuis le builder
COPY --from=builder /install /usr/local

# Créer un utilisateur non-root (sécurité)
RUN useradd --no-create-home --shell /bin/false dituser
USER dituser

# Copier le code source
COPY --chown=dituser:dituser . .

# Port exposé
EXPOSE 8001

# Lancement avec gunicorn (prod) ou runserver (dev via docker-compose)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2"]
