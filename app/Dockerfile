# app/Dockerfile
FROM python:3.10-slim

LABEL maintainer="docente@example.org"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Instalar dependencias del sistema necesarias para compilar y conectar con MySQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    bash && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario no root
RUN useradd --create-home --shell /bin/bash appuser

# Crear carpeta del proyecto y asignar permisos
RUN mkdir -p /app && chown -R appuser:appuser /app

# Definir directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (para aprovechar la caché de Docker)
COPY --chown=appuser:appuser requirements.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest pylint && \
    apt-get purge -y build-essential pkg-config && apt-get autoremove -y && \
    rm -rf /root/.cache/pip

# Copiar el código fuente
COPY --chown=appuser:appuser . .

# Ajustar ownership y permisos (evita el error "Operation not permitted")
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod +x entrypoint.sh wait_for_db.py

# Cambiar al usuario no root
USER appuser

# Exponer el puerto Flask
EXPOSE 5000

# Comando de inicio del contenedor
CMD ["./entrypoint.sh"]
