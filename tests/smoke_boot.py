"""Boot the server in-process, hit critical endpoints, assert 200/expected codes."""
import sys, threading, time, urllib.request, urllib.error, json
from http.server import HTTPServer

sys.path.insert(0, '.')
import server

PORT = 18101
srv = HTTPServer(('127.0.0.1', PORT), server.DashboardHandler)
t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
time.sleep(0.3)

def req(path, method='GET', headers=None, data=None):
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            f'http://127.0.0.1:{PORT}{path}', method=method, headers=headers or {}, data=data),
            timeout=5)
        return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()

failures = []
def check(name, cond, info=''):
    if cond: print(f'  PASS  {name}')
    else: print(f'  FAIL  {name}  {info}'); failures.append(name)

# Tests
s, h, b = req('/healthz'); check('/healthz=200', s == 200)
s, h, b = req('/api/health/detailed'); check('/api/health/detailed=200', s == 200)
check('X-Request-ID header present', 'X-Request-ID' in h or 'x-request-id' in {k.lower() for k in h.keys()})
s, h, b = req('/api/csrf'); check('/api/csrf=200', s == 200)
j = json.loads(b); check('csrf token returned', j.get('ok') and j.get('token'))

# Rate limit (≥1 429 within 25 hits to /login)
codes = []
for _ in range(25):
    s, _, _ = req('/login'); codes.append(s)
check('rate limiter fires', 429 in codes, f'codes={codes[-5:]}')

srv.shutdown()
if failures:
    print(f'\n{len(failures)} FAILURES')
    sys.exit(1)
print('\nAll smoke checks passed')
