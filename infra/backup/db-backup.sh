#!/usr/bin/env bash
# PostgreSQL point-in-time backup.
set -euo pipefail
DB_HOST="${DB_HOST:-localhost}"
DB_NAME="${DB_NAME:-unicorn}"
DB_USER="${DB_USER:-unicorn}"
BACKUP_DIR="${BACKUP_DIR:-/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"
# Retain last 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete
echo "Backup completed: ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"
