"""
Round 5 features module — pluggable into server.py via single import + handler hook.
Provides:
  - Multi-user auth (users.json) + role check
  - Audit log (sqlite + JSON file fallback)
  - Analytics aggregator
  - Bulk operations dispatcher
  - Saved views storage
  - Webhook history ring buffer
  - Auto-summary stub (LLM-ready)
  - /metrics Prometheus exposition
  - Graceful shutdown registry
  - Sentry hook
"""
import os, json, time, hmac, hashlib, base64, threading, signal, sys, sqlite3
from collections import deque, Counter
from pathlib import Path

R5_DATA_DIR = Path(os.environ.get('R5_DATA_DIR', '/tmp/dashboard-r5'))
R5_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============ AUTH (multi-user) ============
_USERS_FILE = R5_DATA_DIR / 'users.json'
_USERS_LOCK = threading.RLock()

def _users_load():
    if not _USERS_FILE.exists():
        # seed admin from env
        admin_user = os.environ.get('DASHBOARD_ADMIN_USER', 'admin')
        admin_pass = os.environ.get('DASHBOARD_ADMIN_PASS', 'change-me')
        seed = {admin_user: {'pw_hash': _hash_pw(admin_pass), 'role': 'admin', 'created': time.time()}}
        _USERS_FILE.write_text(json.dumps(seed, indent=2))
        return seed
    try: return json.loads(_USERS_FILE.read_text())
    except Exception: return {}

def _users_save(d):
    tmp = _USERS_FILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(d, indent=2))
    tmp.replace(_USERS_FILE)

def _hash_pw(pw, salt=None):
    if salt is None: salt = base64.b64encode(os.urandom(16)).decode()
    h = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), 60000)
    return f"{salt}${base64.b64encode(h).decode()}"

def _verify_pw(pw, stored):
    try:
        salt, _ = stored.split('$', 1)
        return hmac.compare_digest(_hash_pw(pw, salt), stored)
    except Exception: return False

def auth_check(username, password):
    with _USERS_LOCK:
        u = _users_load().get(username)
        if not u: return None
        if _verify_pw(password, u['pw_hash']):
            return {'user': username, 'role': u.get('role', 'viewer')}
        return None

def auth_add(username, password, role='viewer'):
    with _USERS_LOCK:
        users = _users_load()
        users[username] = {'pw_hash': _hash_pw(password), 'role': role, 'created': time.time()}
        _users_save(users); return True

def auth_list():
    with _USERS_LOCK:
        return [{'user': k, 'role': v.get('role'), 'created': v.get('created')}
                for k, v in _users_load().items()]

def auth_delete(username):
    with _USERS_LOCK:
        users = _users_load()
        if username in users and users[username].get('role') != 'admin' or len([u for u in users.values() if u.get('role')=='admin']) > 1:
            users.pop(username, None); _users_save(users); return True
        return False

ROLE_PERMS = {
    'admin':  {'read', 'write', 'delete', 'admin'},
    'editor': {'read', 'write'},
    'viewer': {'read'},
}
def role_can(role, perm): return perm in ROLE_PERMS.get(role, set())

# ============ AUDIT LOG ============
_AUDIT_DB = R5_DATA_DIR / 'audit.db'
_AUDIT_LOCK = threading.RLock()

def _audit_init():
    with sqlite3.connect(_AUDIT_DB) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts REAL, user TEXT, action TEXT, target TEXT, ip TEXT, meta TEXT)''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_audit_ts ON events(ts)')
_audit_init()

def audit_log(user, action, target='', ip='', meta=None):
    try:
        with _AUDIT_LOCK, sqlite3.connect(_AUDIT_DB) as c:
            c.execute('INSERT INTO events(ts,user,action,target,ip,meta) VALUES(?,?,?,?,?,?)',
                      (time.time(), user or 'anon', action, target, ip, json.dumps(meta or {})))
    except Exception: pass

def audit_query(limit=100, user=None, action=None, since=None):
    q = 'SELECT id,ts,user,action,target,ip,meta FROM events WHERE 1=1'
    args = []
    if user: q += ' AND user=?'; args.append(user)
    if action: q += ' AND action=?'; args.append(action)
    if since: q += ' AND ts>=?'; args.append(since)
    q += ' ORDER BY ts DESC LIMIT ?'; args.append(int(limit))
    with sqlite3.connect(_AUDIT_DB) as c:
        rows = c.execute(q, args).fetchall()
    return [{'id':r[0],'ts':r[1],'user':r[2],'action':r[3],'target':r[4],'ip':r[5],'meta':json.loads(r[6] or '{}')} for r in rows]

# ============ SAVED VIEWS ============
_VIEWS_FILE = R5_DATA_DIR / 'saved_views.json'
_VIEWS_LOCK = threading.RLock()

def views_load():
    if not _VIEWS_FILE.exists(): return {}
    try: return json.loads(_VIEWS_FILE.read_text())
    except Exception: return {}

def views_save_one(user, name, config):
    with _VIEWS_LOCK:
        d = views_load()
        d.setdefault(user, {})[name] = {'config': config, 'updated': time.time()}
        _VIEWS_FILE.write_text(json.dumps(d, indent=2))

def views_delete(user, name):
    with _VIEWS_LOCK:
        d = views_load()
        if user in d and name in d[user]:
            del d[user][name]
            _VIEWS_FILE.write_text(json.dumps(d, indent=2)); return True
        return False

def views_list(user): return views_load().get(user, {})

# ============ WEBHOOK HISTORY ============
_WEBHOOK_BUFFER = deque(maxlen=500)
_WEBHOOK_LOCK = threading.RLock()

def webhook_record(direction, url, status, payload_size, duration_ms, error=None):
    with _WEBHOOK_LOCK:
        _WEBHOOK_BUFFER.append({
            'ts': time.time(), 'direction': direction, 'url': url,
            'status': status, 'payload_size': payload_size,
            'duration_ms': duration_ms, 'error': error,
        })

def webhook_history(limit=100):
    with _WEBHOOK_LOCK:
        return list(_WEBHOOK_BUFFER)[-limit:][::-1]

# ============ ANALYTICS ============
def analytics_compute(kwr_state):
    """Aggregate stats from kwr state dict."""
    runs = list(kwr_state.values()) if isinstance(kwr_state, dict) else []
    total = len(runs)
    by_status = Counter(r.get('status', 'unknown') for r in runs)
    durations = [r.get('duration_seconds') for r in runs if r.get('duration_seconds')]
    avg_dur = sum(durations) / len(durations) if durations else 0
    success = by_status.get('complete', 0) + by_status.get('done', 0)
    success_rate = (success / total * 100) if total else 0

    # Time series last 30 days
    now = time.time(); day = 86400
    buckets = Counter()
    for r in runs:
        ts = r.get('created_at_ts') or r.get('updated_at_ts')
        if not ts: continue
        try: ts = float(ts)
        except Exception: continue
        if now - ts > 30 * day: continue
        bucket = int((now - ts) // day)
        buckets[bucket] += 1
    time_series = [{'days_ago': i, 'count': buckets.get(i, 0)} for i in range(30)]

    # Top errors
    errors = Counter()
    for r in runs:
        err = r.get('error') or r.get('deploy_error')
        if err: errors[str(err)[:80]] += 1
    top_errors = [{'error': e, 'count': c} for e, c in errors.most_common(10)]

    return {
        'total_runs': total,
        'by_status': dict(by_status),
        'success_rate': round(success_rate, 2),
        'avg_duration_seconds': round(avg_dur, 2),
        'time_series_last_30d': time_series,
        'top_errors': top_errors,
        'webhook_calls_recent': len(_WEBHOOK_BUFFER),
    }

# ============ BULK OPS ============
def bulk_dispatch(action, ids, kwr_state, kwr_lock):
    """Apply bulk action to multiple run_ids. Returns (success_ids, failed)."""
    ok, fail = [], {}
    with kwr_lock:
        for rid in ids:
            try:
                if action == 'delete':
                    if rid in kwr_state: del kwr_state[rid]; ok.append(rid)
                    else: fail[rid] = 'not_found'
                elif action == 'tag':
                    if rid in kwr_state:
                        kwr_state[rid].setdefault('tags', []); ok.append(rid)
                    else: fail[rid] = 'not_found'
                elif action == 'archive':
                    if rid in kwr_state: kwr_state[rid]['archived'] = True; ok.append(rid)
                    else: fail[rid] = 'not_found'
                else: fail[rid] = f'unknown_action:{action}'
            except Exception as e: fail[rid] = str(e)
    return ok, fail

# ============ AUTO-SUMMARY (LLM-ready stub) ============
def summarize_run(run_data):
    """Heuristic summary; replace with LLM call when keys configured."""
    status = run_data.get('status', 'unknown')
    stage = run_data.get('current_stage', '?')
    err = run_data.get('error') or run_data.get('deploy_error')
    logs = run_data.get('logs') or []
    dur = run_data.get('duration_seconds', 0)

    parts = [f"Status: {status}", f"Stage: {stage}", f"Duration: {dur:.1f}s"]
    if err: parts.append(f"Error: {err}")
    if logs:
        last_errs = [l for l in logs[-50:] if any(k in l.lower() for k in ('error','fail','exception'))]
        if last_errs: parts.append(f"Recent issues ({len(last_errs)}): {last_errs[-1][:120]}")
        else: parts.append(f"Last log: {logs[-1][:120]}")

    # Recommendation
    rec = ''
    if status in ('error', 'failed'):
        if 'timeout' in str(err or '').lower(): rec = '→ Try increasing timeout or splitting batch'
        elif 'rate' in str(err or '').lower(): rec = '→ Add rate-limit backoff'
        elif 'auth' in str(err or '').lower(): rec = '→ Check API credentials'
        else: rec = '→ Review logs and retry'
    elif status == 'complete': rec = '✓ Run completed successfully'
    if rec: parts.append(rec)

    return {'summary': ' | '.join(parts), 'recommendation': rec}

# ============ /metrics Prometheus ============
_METRICS = {'requests_total': 0, 'requests_by_status': Counter(), 'errors_total': 0}
_METRICS_LOCK = threading.RLock()

def metrics_inc(metric, by=1, label=None):
    with _METRICS_LOCK:
        if label is not None:
            _METRICS.setdefault(metric, Counter())[label] += by
        else:
            _METRICS[metric] = _METRICS.get(metric, 0) + by

def metrics_render():
    lines = ['# HELP dashboard_requests_total Total HTTP requests',
             '# TYPE dashboard_requests_total counter',
             f'dashboard_requests_total {_METRICS.get("requests_total", 0)}',
             '# HELP dashboard_errors_total Total errors',
             '# TYPE dashboard_errors_total counter',
             f'dashboard_errors_total {_METRICS.get("errors_total", 0)}',
             '# HELP dashboard_requests_by_status HTTP requests by status',
             '# TYPE dashboard_requests_by_status counter']
    for code, n in (_METRICS.get('requests_by_status') or {}).items():
        lines.append(f'dashboard_requests_by_status{{status="{code}"}} {n}')
    return '\n'.join(lines) + '\n'

# ============ GRACEFUL SHUTDOWN ============
_SHUTDOWN_HOOKS = []
_SHUTDOWN_FIRED = False

def on_shutdown(fn): _SHUTDOWN_HOOKS.append(fn)

def _handle_signal(signum, frame):
    global _SHUTDOWN_FIRED
    if _SHUTDOWN_FIRED: return
    _SHUTDOWN_FIRED = True
    print(f'[r5] SIGTERM received, running {len(_SHUTDOWN_HOOKS)} shutdown hooks', flush=True)
    for h in _SHUTDOWN_HOOKS:
        try: h()
        except Exception as e: print(f'[r5] shutdown hook error: {e}', flush=True)
    sys.exit(0)

try:
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
except Exception: pass

# ============ SENTRY HOOK ============
def sentry_init():
    dsn = os.environ.get('SENTRY_DSN', '').strip()
    if not dsn: return False
    try:
        import sentry_sdk
        sentry_sdk.init(dsn=dsn, traces_sample_rate=0.1)
        print('[r5] sentry initialized', flush=True)
        return True
    except ImportError:
        print('[r5] SENTRY_DSN set but sentry_sdk not installed', flush=True)
        return False
sentry_init()

print('[r5] features module loaded', flush=True)
