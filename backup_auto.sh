#!/bin/bash
# /app/backup_auto.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/app/storage/backups"
mkdir -p "$BACKUP_DIR"

# Variables de conexión
DB_USER="nava"
DB_PASS="1234"
DB_HOST="db"
DB_NAME="streaming"

# Backup de la BD
mysqldump -u $DB_USER -p$DB_PASS -h $DB_HOST $DB_NAME > "$BACKUP_DIR/auto_${TIMESTAMP}.sql"

# Mantener solo los últimos 15 backups
ls -t "$BACKUP_DIR"/auto_*.sql | tail -n +15 | xargs rm -f 2>/dev/null

echo "Backup completado: auto_${TIMESTAMP}.sql"
