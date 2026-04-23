#!/usr/bin/env bash
# Daily backup trigger — POSTs to running dashboard /api/backup/run
# Install:  crontab -e   then add:   0 3 * * * /home/seoadmin/webs-html-improvements-files/scripts/cron_backup.sh >> /var/log/dashboard-backup.log 2>&1
set -e
PORT="${DASHBOARD_PORT:-8000}"
HOST="${DASHBOARD_HOST:-127.0.0.1}"
echo "[$(date -u +%FT%TZ)] cron-backup start"
curl -fsS -X POST "http://${HOST}:${PORT}/api/backup/run" \
  -H 'Content-Type: application/json' \
  --max-time 60 || echo "backup endpoint failed"
echo "[$(date -u +%FT%TZ)] cron-backup done"
