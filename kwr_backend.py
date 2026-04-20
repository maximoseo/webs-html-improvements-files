"""
Keyword Research Automation backend.
General-purpose: works for any site - no hardcoded domains.

State machine stages:
  queued -> validating -> analyzing_site -> parsing_sitemap ->
  researching_competitors -> generating_rows -> deduplicating ->
  ready | error | cancelled

Thread safety: all _state mutations go through _lock (RLock).
No imports from server.py - call_llm injected as argument.
"""

import datetime
import io
import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

_state = {}          # run_id -> job dict
_lock = threading.RLock()

# ---------------------------------------------------------------------------
# Public API (called by server.py route handlers)
# ---------------------------------------------------------------------------

def start_run(payload: dict, call_llm) -> tuple:
    """
    Validate payload, create a new run, launch threaded runner.
    Returns (run_id, None) on success or (None, error_str) on validation failure.
    """
    required = ['website_url', 'sitemap_url', 'about_url', 'brand_name',
                'target_language', 'target_market']
    missing = [f for f in required if not (payload.get(f) or '').strip()]
    if missing:
        return None, f"Missing required fields: {', '.join(missing)}"

    # Validate URLs
    for field in ['website_url', 'sitemap_url', 'about_url']:
        val = payload.get(field, '').strip()
        if val and not val.startswith(('http://', 'https://')):
            return None, f"{field} must start with http:// or https://"

    run_id = str(uuid.uuid4())
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    with _lock:
        _state[run_id] = {
            'run_id': run_id,
            'status': 'queued',
            'current_stage': 'queued',
            'finished_stages': [],
            'error_stages': [],
            'progress': 0,
            'logs': [],
            'rows': [],
            'existing_pages': [],
            'row_count': 0,
            'honest_count_note': '',
            'preview_edited': False,
            'created_at': now,
            'updated_at': now,
            'inputs': payload,
            'cancel_requested': False,
            'sheet_url': None,
            'deploy_error': None,
            'deployed_at': None,
        }

    t = threading.Thread(target=_runner, args=(run_id, call_llm), daemon=True)
    t.start()
    return run_id, None


def get_status(run_id: str) -> dict | None:
    with _lock:
        job = _state.get(run_id)
        if job is None:
            return None
        return dict(job)   # shallow copy is fine for JSON serialization


def cancel_run(run_id: str) -> bool:
    with _lock:
        job = _state.get(run_id)
        if job is None:
            return False
        if job['status'] in ('ready', 'complete', 'error', 'cancelled'):
            return False
        job['cancel_requested'] = True
        return True


COLUMNS = ['Existing Parent Page', 'Pillar', 'Cluster', 'Intent', 'Primary Keyword', 'Keywords']


def _worksheet_name(job: dict, sheet_prefix: str) -> str:
    brand = (job.get('inputs') or {}).get('brand_name', 'kwr')
    safe_brand = _slugify(brand)[:30]
    date_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    prefix = _slugify(sheet_prefix)[:20] if sheet_prefix else ''
    return (f"{prefix}-{safe_brand}-{date_str}".strip('-')
            if prefix else f"kwr-{safe_brand}-{date_str}")


def build_excel(run_id: str) -> tuple:
    """
    Build an .xlsx file in memory from the current rows.
    Returns (bytes, worksheet_name, None) or (None, None, error_str).
    """
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        return None, None, "openpyxl not installed - cannot build Excel file"

    with _lock:
        job = _state.get(run_id)
        if job is None:
            return None, None, f"Run {run_id} not found"
        rows = list(job.get('rows') or [])
        ws_name = _worksheet_name(job, '')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = ws_name[:31]  # Excel tab name limit

    # Header style
    header_fill = PatternFill('solid', fgColor='1F3864')
    header_font = Font(bold=True, color='FFFFFF', size=11)
    thin = Side(style='thin', color='CCCCCC')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for col_idx, col_name in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = border

    ws.row_dimensions[1].height = 30

    # Pillar / cluster row styles
    pillar_fill = PatternFill('solid', fgColor='D9E1F2')
    pillar_font = Font(bold=True, size=10)
    cluster_font = Font(size=10)
    cluster_fill = PatternFill('solid', fgColor='FFFFFF')

    for r_idx, row in enumerate(rows, 2):
        is_pillar = (str(row.get('col_a', '')).strip() == '-' or
                     not str(row.get('col_a', '')).strip())
        fill = pillar_fill if is_pillar else cluster_fill
        font = pillar_font if is_pillar else cluster_font

        values = [
            row.get('col_a', ''),
            row.get('col_b', ''),
            row.get('col_c', ''),
            row.get('col_d', ''),
            row.get('col_e', ''),
            row.get('col_f', ''),
        ]
        for c_idx, val in enumerate(values, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.fill = fill
            cell.font = font
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = border

    # Column widths
    col_widths = [30, 25, 30, 15, 35, 50]
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.freeze_panes = 'A2'

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue(), ws_name, None


def approve_and_save(run_id: str, edited_rows: list, sheet_prefix: str) -> tuple:
    """
    Mark run as approved, save edited rows, build Excel bytes.
    Returns (excel_bytes, worksheet_name, None) or (None, None, error_str).
    Does NOT write anywhere externally — caller decides where to save.
    """
    with _lock:
        job = _state.get(run_id)
        if job is None:
            return None, None, f"Run {run_id} not found"
        if job['status'] not in ('ready', 'complete'):
            return None, None, f"Run is in state '{job['status']}' — can only approve 'ready' runs"
        if not edited_rows:
            return None, None, "No rows to save"
        job['rows'] = edited_rows
        job['row_count'] = len(edited_rows)

    excel_bytes, ws_name, err = build_excel(run_id)
    if err:
        return None, None, err

    deployed_at = datetime.datetime.utcnow().isoformat() + 'Z'
    with _lock:
        _state[run_id]['status'] = 'complete'
        _state[run_id]['deployed_at'] = deployed_at
        _state[run_id]['worksheet_name'] = ws_name
        _state[run_id]['deploy_error'] = None

    return excel_bytes, ws_name, None


def push_to_sheets(run_id: str, sheet_target: str) -> tuple:
    """
    Push approved rows to Google Sheets using gspread + service account.
    Requires GOOGLE_SERVICE_ACCOUNT_JSON env var (JSON string of the SA key).
    Returns (sheet_url, None) or (None, error_str).
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        return None, "gspread / google-auth not installed"

    sa_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', '').strip()
    if not sa_json:
        return None, "GOOGLE_SERVICE_ACCOUNT_JSON env var not set"

    with _lock:
        job = _state.get(run_id)
        if job is None:
            return None, f"Run {run_id} not found"
        rows = list(job.get('rows') or [])
        ws_name = job.get('worksheet_name') or _worksheet_name(job, '')

    if not rows:
        return None, "No rows to push — approve first"
    if not sheet_target or not sheet_target.strip():
        return None, "sheet_target (Google Sheet URL or ID) is required"

    try:
        sa_info = json.loads(sa_json)
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]
        creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
        gc = gspread.authorize(creds)

        # Open by URL or ID
        if 'docs.google.com' in sheet_target:
            sh = gc.open_by_url(sheet_target)
        else:
            sh = gc.open_by_key(sheet_target)

        # Always create a NEW worksheet — never overwrite
        try:
            ws = sh.add_worksheet(title=ws_name, rows=len(rows) + 5, cols=6)
        except Exception:
            # If name collision, append timestamp
            ws_name = ws_name + '-' + datetime.datetime.utcnow().strftime('%H%M%S')
            ws = sh.add_worksheet(title=ws_name, rows=len(rows) + 5, cols=6)

        # Write header + rows
        data = [COLUMNS]
        for row in rows:
            data.append([
                row.get('col_a', ''),
                row.get('col_b', ''),
                row.get('col_c', ''),
                row.get('col_d', ''),
                row.get('col_e', ''),
                row.get('col_f', ''),
            ])
        ws.update(data, value_input_option='RAW')

        # Bold header
        ws.format('A1:F1', {'textFormat': {'bold': True},
                             'backgroundColor': {'red': 0.12, 'green': 0.22, 'blue': 0.39}})

        sheet_url = sh.url
        with _lock:
            _state[run_id]['sheet_url'] = sheet_url
            _state[run_id]['worksheet_name'] = ws_name

        return sheet_url, None

    except json.JSONDecodeError:
        return None, "GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON"
    except Exception as exc:
        return None, str(exc)[:500]


def save_to_obsidian(run_id: str) -> tuple:
    """
    Save the keyword research result as a Markdown note to Obsidian via local REST API.
    Returns (note_path, None) or (None, error_str).
    """
    obsidian_url = os.getenv('OBSIDIAN_LOCAL_HTTP_URL', 'http://127.0.0.1:27123').rstrip('/')
    obsidian_key = os.getenv('OBSIDIAN_LOCAL_API_KEY', '').strip()
    if not obsidian_key:
        return None, "OBSIDIAN_LOCAL_API_KEY env var not set"

    with _lock:
        job = _state.get(run_id)
        if job is None:
            return None, f"Run {run_id} not found"
        rows = list(job.get('rows') or [])
        inputs = job.get('inputs') or {}
        ws_name = job.get('worksheet_name', run_id)
        created_at = job.get('created_at', '')

    brand = inputs.get('brand_name', 'unknown')
    website = inputs.get('website_url', '')
    market = inputs.get('target_market', '')
    language = inputs.get('target_language', '')

    # Build markdown table
    lines = [
        f"# KWR: {brand}",
        f"",
        f"- **Site:** {website}",
        f"- **Market:** {market}",
        f"- **Language:** {language}",
        f"- **Run date:** {created_at[:10] if created_at else 'unknown'}",
        f"- **Rows:** {len(rows)}",
        f"- **Worksheet:** {ws_name}",
        f"",
        f"| Existing Parent Page | Pillar | Cluster | Intent | Primary Keyword | Keywords |",
        f"|---|---|---|---|---|---|",
    ]
    for row in rows:
        def esc(v):
            return str(v or '').replace('|', '\\|')
        lines.append(
            f"| {esc(row.get('col_a',''))} "
            f"| {esc(row.get('col_b',''))} "
            f"| {esc(row.get('col_c',''))} "
            f"| {esc(row.get('col_d',''))} "
            f"| {esc(row.get('col_e',''))} "
            f"| {esc(row.get('col_f',''))} |"
        )

    note_content = '\n'.join(lines)
    note_path = f"html-redesign-dashboard/kwr-results/{ws_name}.md"
    url = f"{obsidian_url}/vault/{urllib.parse.quote(note_path)}"

    try:
        body = note_content.encode('utf-8')
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                'Authorization': f'Bearer {obsidian_key}',
                'Content-Type': 'text/markdown',
            },
            method='PUT'
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp.read()
        return note_path, None
    except urllib.error.HTTPError as exc:
        return None, f"Obsidian API error {exc.code}: {exc.read().decode('utf-8','replace')[:200]}"
    except Exception as exc:
        return None, str(exc)[:300]


def update_rows(run_id: str, rows: list) -> bool:
    """Allow user to save edits to the preview without deploying."""
    with _lock:
        job = _state.get(run_id)
        if job is None:
            return False
        job['rows'] = rows
        job['preview_edited'] = True
        job['row_count'] = len(rows)
        return True


def list_recent(limit: int = 10) -> list:
    with _lock:
        jobs = sorted(_state.values(), key=lambda j: j.get('created_at', ''), reverse=True)
        return [_job_summary(j) for j in jobs[:limit]]


# ---------------------------------------------------------------------------
# Internal runner
# ---------------------------------------------------------------------------

class _Cancelled(Exception):
    pass


def _runner(run_id: str, call_llm):
    def log(msg: str):
        ts = datetime.datetime.utcnow().strftime('%H:%M:%S')
        with _lock:
            _state[run_id]['logs'].append(f"[{ts}] {msg}")
            _state[run_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

    def set_stage(stage: str, progress: int):
        with _lock:
            prev = _state[run_id]['current_stage']
            if prev and prev != stage and prev not in _state[run_id]['finished_stages']:
                _state[run_id]['finished_stages'].append(prev)
            _state[run_id]['current_stage'] = stage
            _state[run_id]['progress'] = progress
            _state[run_id]['status'] = 'running'
            _state[run_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

    def check_cancel():
        with _lock:
            if _state[run_id].get('cancel_requested'):
                raise _Cancelled()

    def fail(stage: str, error: str):
        with _lock:
            _state[run_id]['status'] = 'error'
            _state[run_id]['current_stage'] = stage
            _state[run_id]['error_stages'].append(stage)
            _state[run_id]['logs'].append(f"[ERROR] {error}")
            _state[run_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

    try:
        with _lock:
            inputs = dict(_state[run_id]['inputs'])

        website_url   = inputs['website_url'].rstrip('/')
        sitemap_url   = inputs['sitemap_url']
        about_url     = inputs['about_url']
        brand_name    = inputs['brand_name']
        target_lang   = inputs['target_language']
        target_market = inputs['target_market']
        sheet_target  = inputs.get('spreadsheet_target', '')
        competitor_urls = [u.strip() for u in (inputs.get('competitor_urls') or '').split('\n') if u.strip()]
        exclusions    = inputs.get('notes_exclusions', '')

        # ── Stage 1: validating ─────────────────────────────────────────────
        set_stage('validating', 5)
        check_cancel()
        log(f"Validating inputs for {website_url}")

        # Quick HEAD check on website_url
        try:
            req = urllib.request.Request(website_url, method='HEAD', headers={'User-Agent': 'KWR-Bot/1.0'})
            urllib.request.urlopen(req, timeout=10)
            log(f"Site reachable: {website_url}")
        except Exception as e:
            log(f"Warning: site HEAD check failed ({e}) - continuing anyway")

        # ── Stage 2: analyzing_site ─────────────────────────────────────────
        set_stage('analyzing_site', 15)
        check_cancel()
        log("Fetching home page and about page...")

        home_text = _fetch_page_text(website_url)
        about_text = _fetch_page_text(about_url)
        log(f"Home page: {len(home_text)} chars, About page: {len(about_text)} chars")

        # Summarize site with LLM
        check_cancel()
        site_summary_prompt = f"""Analyze this website for keyword research purposes.
Brand: {brand_name}
Target Language: {target_lang}
Target Market: {target_market}
Home page content (truncated):
{home_text[:3000]}

About page content (truncated):
{about_text[:3000]}

Return a JSON object with:
- "services": array of strings (actual services/products offered)
- "topics": array of strings (main topic areas)
- "tone": string (brand tone)
- "description": string (1-2 sentence site description)
Only include real services/products visible in the content. Do not invent offerings."""

        site_msgs = [
            {'role': 'system', 'content': 'You are an SEO analyst. Return only valid JSON.'},
            {'role': 'user', 'content': site_summary_prompt}
        ]
        site_summary_raw, _ = call_llm(site_msgs, 'anthropic/claude-opus-4')
        try:
            site_summary = json.loads(_extract_json(site_summary_raw))
        except Exception:
            site_summary = {'services': [], 'topics': [], 'tone': 'professional', 'description': site_summary_raw[:200]}
        log(f"Site analysis done. Services: {site_summary.get('services', [])[:3]}")

        # ── Stage 3: parsing_sitemap ─────────────────────────────────────────
        set_stage('parsing_sitemap', 30)
        check_cancel()
        log(f"Parsing sitemap: {sitemap_url}")

        existing_pages = _parse_sitemap(sitemap_url)
        log(f"Found {len(existing_pages)} existing pages in sitemap")
        with _lock:
            _state[run_id]['existing_pages'] = existing_pages[:200]  # cap for UI

        # ─�� Stage 4: researching_competitors ────────────────────────────────
        set_stage('researching_competitors', 45)
        check_cancel()
        log("Researching competitor topics...")

        comp_topics = []
        if competitor_urls:
            for cu in competitor_urls[:3]:
                check_cancel()
                comp_text = _fetch_page_text(cu)
                log(f"Fetched competitor: {cu} ({len(comp_text)} chars)")
                comp_topics.append({'url': cu, 'text': comp_text[:2000]})

        # ── Stage 5: generating_rows ─────────────────────────────────────────
        set_stage('generating_rows', 60)
        check_cancel()
        log("Generating keyword research rows with LLM...")

        existing_paths = '\n'.join(existing_pages[:100]) if existing_pages else '(none found)'
        comp_context = '\n'.join([f"Competitor {i+1} ({c['url']}): {c['text'][:500]}" for i,c in enumerate(comp_topics)]) if comp_topics else '(none provided)'
        exclusion_note = f"Exclusions: {exclusions}" if exclusions else ''

        kwr_prompt = f"""Generate a comprehensive keyword research plan for:
Brand: {brand_name}
Website: {website_url}
Target Language: {target_lang}
Target Market: {target_market}
Services/Products: {json.dumps(site_summary.get('services', []))}
Main Topics: {json.dumps(site_summary.get('topics', []))}
{exclusion_note}

Existing pages (do NOT duplicate these):
{existing_paths}

Competitor context:
{comp_context}

Rules:
- Output ONLY a JSON array of row objects
- Each row has exactly these keys: existing_parent_page, pillar, cluster, intent, primary_keyword, keywords
- pillar rows: existing_parent_page="-", cluster=pillar value, intent="pillar"
- cluster rows: existing_parent_page=slug of parent pillar page, intent=one of (informational|navigational|transactional|commercial)
- Do NOT duplicate existing pages, do NOT create cannibalization between rows
- Do NOT invent services not found on the site
- Do NOT mix languages except where brand/URL requires it
- Target 200-250 total rows (pillar + cluster combined)
- primary_keyword must be unique across all rows
- keywords = comma-separated list of 3-5 related keywords
- Use language: {target_lang}
- Market context: {target_market}

Return only the JSON array, no explanation."""

        kwr_msgs = [
            {'role': 'system', 'content': 'You are an expert SEO strategist. Return only valid JSON arrays.'},
            {'role': 'user', 'content': kwr_prompt}
        ]
        kwr_raw, provider = call_llm(kwr_msgs, 'anthropic/claude-opus-4')
        log(f"LLM response received via {provider} ({len(kwr_raw)} chars)")

        # ── Stage 6: deduplicating ────────────────────────────────────────────
        set_stage('deduplicating', 80)
        check_cancel()
        log("Parsing and deduplicating rows...")

        try:
            raw_rows = json.loads(_extract_json(kwr_raw))
            if not isinstance(raw_rows, list):
                raise ValueError("LLM did not return an array")
        except Exception as e:
            fail('deduplicating', f"Failed to parse LLM output as JSON: {e}\nRaw (first 500): {kwr_raw[:500]}")
            return

        # Normalize + deduplicate
        seen_kw = set()
        seen_pages = set(p.lower() for p in existing_pages)
        clean_rows = []
        for row in raw_rows:
            check_cancel()
            pk = (row.get('primary_keyword') or '').strip().lower()
            if not pk:
                continue
            if pk in seen_kw:
                continue
            seen_kw.add(pk)
            clean_rows.append({
                'existing_parent_page': (row.get('existing_parent_page') or '-').strip(),
                'pillar':               (row.get('pillar') or '').strip(),
                'cluster':              (row.get('cluster') or '').strip(),
                'intent':               (row.get('intent') or 'informational').strip(),
                'primary_keyword':      (row.get('primary_keyword') or '').strip(),
                'keywords':             (row.get('keywords') or '').strip(),
            })

        log(f"After deduplication: {len(clean_rows)} rows (from {len(raw_rows)} raw)")

        honest_note = ''
        if len(clean_rows) < 200:
            honest_note = (
                f"Produced {len(clean_rows)} valid net-new rows. "
                f"The site's existing coverage and deduplication constraints "
                f"did not support expansion to 200 rows without adding irrelevant filler."
            )
            log(f"Note: {honest_note}")

        with _lock:
            _state[run_id]['rows'] = clean_rows
            _state[run_id]['row_count'] = len(clean_rows)
            _state[run_id]['honest_count_note'] = honest_note
            _state[run_id]['status'] = 'ready'
            _state[run_id]['current_stage'] = 'ready'
            _state[run_id]['progress'] = 100
            _state[run_id]['finished_stages'].append('deduplicating')
            _state[run_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'

        log(f"Pipeline complete. {len(clean_rows)} rows ready for review.")

    except _Cancelled:
        with _lock:
            _state[run_id]['status'] = 'cancelled'
            _state[run_id]['current_stage'] = 'cancelled'
            _state[run_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        _log_safe(run_id, "Run cancelled by user.")

    except Exception as exc:
        import traceback
        tb = traceback.format_exc()
        with _lock:
            stage = _state[run_id].get('current_stage', 'unknown')
            _state[run_id]['status'] = 'error'
            _state[run_id]['error_stages'].append(stage)
            _state[run_id]['logs'].append(f"[ERROR] Unexpected: {exc}")
            _state[run_id]['logs'].append(tb[-800:])
            _state[run_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _log_safe(run_id, msg):
    ts = datetime.datetime.utcnow().strftime('%H:%M:%S')
    with _lock:
        if run_id in _state:
            _state[run_id]['logs'].append(f"[{ts}] {msg}")


def _fetch_page_text(url: str, timeout: int = 15) -> str:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'KWR-Bot/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode('utf-8', 'replace')
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:8000]
    except Exception as e:
        return f"(fetch failed: {e})"


def _parse_sitemap(sitemap_url: str) -> list:
    try:
        req = urllib.request.Request(sitemap_url, headers={'User-Agent': 'KWR-Bot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode('utf-8', 'replace')
        # Handle sitemap index (links to sub-sitemaps)
        sub_maps = re.findall(r'<loc>\s*(https?://[^\s<]+sitemap[^\s<]*)\s*</loc>', raw, re.IGNORECASE)
        urls = re.findall(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', raw, re.IGNORECASE)
        # If only sub-maps found, fetch first few
        if sub_maps and len(urls) <= len(sub_maps):
            all_urls = []
            for sm in sub_maps[:3]:
                try:
                    req2 = urllib.request.Request(sm, headers={'User-Agent': 'KWR-Bot/1.0'})
                    with urllib.request.urlopen(req2, timeout=10) as r2:
                        sub_raw = r2.read().decode('utf-8', 'replace')
                    all_urls += re.findall(r'<loc>\s*(https?://[^\s<]+)\s*</loc>', sub_raw, re.IGNORECASE)
                except Exception:
                    pass
            return all_urls[:300]
        return [u for u in urls if 'sitemap' not in u.lower()][:300]
    except Exception:
        return []


def _extract_json(text: str) -> str:
    """Extract JSON from LLM output that may contain prose or fenced blocks."""
    # Try fenced block first
    m = re.search(r'```(?:json)?\s*([\[\{].*?)\s*```', text, re.DOTALL)
    if m:
        return m.group(1)
    # Try first [ ... ] or { ... }
    m = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
    if m:
        return m.group(1)
    return text


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


def _job_summary(job: dict) -> dict:
    return {
        'run_id':       job.get('run_id'),
        'status':       job.get('status'),
        'current_stage': job.get('current_stage'),
        'progress':     job.get('progress', 0),
        'row_count':    job.get('row_count', 0),
        'created_at':   job.get('created_at'),
        'updated_at':   job.get('updated_at'),
        'website_url':  (job.get('inputs') or {}).get('website_url', ''),
        'brand_name':   (job.get('inputs') or {}).get('brand_name', ''),
        'sheet_url':    job.get('sheet_url'),
        'deploy_error': job.get('deploy_error'),
        'honest_count_note': job.get('honest_count_note', ''),
    }
