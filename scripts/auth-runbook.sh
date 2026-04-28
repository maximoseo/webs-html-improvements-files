#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
AUTH_DOCTOR="$ROOT_DIR/scripts/auth_doctor.py"

if [[ ! -f "$AUTH_DOCTOR" ]]; then
  echo "auth_doctor.py not found at $AUTH_DOCTOR" >&2
  exit 1
fi

MODE="${1:-help}"
shift || true

DEFAULT_PROD_URL="https://html-redesign-dashboard.maximo-seo.ai"
DEFAULT_LOCAL_URL="http://127.0.0.1:${PORT:-8010}"
DEFAULT_USER="${TEST_ADMIN_USER:-admin}"
DEFAULT_EMAIL="${TEST_ADMIN_EMAIL:-service@maximo-seo.com}"
DEFAULT_PASSWORD="${TEST_ADMIN_PASSWORD:-}"
DEFAULT_IP="${AUTH_DOCTOR_FORWARDED_IP:-203.0.113.77}"

run_doctor() {
  python3 "$AUTH_DOCTOR" "$@"
}

check_local_server() {
  local url="$1"
  if ! python3 - <<'PY' "$url"
import sys, urllib.request
url = sys.argv[1].rstrip('/') + '/login'
with urllib.request.urlopen(url, timeout=3) as resp:
    if resp.status < 200 or resp.status >= 500:
        raise SystemExit(1)
PY
  then
    echo "Local dashboard is not reachable at $url" >&2
    echo "Start it first, for example:" >&2
    echo "  PORT=${PORT:-8010} DASHBOARD_USER=admin DASHBOARD_PASSWORD='***' python3 server.py" >&2
    exit 3
  fi
}

require_password() {
  if [[ -z "$DEFAULT_PASSWORD" ]]; then
    echo "TEST_ADMIN_PASSWORD is required for this mode." >&2
    echo "Example: TEST_ADMIN_PASSWORD='***' scripts/auth-runbook.sh full-prod" >&2
    exit 2
  fi
}

case "$MODE" in
  safe-prod)
    run_doctor "$DEFAULT_PROD_URL" "$@"
    ;;
  full-prod)
    require_password
    run_doctor "$DEFAULT_PROD_URL" \
      --user "$DEFAULT_USER" \
      --email "$DEFAULT_EMAIL" \
      --password "$DEFAULT_PASSWORD" \
      --forwarded-ip "$DEFAULT_IP" \
      "$@"
    ;;
  local)
    require_password
    check_local_server "$DEFAULT_LOCAL_URL"
    run_doctor "$DEFAULT_LOCAL_URL" \
      --user "$DEFAULT_USER" \
      --email "$DEFAULT_EMAIL" \
      --password "$DEFAULT_PASSWORD" \
      --forwarded-ip "$DEFAULT_IP" \
      "$@"
    ;;
  custom)
    if [[ $# -lt 1 ]]; then
      echo "Usage: scripts/auth-runbook.sh custom <base_url> [auth_doctor args...]" >&2
      exit 2
    fi
    base_url="$1"
    shift
    if [[ -n "$DEFAULT_PASSWORD" ]]; then
      run_doctor "$base_url" \
        --user "$DEFAULT_USER" \
        --email "$DEFAULT_EMAIL" \
        --password "$DEFAULT_PASSWORD" \
        --forwarded-ip "$DEFAULT_IP" \
        "$@"
    else
      run_doctor "$base_url" "$@"
    fi
    ;;
  help|-h|--help)
    cat <<'EOF'
Usage:
  scripts/auth-runbook.sh safe-prod
  scripts/auth-runbook.sh full-prod
  scripts/auth-runbook.sh local
  scripts/auth-runbook.sh custom <base_url> [auth_doctor args...]

Modes:
  safe-prod  Public checks only against production. No password required.
  full-prod  Full production auth diagnostics. Requires TEST_ADMIN_PASSWORD.
  local      Full local auth diagnostics against http://127.0.0.1:${PORT:-8010}.
  custom     Run against any base URL. If TEST_ADMIN_PASSWORD is set, full checks run.

Environment:
  TEST_ADMIN_USER         default: admin
  TEST_ADMIN_EMAIL        default: service@maximo-seo.com
  TEST_ADMIN_PASSWORD     required for full-prod/local/full custom checks
  AUTH_DOCTOR_FORWARDED_IP default: 203.0.113.77
  PORT                    local mode only, default: 8010
EOF
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    echo "Run scripts/auth-runbook.sh --help" >&2
    exit 2
    ;;
esac
