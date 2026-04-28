#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# seed-supabase-admin.sh
# One-shot idempotent seed:
#   1) ensure public.dashboard_users table + RLS policies exist
#   2) upsert admin user in Supabase Auth with a given password
#   3) upsert admin row in public.dashboard_users
#
# Reads from .env.local (gitignored). Requires jq or python.
#
# Usage:
#   bash scripts/seed-supabase-admin.sh [new_password]
# If new_password omitted, uses $TEST_ADMIN_PASSWORD.
# ---------------------------------------------------------------------------
set -euo pipefail

if [[ ! -f .env.local ]]; then
  echo ".env.local not found. Copy .env.example and fill it in." >&2
  exit 1
fi
set -a; source .env.local; set +a

: "${SUPABASE_URL:?SUPABASE_URL missing}"
: "${SUPABASE_SERVICE_ROLE_KEY:?SUPABASE_SERVICE_ROLE_KEY missing}"
: "${SUPABASE_MANAGEMENT_TOKEN:?SUPABASE_MANAGEMENT_TOKEN missing}"
: "${SUPABASE_PROJECT_REF:?SUPABASE_PROJECT_REF missing}"

NEW_PASSWORD="${1:-${TEST_ADMIN_PASSWORD:-}}"
ADMIN_EMAIL="${TEST_ADMIN_EMAIL:-service@maximo-seo.com}"
if [[ -z "$NEW_PASSWORD" ]]; then
  echo "Supply a password: bash scripts/seed-supabase-admin.sh 'StrongPassword!'" >&2
  exit 2
fi

jqpy() { python -c "import json,sys; print(json.dumps({'query': sys.argv[1]}))" "$1"; }

echo "==> 1. Ensure dashboard_users table + RLS"
SQL='create table if not exists public.dashboard_users (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  role text not null default '"'"'viewer'"'"' check (role in ('"'"'admin'"'"','"'"'editor'"'"','"'"'viewer'"'"')),
  display_name text, email text,
  last_login timestamptz, created_at timestamptz not null default now()
);
alter table public.dashboard_users enable row level security;
drop policy if exists "self_read" on public.dashboard_users;
create policy "self_read" on public.dashboard_users for select using (auth.uid() = id);
drop policy if exists "service_full" on public.dashboard_users;
create policy "service_full" on public.dashboard_users for all to service_role using (true) with check (true);'
curl -sS -X POST "https://api.supabase.com/v1/projects/$SUPABASE_PROJECT_REF/database/query" \
  -H "Authorization: Bearer $SUPABASE_MANAGEMENT_TOKEN" -H "Content-Type: application/json" \
  -d "$(jqpy "$SQL")" -o /dev/null -w 'SQL status: %{http_code}\n'

echo "==> 2. Upsert admin user in Supabase Auth"
LOOKUP=$(curl -sS "$SUPABASE_URL/auth/v1/admin/users?email=$ADMIN_EMAIL" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY")
USER_ID=$(echo "$LOOKUP" | python -c "import json,sys; d=json.load(sys.stdin); us=d.get('users') if isinstance(d,dict) else d; print((us[0].get('id') if us else '') if isinstance(us,list) else (d.get('id') or ''))")

if [[ -z "$USER_ID" ]]; then
  echo "    creating new user"
  RESP=$(curl -sS -X POST "$SUPABASE_URL/auth/v1/admin/users" \
    -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
    -H "Content-Type: application/json" \
    -d "$(python -c "import json,sys; print(json.dumps({'email':sys.argv[1],'password':sys.argv[2],'email_confirm':True,'user_metadata':{'username':'admin','display_name':'Admin'},'app_metadata':{'role':'admin'}}))" "$ADMIN_EMAIL" "$NEW_PASSWORD")")
  USER_ID=$(echo "$RESP" | python -c "import json,sys; print(json.load(sys.stdin).get('id') or '')")
else
  echo "    updating existing user $USER_ID"
  curl -sS -X PUT "$SUPABASE_URL/auth/v1/admin/users/$USER_ID" \
    -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
    -H "Content-Type: application/json" \
    -d "$(python -c "import json,sys; print(json.dumps({'password':sys.argv[1],'email_confirm':True,'user_metadata':{'username':'admin','display_name':'Admin'},'app_metadata':{'role':'admin'}}))" "$NEW_PASSWORD")" \
    -o /dev/null -w '    status: %{http_code}\n'
fi

echo "==> 3. Upsert dashboard_users row (id=$USER_ID)"
SQL2="insert into public.dashboard_users (id, username, role, display_name, email)
values ('$USER_ID', 'admin', 'admin', 'Admin', '$ADMIN_EMAIL')
on conflict (id) do update set username=excluded.username, role=excluded.role, email=excluded.email;"
curl -sS -X POST "https://api.supabase.com/v1/projects/$SUPABASE_PROJECT_REF/database/query" \
  -H "Authorization: Bearer $SUPABASE_MANAGEMENT_TOKEN" -H "Content-Type: application/json" \
  -d "$(jqpy "$SQL2")" -o /dev/null -w 'Upsert status: %{http_code}\n'

echo "==> 4. Verify login works"
curl -sS -X POST "$SUPABASE_URL/auth/v1/token?grant_type=password" \
  -H "apikey: $SUPABASE_ANON_KEY" -H "Content-Type: application/json" \
  -d "$(python -c "import json,sys; print(json.dumps({'email':sys.argv[1],'password':sys.argv[2]}))" "$ADMIN_EMAIL" "$NEW_PASSWORD")" \
  | python -c "import json,sys; d=json.load(sys.stdin); print('LOGIN:', 'OK' if d.get('access_token') else 'FAIL', d.get('error_description') or d.get('msg') or '')"

echo ""
echo "Done. Update TEST_ADMIN_PASSWORD in .env.local and Render."
