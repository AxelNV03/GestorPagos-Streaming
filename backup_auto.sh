#!/bin/bash
# /app/backup_auto.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/app/storage/backups"
mkdir -p "$BACKUP_DIR"

# Backup de la BD
mysqldump -u $DB_USER -p$DB_PASS -h $DB_HOST $DB_NAME > "$BACKUP_DIR/auto_${TIMESTAMP}.sql"

# Mantener solo los últimos 7 backups
ls -t "$BACKUP_DIR"/auto_*.sql | tail -n +15 | xargs rm -f 2>/dev/null

echo "Backup completado: auto_${TIMESTAMP}.sql"

# Notificar por Telegram
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${TELEGRAM_ADMIN_CHAT_ID}" \
    -d "text=✅ *Backup automático*%0A📁 auto_${TIMESTAMP}.sql" \
    -d "parse_mode=Markdown"