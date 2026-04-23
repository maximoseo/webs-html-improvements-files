"""
Round 6 features:
  - Telegram alerts (alert_failure, alert_info)
  - Cloud backup (S3-compatible: B2, R2, AWS S3) using boto3 if available, urllib fallback
  - CSRF hard-enforce switch (env DASH_CSRF=2)
  - AI summary via OpenRouter (replaces heuristic when OPENROUTER_API_KEY set)
"""
import os, json, time, threading, urllib.request, urllib.error, hashlib, hmac, base64
from pathlib import Path

# ============ TELEGRAM ALERTS ============
TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '').strip()
TG_CHAT_ID = os.environ.get('TG_CHAT_ID', '').strip()
TG_ALERTS_ENABLED = bool(TG_BOT_TOKEN and TG_CHAT_ID)
_TG_THROTTLE = {}  # key -> last_sent_ts
_TG_LOCK = threading.RLock()

def tg_send(text, key=None, throttle_seconds=300):
    """Send to Telegram with optional throttling per key."""
    if not TG_ALERTS_ENABLED: return False
    if key:
        with _TG_LOCK:
            last = _TG_THROTTLE.get(key, 0)
            if time.time() - last < throttle_seconds: return False
            _TG_THROTTLE[key] = time.time()
    try:
        url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
        data = json.dumps({'chat_id': TG_CHAT_ID, 'text': text[:4000], 'parse_mode': 'Markdown', 'disable_web_page_preview': True}).encode()
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r: return r.status == 200
    except Exception as e:
        print(f'[r6] telegram send failed: {e}', flush=True); return False

def alert_failure(title, details='', run_id=''):
    txt = f'🚨 *{title}*\n```\n{str(details)[:1500]}\n```'
    if run_id: txt += f'\nRun: `{run_id}`'
    return tg_send(txt, key=f'fail:{title}', throttle_seconds=300)

def alert_info(title, msg=''):
    return tg_send(f'ℹ️ *{title}*\n{msg}', key=f'info:{title}', throttle_seconds=600)

# ============ CLOUD BACKUP (S3-compatible) ============
S3_ENABLED = bool(os.environ.get('S3_BUCKET'))
S3_BUCKET = os.environ.get('S3_BUCKET', '')
S3_ENDPOINT = os.environ.get('S3_ENDPOINT', 'https://s3.us-west-002.backblazeb2.com')
S3_KEY = os.environ.get('S3_KEY', '')
S3_SECRET = os.environ.get('S3_SECRET', '')
S3_REGION = os.environ.get('S3_REGION', 'us-west-002')

def cloud_backup_upload(local_path, key=None):
    """Upload a file to S3-compatible bucket. Returns (ok, url_or_error)."""
    if not S3_ENABLED: return False, 'S3 not configured'
    p = Path(local_path)
    if not p.exists(): return False, f'file not found: {local_path}'
    key = key or f'backups/{int(time.time())}/{p.name}'
    try:
        import boto3
        s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT, aws_access_key_id=S3_KEY,
                          aws_secret_access_key=S3_SECRET, region_name=S3_REGION)
        s3.upload_file(str(p), S3_BUCKET, key)
        return True, f'{S3_ENDPOINT}/{S3_BUCKET}/{key}'
    except ImportError:
        return _s3_upload_sigv4(p, key)
    except Exception as e:
        return False, str(e)

def _s3_upload_sigv4(path, key):
    """Manual SigV4 PUT (fallback when boto3 unavailable)."""
    try:
        body = path.read_bytes()
        host = S3_ENDPOINT.replace('https://','').replace('http://','').rstrip('/')
        amzdate = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
        datestamp = amzdate[:8]
        payload_hash = hashlib.sha256(body).hexdigest()
        canonical_uri = f'/{S3_BUCKET}/{key}'
        canonical_headers = f'host:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amzdate}\n'
        signed_headers = 'host;x-amz-content-sha256;x-amz-date'
        canonical_request = f'PUT\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}'
        cred_scope = f'{datestamp}/{S3_REGION}/s3/aws4_request'
        string_to_sign = f'AWS4-HMAC-SHA256\n{amzdate}\n{cred_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}'
        def sign(k, m): return hmac.new(k, m.encode(), hashlib.sha256).digest()
        kDate = sign(('AWS4'+S3_SECRET).encode(), datestamp)
        kRegion = sign(kDate, S3_REGION); kService = sign(kRegion, 's3'); kSigning = sign(kService, 'aws4_request')
        signature = hmac.new(kSigning, string_to_sign.encode(), hashlib.sha256).hexdigest()
        auth = f'AWS4-HMAC-SHA256 Credential={S3_KEY}/{cred_scope}, SignedHeaders={signed_headers}, Signature={signature}'
        req = urllib.request.Request(f'{S3_ENDPOINT}{canonical_uri}', data=body, method='PUT',
            headers={'Host':host,'x-amz-date':amzdate,'x-amz-content-sha256':payload_hash,'Authorization':auth})
        with urllib.request.urlopen(req, timeout=30) as r:
            return (r.status in (200,201)), f'{S3_ENDPOINT}{canonical_uri}'
    except Exception as e: return False, f'sigv4 error: {e}'

def cloud_backup_all(files):
    """Backup multiple files. Returns dict {file: (ok, info)}."""
    return {f: cloud_backup_upload(f) for f in files}

# ============ AI SUMMARY (OpenRouter) ============
OR_KEY = os.environ.get('OPENROUTER_API_KEY', '').strip()
OR_MODEL = os.environ.get('OPENROUTER_MODEL', 'openai/gpt-4o-mini')

def ai_summarize_run(run_data):
    """LLM summary if OpenRouter available, else None."""
    if not OR_KEY: return None
    logs = run_data.get('logs') or []
    context = {
        'status': run_data.get('status'), 'stage': run_data.get('current_stage'),
        'duration_s': run_data.get('duration_seconds'),
        'error': run_data.get('error') or run_data.get('deploy_error'),
        'last_logs': logs[-30:] if logs else [],
        'config': {k: run_data.get(k) for k in ('domain','language','locale') if run_data.get(k)},
    }
    prompt = (
        "You are an expert SEO/devops analyst. Summarize this run in 3-5 short bullet points "
        "in HEBREW. Be concrete: what happened, why (if failure), and one actionable next step. "
        "Use plain text, no markdown headers.\n\n"
        f"Run data:\n{json.dumps(context, ensure_ascii=False, indent=2)[:4000]}"
    )
    try:
        body = json.dumps({
            'model': OR_MODEL,
            'messages': [{'role':'user','content':prompt}],
            'max_tokens': 400, 'temperature': 0.3,
        }).encode()
        req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
            data=body, headers={'Authorization': f'Bearer {OR_KEY}','Content-Type':'application/json',
                                'HTTP-Referer':'https://webs-html-improvements-files.onrender.com',
                                'X-Title':'Dashboard R6'})
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.loads(r.read())
            text = d['choices'][0]['message']['content']
            return {'summary': text.strip(), 'model': OR_MODEL, 'source': 'openrouter'}
    except Exception as e:
        print(f'[r6] ai_summarize failed: {e}', flush=True); return None

# ============ CSRF HARD MODE ============
CSRF_HARD = os.environ.get('DASH_CSRF') == '2'

print(f'[r6] loaded — telegram={TG_ALERTS_ENABLED} s3={S3_ENABLED} ai={bool(OR_KEY)} csrf_hard={CSRF_HARD}', flush=True)
