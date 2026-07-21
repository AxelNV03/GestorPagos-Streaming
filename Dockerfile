# Usamos una imagen de Python oficial y ligera
FROM python:3.10-slim

# Instalamos dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    default-mysql-client \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Definimos el directorio donde vivirá el código dentro del contenedor
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar el sistema de capas de Docker (caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de tu proyecto al contenedor
COPY . .

# Dar permisos al script de backup
RUN chmod +x /app/backup_auto.sh

# Configurar cron para backup diario a las 3:00 AM
RUN echo "0 3 * * * /app/backup_auto.sh >> /var/log/backup.log 2>&1" > /etc/cron.d/backup-cron && \
    chmod 0644 /etc/cron.d/backup-cron && \
    crontab /etc/cron.d/backup-cron

# Crear archivo de log
RUN touch /var/log/backup.log

# El puerto por defecto que usa Flask
EXPOSE 5000

# Comando para iniciar: cron + Flask
CMD cron && python run.py