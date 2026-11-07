FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    curl \
    pkg-config \
    default-mysql-client \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Permisos de ejecución a los scripts
RUN chmod +x /app/scripts/container/*.sh

# Cron desde archivo versionado
COPY scripts/container/crontab /etc/cron.d/pagos-cron
RUN chmod 0644 /etc/cron.d/pagos-cron && \
    crontab /etc/cron.d/pagos-cron

# Logs
RUN touch /var/log/backup.log /var/log/recordatorio.log /var/log/morosos.log

# Zona horaria
RUN ln -fs /usr/share/zoneinfo/America/Mexico_City /etc/localtime && \
    echo "America/Mexico_City" > /etc/timezone

EXPOSE 5000

CMD cron && python run.py