# app/Dockerfile
FROM python:3.10-slim

LABEL maintainer="docente@example.org"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    bash && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no root
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copiar dependencias
COPY --chown=appuser:appuser requirements.txt .

# Instalar pip y dependencias (como root)
RUN pip install --no-cache-dir --upgrade pip --root-user-action=ignore && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install pytest pylint && \
    apt-get purge -y build-essential pkg-config && apt-get autoremove -y

# Copiar código fuente
COPY --chown=appuser:appuser . .

# Permisos
RUN chmod -R 755 /app && chmod +x entrypoint.sh wait_for_db.py

# Cambiar a usuario appuser
USER appuser

# Crear cache pytest con permisos correctos
RUN mkdir -p /app/.pytest_cache && chmod -R 777 /app/.pytest_cache

EXPOSE 5000

CMD ["./entrypoint.sh"]
