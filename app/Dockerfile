# app/Dockerfile
FROM python:3.10-slim

LABEL maintainer="docente@example.org"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

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

# Crear carpeta del proyecto con permisos adecuados
RUN mkdir -p /app/.pytest_cache && chown -R appuser:appuser /app

WORKDIR /app

# Copiar dependencias primero (aprovecha caché de Docker)
COPY --chown=appuser:appuser requirements.txt .

# Instalar pip y dependencias como root
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest pylint && \
    apt-get purge -y build-essential pkg-config && apt-get autoremove -y

# Copiar el código fuente de la aplicación
COPY --chown=appuser:appuser . .

# Ajustar permisos y scripts ejecutables
RUN chmod -R 755 /app && chmod +x entrypoint.sh wait_for_db.py

# Cambiar a usuario no root
USER appuser

# Exponer el puerto de Flask
EXPOSE 5000

# Ejecutar el contenedor
CMD ["./entrypoint.sh"]
