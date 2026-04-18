#!/usr/bin/env python3
import base64
import concurrent.futures
import json
import mimetypes
import os
import posixpath
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'index.html'
DATA = ROOT / 'data.json'
MAP_FILE = ROOT / 'n8n-workflow-map.json'
REPO = 'maximoseo/webs-html-improvements-files'
RAW_BASE = f'https://raw.githubusercontent.com/{REPO}/main'
DEFAULT_N8N_BASE = 'https://websiseo.app.n8n.cloud'


def load_json_file(path: Path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def text_response(handler, status, body: bytes, content_type: str):
    handler.send_response(status)
    handler.send_header('Content-Type', content_type)
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_request_json(handler):
    length = int(handler.headers.get('Content-Length', '0') or '0')
    raw = handler.rfile.read(length) if length else b'{}'
    if not raw:
        return {}
    return json.loads(raw.decode('utf-8'))


def fetch_json(url, headers=None, method='GET', body=None, timeout=60):
    req = urllib.request.Request(url, headers=headers or {}, method=method)
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    else:
        data = None
    with urllib.request.urlopen(req, data=data, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


def fetch_text(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers=headers or {}, method='GET')
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8')


def n8n_headers():
    key = os.getenv('N8N_API_KEY')
    if not key:
        return None
    return {'X-N8N-API-KEY': key, 'Accept': 'application/json'}


def prompt_headers():
    key = os.getenv('OPENAI_API_KEY') or os.getenv('OPENROUTER_API_KEY')
    if not key:
        return None, None
    base = os.getenv('OPENAI_BASE_URL') or ('https://openrouter.ai/api/v1' if os.getenv('OPENROUTER_API_KEY') and not os.getenv('OPENAI_API_KEY') else 'https://api.openai.com/v1')
    headers = {'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
    if 'openrouter.ai' in base:
        headers['HTTP-Referer'] = os.getenv('OPENROUTER_SITE_URL', 'https://html-redesign-dashboard.maximo-seo.ai/')
        headers['X-Title'] = os.getenv('OPENROUTER_APP_NAME', 'HTML Redesign Dashboard')
    return base.rstrip('/'), headers



def supabase_comments_config():
    url = (os.getenv('SUPABASE_URL') or '').strip().rstrip('/')
    key = (
        (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or '').strip()
        or (os.getenv('SUPABASE_ANON_KEY') or '').strip()
        or (os.getenv('SUPABASE_API_KEY') or '').strip()
    )
    table = (os.getenv('SUPABASE_COMMENTS_TABLE') or 'dashboard_comments').strip() or 'dashboard_comments'
    schema = (os.getenv('SUPABASE_SCHEMA') or 'public').strip() or 'public'
    return {'url': url, 'key': key, 'table': table, 'schema': schema, 'configured': bool(url and key and table)}


def supabase_comments_headers(prefer=None):
    cfg = supabase_comments_config()
    if not cfg['configured']:
        return None
    headers = {
        'apikey': cfg['key'],
        'Authorization': f"Bearer {cfg['key']}",
        'Accept': 'application/json',
        'Accept-Profile': cfg['schema'],
        'Content-Profile': cfg['schema'],
    }
    if prefer:
        headers['Prefer'] = prefer
    return headers


def serialize_comment_row(row):
    return {
        'id': row.get('id'),
        'createdAt': row.get('created_at'),
        'domain': row.get('domain') or '',
        'agentName': row.get('agent_name') or '',
        'versionName': row.get('version_name') or '',
        'contextType': row.get('context_type') or '',
        'contextKey': row.get('context_key') or '',
        'filePath': row.get('file_path') or '',
        'commentText': row.get('comment_text') or '',
        'authorName': row.get('author_name') or '',
        'metadata': row.get('metadata') or {},
    }


def list_supabase_comments(filters):
    cfg = supabase_comments_config()
    if not cfg['configured']:
        return {'ok': True, 'configured': False, 'table': cfg['table'], 'comments': []}
    context_key = (filters.get('contextKey') or '').strip()
    domain = normalize_domain(filters.get('domain') or '')
    agent_name = (filters.get('agentName') or '').strip()
    version_name = (filters.get('versionName') or '').strip()
    context_type = (filters.get('contextType') or '').strip()
    file_path = (filters.get('filePath') or '').strip()
    try:
        limit = int(filters.get('limit') or 50)
    except Exception:
        limit = 50
    limit = max(1, min(limit, 100))
    if not context_key and not any([domain, agent_name, version_name, context_type, file_path]):
        raise ValueError('contextKey or at least one context filter is required')
    query = [
        'select=' + urllib.parse.quote('id,created_at,domain,agent_name,version_name,context_type,context_key,file_path,comment_text,author_name,metadata', safe=',_'),
        'order=' + urllib.parse.quote('created_at.desc', safe='._'),
        f'limit={limit}',
    ]
    if context_key:
        query.append('context_key=eq.' + urllib.parse.quote(context_key, safe=''))
    if domain:
        query.append('domain=eq.' + urllib.parse.quote(domain, safe=''))
    if agent_name:
        query.append('agent_name=eq.' + urllib.parse.quote(agent_name, safe=''))
    if version_name:
        query.append('version_name=eq.' + urllib.parse.quote(version_name, safe=''))
    if context_type:
        query.append('context_type=eq.' + urllib.parse.quote(context_type, safe=''))
    if file_path:
        query.append('file_path=eq.' + urllib.parse.quote(file_path, safe=''))
    url = f"{cfg['url']}/rest/v1/{urllib.parse.quote(cfg['table'], safe='')}?{'&'.join(query)}"
    rows = fetch_json(url, headers=supabase_comments_headers(), timeout=30)
    rows = rows if isinstance(rows, list) else []
    return {'ok': True, 'configured': True, 'table': cfg['table'], 'comments': [serialize_comment_row(r) for r in rows]}


def save_supabase_comment(payload):
    cfg = supabase_comments_config()
    if not cfg['configured']:
        raise RuntimeError('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY/SUPABASE_ANON_KEY are not configured')
    comment_text = (payload.get('commentText') or payload.get('comment') or '').strip()
    if not comment_text:
        raise ValueError('commentText is required')
    if len(comment_text) > 5000:
        raise ValueError('commentText is too long (max 5000 chars)')
    domain = normalize_domain(payload.get('domain') or '')
    agent_name = (payload.get('agentName') or '').strip()
    version_name = (payload.get('versionName') or '').strip()
    context_type = (payload.get('contextType') or 'general').strip() or 'general'
    file_path = (payload.get('filePath') or '').strip()
    context_key = (payload.get('contextKey') or '').strip() or '::'.join([context_type, domain, agent_name, version_name, file_path])
    author_name = (payload.get('authorName') or '').strip()
    metadata = payload.get('metadata') if isinstance(payload.get('metadata'), dict) else {}
    row = {
        'domain': domain,
        'agent_name': agent_name,
        'version_name': version_name,
        'context_type': context_type,
        'context_key': context_key,
        'file_path': file_path,
        'comment_text': comment_text,
        'author_name': author_name or None,
        'metadata': metadata,
    }
    url = f"{cfg['url']}/rest/v1/{urllib.parse.quote(cfg['table'], safe='')}"
    result = fetch_json(url, headers=supabase_comments_headers('return=representation'), method='POST', body=row, timeout=30)
    saved = result[0] if isinstance(result, list) and result else row
    return {'ok': True, 'configured': True, 'table': cfg['table'], 'comment': serialize_comment_row(saved)}


def normalize_domain(value: str) -> str:
    value = (value or '').strip().lower()
    if not value:
        return ''
    value = value.replace('https://', '').replace('http://', '')
    if value.startswith('www.'):
        value = value[4:]
    return value.strip('/ ')


def workflow_matches_domain(workflow, domain: str) -> bool:
    target = normalize_domain(domain)
    tokens = [workflow.get('name', '')]
    tokens.extend(tag.get('name', '') for tag in workflow.get('tags', []) if isinstance(tag, dict))
    for token in tokens:
        normalized = normalize_domain(token)
        if normalized == target or target in normalized or normalized in target:
            return True
    return False


def list_live_workflows():
    headers = n8n_headers()
    if not headers:
        raise RuntimeError('N8N_API_KEY is not configured')
    base = os.getenv('N8N_BASE_URL', DEFAULT_N8N_BASE).rstrip('/')
    data = fetch_json(f'{base}/api/v1/workflows', headers=headers)
    return base, data.get('data', [])


def resolve_workflow_id(domain: str, explicit_id=None):
    domain = normalize_domain(domain)
    if explicit_id:
        return explicit_id, {'strategy': 'explicit'}

    mapping = load_json_file(MAP_FILE, {'domains': {}})
    mapped = (mapping.get('domains') or {}).get(domain)
    if isinstance(mapped, dict) and mapped.get('workflowId'):
        return mapped['workflowId'], {'strategy': 'map', 'mapping': mapped}
    if isinstance(mapped, str) and mapped:
        return mapped, {'strategy': 'map'}

    base, workflows = list_live_workflows()
    matches = []
    for workflow in workflows:
        if workflow_matches_domain(workflow, domain):
            matches.append({
                'id': workflow.get('id'),
                'name': workflow.get('name'),
                'active': workflow.get('active'),
                'tags': [tag.get('name') for tag in workflow.get('tags', []) if isinstance(tag, dict)],
            })
    if len(matches) == 1:
        return matches[0]['id'], {'strategy': 'auto', 'candidates': matches, 'base': base}
    if len(matches) > 1:
        raise ValueError(json.dumps({'code': 'ambiguous_workflow_match', 'candidates': matches}, ensure_ascii=False))
    raise LookupError(json.dumps({'code': 'workflow_not_found', 'domain': domain, 'candidates': []}, ensure_ascii=False))


def build_workflow_payload(source, live):
    payload = {
        'name': source.get('name') or live.get('name'),
        'nodes': source.get('nodes') or live.get('nodes') or [],
        'connections': source.get('connections') or live.get('connections') or {},
        'settings': source.get('settings') if 'settings' in source else live.get('settings') or {},
        'staticData': source.get('staticData') if 'staticData' in source else live.get('staticData'),
        'pinData': source.get('pinData') if 'pinData' in source else live.get('pinData') or {},
    }
    if 'meta' in source or live.get('meta') is not None:
        payload['meta'] = source.get('meta') if 'meta' in source else live.get('meta')
    if 'tags' in source:
        payload['tags'] = source.get('tags')
    elif live.get('tags'):
        payload['tags'] = live.get('tags')
    if 'active' in source or live.get('active') is not None:
        payload['active'] = source.get('active') if 'active' in source else live.get('active')
    if live.get('versionId'):
        payload['versionId'] = live.get('versionId')
    return payload


def _normalize_checklist(raw):
    """Accept list[str] or list[{label: str}] from the client. Return clean list[str]."""
    if not raw:
        return []
    out = []
    if isinstance(raw, list):
        for entry in raw:
            if entry is None:
                continue
            if isinstance(entry, str):
                s = entry.strip()
            elif isinstance(entry, dict):
                s = str(entry.get('label') or entry.get('text') or '').strip()
            elif isinstance(entry, (int, float, bool)):
                continue
            else:
                s = str(entry).strip()
            if s:
                out.append(s)
    # dedupe while preserving order, cap length defensively
    seen = set()
    clean = []
    for s in out:
        if s in seen:
            continue
        seen.add(s)
        clean.append(s[:500])
        if len(clean) >= 60:
            break
    return clean



BRAINSTORM_MODELS = [
    {"id": "google/gemini-3.1-pro-preview",   "label": "Gemini 3 Pro"},
    {"id": "anthropic/claude-opus-4.7",       "label": "Claude Opus 4.7"},
    {"id": "openai/gpt-5.4",                  "label": "GPT-5.4"},
    {"id": "minimax/minimax-m2.7",            "label": "MiniMax M2.7"},
    {"id": "moonshotai/kimi-k2.5",            "label": "Kimi K2.5"},
    {"id": "z-ai/glm-5.1",                    "label": "GLM 5.1"},
]
SYNTH_MODEL = os.getenv("PROMPT_SYNTH_MODEL", "anthropic/claude-sonnet-4.6")


def _call_one_model(base, headers, model_id, system, user, timeout=180):
    body = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    }
    try:
        r = fetch_json(f"{base}/chat/completions", headers=headers, method="POST", body=body, timeout=timeout)
        choices = r.get("choices") or []
        content = ""
        if choices:
            msg = choices[0].get("message") or {}
            content = msg.get("content") or ""
        if isinstance(content, list):
            content = "".join(p.get("text","") for p in content if isinstance(p, dict))
        content = str(content).strip()
        if not content:
            return {"model": model_id, "ok": False, "error": "empty response"}
        return {"model": model_id, "ok": True, "content": content}
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")[:400]
        except Exception:
            pass
        return {"model": model_id, "ok": False, "error": f"HTTP {e.code}", "detail": detail}
    except Exception as e:
        return {"model": model_id, "ok": False, "error": str(e)[:400]}


def brainstorm_prompt_multi_model(payload):
    """Run 6 top LLMs in parallel on the same draft, then synthesize into one final prompt."""
    draft = (payload.get("draftPrompt") or "").strip()
    if not draft:
        raise ValueError("Draft prompt is required")
    base, headers = prompt_headers()
    if not headers:
        raise RuntimeError("OPENAI_API_KEY or OPENROUTER_API_KEY is not configured")

    current_date = os.getenv("PROMPT_CURRENT_DATE", "2026-04-17")
    checklist_rules = _normalize_checklist(payload.get("checklist"))
    domain = payload.get("domain") or "unknown"
    agent_name = payload.get("agentName") or "unknown"
    version_name = payload.get("versionName") or "unknown"
    file_manifest = payload.get("fileManifest") or []

    # Build manifest summary for model context
    manifest_lines = []
    for f in file_manifest[:40]:
        name = f.get("name","")
        path = f.get("path","")
        if name:
            manifest_lines.append(f"- {name}  (repo path: {path})")
    manifest_block = "\n".join(manifest_lines) if manifest_lines else "(no files provided)"

    checklist_block = ""
    checklist_brain_block = ""
    checklist_synth_block = ""
    if checklist_rules:
        checklist_block = "\n".join(f"{i+1}. {r}" for i, r in enumerate(checklist_rules))
        checklist_brain_block = "--- USER CHECKLIST RULES ---\n" + checklist_block + "\n--- END CHECKLIST ---\n\n"
        checklist_synth_block = "--- USER CHECKLIST RULES (MUST all be in the final) ---\n" + checklist_block + "\n--- END ---\n\n"

    # The system prompt each model sees during the brainstorm round
    brain_system = (
        "You are an elite prompt engineer brainstorming the perfect AI-agent prompt for "
        "a production HTML redesign workflow. You will be given a draft + project context + "
        "user-selected rules. Produce ONE production-quality rewritten prompt using these sections "
        "with ## markdown headers IN THIS ORDER:\n"
        "## Objective\n## Context\n## Specific Requirements\n## Additional Mandatory Rules\n"
        "## Acceptance Criteria\n## Delivery\n"
        "All requirements must be numbered, measurable, and concrete. No filler, no 'make it better', "
        "no vague language. The Delivery section must explicitly require uploading the improved files "
        "to the GitHub repo behind https://html-redesign-dashboard.maximo-seo.ai/ AND to the local "
        "Obsidian vault path, replacing old files in the same version folder. "
        "Every checklist rule the user selected must appear under Additional Mandatory Rules AND be "
        "verified in Acceptance Criteria. "
        "Return plain markdown only, no code fences, no preamble."
    )
    brain_user = (
        f"Project domain:   {domain}\n"
        f"Target agent:     {agent_name}\n"
        f"Version folder:   {version_name}\n"
        f"Current date:     {current_date}\n\n"
        f"--- FILE MANIFEST ---\n{manifest_block}\n--- END MANIFEST ---\n\n"
        f"{checklist_brain_block}"
        f"--- USER DRAFT PROMPT ---\n{draft}\n--- END DRAFT ---\n\n"
        "Produce the best possible rewritten prompt. Distinguish your work with specificity, measurable "
        "criteria, and a rock-solid Delivery section that references the real folder paths."
    )

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {
            pool.submit(_call_one_model, base, headers, m["id"], brain_system, brain_user, 180): m
            for m in BRAINSTORM_MODELS
        }
        for fut in concurrent.futures.as_completed(futures, timeout=240):
            m = futures[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = {"model": m["id"], "ok": False, "error": str(e)[:400]}
            r["label"] = m["label"]
            results.append(r)

    successes = [r for r in results if r.get("ok") and r.get("content")]
    if not successes:
        errors = [{"model": r["model"], "label": r.get("label"), "error": r.get("error"), "detail": r.get("detail","")} for r in results]
        raise RuntimeError(json.dumps({"code": "all_models_failed", "errors": errors}, ensure_ascii=False))

    # Synthesis step — merge all successful outputs into the perfect final prompt
    drafts_block = "\n\n".join(
        f"=== DRAFT FROM {r['label']} ({r['model']}) ===\n{r['content']}\n=== END {r['label']} ==="
        for r in successes
    )
    synth_system = (
        "You are the head prompt architect. You will be given multiple expert-written versions of the "
        "same prompt produced by different elite LLMs. Your job is to synthesize ONE FINAL prompt that "
        "is strictly better than any individual version — pulling in the strongest wording, sharpest "
        "requirements, and most complete acceptance criteria from each draft, removing duplication, and "
        "producing a single clean result.\n\n"
        "Strict rules:\n"
        "1. Output PLAIN MARKDOWN. No code fences. No 'here is the synthesized prompt' preamble.\n"
        "2. Keep the exact section order: ## Objective, ## Context, ## Specific Requirements, "
        "## Additional Mandatory Rules, ## Acceptance Criteria, ## Delivery.\n"
        "3. Every numbered requirement must map to at least one acceptance criterion.\n"
        "4. Delivery must include: upload to GitHub repo maximoseo/webs-html-improvements-files "
        "(folder for the specified domain/version) AND to the Obsidian vault path "
        "C:\\Obsidian\\HTML REDESIGN\\HTML REDESIGN\\<domain>\\<agent>\\updated files\\<date>\\; "
        "replace old files in place, do not create parallel folders. Include the exact commit message "
        "format: feat(<domain>): <summary> — <date>.\n"
        "5. Use the provided current date for all date references; correct any stale dates from the drafts.\n"
        "6. Keep the Additional Mandatory Rules section only if user-selected rules exist; otherwise omit it.\n"
        "7. Style: direct, professional, zero filler. Every bullet is actionable and specific."
    )
    synth_user = (
        f"Project domain:   {domain}\n"
        f"Target agent:     {agent_name}\n"
        f"Version folder:   {version_name}\n"
        f"Current date:     {current_date}\n\n"
        f"{checklist_synth_block}"
        f"--- FILE MANIFEST ---\n{manifest_block}\n--- END MANIFEST ---\n\n"
        f"--- CANDIDATE DRAFTS FROM MULTIPLE MODELS ---\n{drafts_block}\n--- END CANDIDATES ---\n\n"
        "Produce the single synthesized final prompt now."
    )

    synth = _call_one_model(base, headers, SYNTH_MODEL, synth_system, synth_user, timeout=240)
    if not synth.get("ok") or not synth.get("content"):
        raise RuntimeError(json.dumps({
            "code": "synthesis_failed",
            "synthError": synth.get("error","unknown"),
            "synthDetail": synth.get("detail",""),
            "partialModels": [{"model": r["model"], "label": r["label"]} for r in successes],
        }, ensure_ascii=False))

    return {
        "ok": True,
        "finalPrompt": synth["content"],
        "synthModel": SYNTH_MODEL,
        "modelsUsed": [{"model": r["model"], "label": r["label"], "chars": len(r["content"])} for r in successes],
        "modelsFailed": [{"model": r["model"], "label": r.get("label"), "error": r.get("error")} for r in results if not r.get("ok")],
    }


def commit_prompt_to_github(payload):
    """Commit a single text file (the improved prompt) to the dashboard repo via GitHub Contents API."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is not configured on the server")
    repo_path = (payload.get("path") or "").strip().lstrip("/")
    content = payload.get("content") or ""
    message = (payload.get("message") or "chore: update improved prompt").strip()
    branch = (payload.get("branch") or "main").strip()
    if not repo_path:
        raise ValueError("path is required")
    if not content:
        raise ValueError("content is required")
    if ".." in repo_path or repo_path.startswith("/"):
        raise ValueError("invalid path")

    api_base = f"https://api.github.com/repos/{REPO}/contents/"
    api_url = api_base + "/".join(urllib.parse.quote(p) for p in repo_path.split("/"))
    gh_headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "dashboard-commit-bot",
    }

    # Check for existing sha
    sha = None
    try:
        existing = fetch_json(f"{api_url}?ref={urllib.parse.quote(branch)}", headers=gh_headers, timeout=30)
        if isinstance(existing, dict) and existing.get("sha"):
            sha = existing["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise

    body = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if sha:
        body["sha"] = sha

    result = fetch_json(api_url, headers=gh_headers, method="PUT", body=body, timeout=60)
    commit = result.get("commit") or {}
    contentInfo = result.get("content") or {}
    return {
        "ok": True,
        "path": repo_path,
        "branch": branch,
        "replaced": bool(sha),
        "commitSha": commit.get("sha"),
        "commitUrl": commit.get("html_url"),
        "fileUrl": contentInfo.get("html_url"),
        "downloadUrl": contentInfo.get("download_url"),
    }


def tweak_html_with_prompt(payload):
    improved_prompt = (payload.get('improvedPrompt') or '').strip()
    html_download_url = (payload.get('htmlDownloadUrl') or '').strip()
    if not improved_prompt:
        raise ValueError('improvedPrompt is required')
    if not html_download_url:
        raise ValueError('htmlDownloadUrl is required')
    base, headers = prompt_headers()
    if not headers:
        raise RuntimeError('OPENAI_API_KEY or OPENROUTER_API_KEY is not configured')
    default_model = os.getenv('PROMPT_TWEAK_MODEL', 'anthropic/claude-sonnet-4.6')
    model = (payload.get('model') or '').strip() or default_model
    domain = payload.get('domain') or 'unknown'
    agent_name = payload.get('agentName') or 'unknown'
    version_name = payload.get('versionName') or 'unknown'
    html_file_name = (payload.get('htmlFileName') or 'Improved_HTML_Template.html').strip()
    html_file_path = (payload.get('htmlFilePath') or '').strip()
    latest_only = bool(payload.get('latestOnly', True))
    file_manifest = payload.get('fileManifest') or []
    current_html = fetch_text(html_download_url)
    manifest_lines = []
    for f in file_manifest:
        name = (f.get('name') or '').strip()
        if not name:
            continue
        manifest_lines.append(f"- {name} | path: {(f.get('path') or '').strip()} | download: {(f.get('download') or '').strip()}")
    manifest_block = '\n'.join(manifest_lines) if manifest_lines else '- No manifest provided'
    latest_rule = 'Only output the final latest replacement HTML for the active file. Do not mention old parallel files, duplicate versions, or archival outputs.' if latest_only else ''
    system = ('You are a senior HTML redesign engineer. Apply the improved prompt to the provided HTML template and return the full corrected HTML file. Return raw HTML only. No markdown fences. No explanations before or after the HTML. Preserve working content and structure unless the improved prompt explicitly requires a change. Keep the file production-ready and self-contained.')
    user = (f'Target domain: {domain}\n' f'Target agent: {agent_name}\n' f'Active version folder: {version_name}\n' f'Active HTML file name: {html_file_name}\n' f'Active HTML file path: {html_file_path}\n' f'{latest_rule}\n\n' f'--- FILE MANIFEST ---\n{manifest_block}\n--- END FILE MANIFEST ---\n\n' f'--- IMPROVED PROMPT TO APPLY ---\n{improved_prompt}\n--- END IMPROVED PROMPT ---\n\n' f'--- CURRENT HTML TEMPLATE ---\n{current_html}\n--- END CURRENT HTML TEMPLATE ---\n\n' 'Now return the fully updated HTML for the active file only.')
    body = {'model': model, 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]}
    response = fetch_json(f'{base}/chat/completions', headers=headers, method='POST', body=body, timeout=240)
    choices = response.get('choices') or []
    content = ''
    if choices:
        message = choices[0].get('message') or {}
        content = message.get('content') or ''
    if isinstance(content, list):
        content = ''.join(part.get('text', '') for part in content if isinstance(part, dict))
    content = str(content).strip()
    if content.startswith('```'):
        content = content.strip('`')
        if content.lower().startswith('html'):
            content = content[4:].lstrip()
    if not content:
        raise RuntimeError('Model returned empty HTML content')
    return {'ok': True, 'model': model, 'html': content, 'summary': f'Tweaked {html_file_name} for {domain}'}


def improve_prompt_with_model(payload):
    draft = (payload.get('draftPrompt') or '').strip()
    if not draft:
        raise ValueError('Draft prompt is required')
    base, headers = prompt_headers()
    if not headers:
        raise RuntimeError('OPENAI_API_KEY or OPENROUTER_API_KEY is not configured')
    # Accept model override from the browser payload; fall back to env / default
    default_model = os.getenv('PROMPT_IMPROVER_MODEL', 'anthropic/claude-sonnet-4.6')
    model = (payload.get('model') or '').strip() or default_model
    current_date = os.getenv('PROMPT_CURRENT_DATE', '2026-04-15')
    checklist_rules = _normalize_checklist(payload.get('checklist'))

    system = (
        'You are a senior prompt engineer for agentic coding and design workflows. '
        'Rewrite the user draft into a production-ready, well-structured prompt for the specified agent. '
        'Return plain-text markdown only — no code fences, no preamble, no "here is your prompt" wrapper. '
        'The output MUST use clearly labeled sections with markdown headers (## Section Name) so the reader '
        'can instantly scan the prompt. Required sections in this order:\n'
        '## Objective — one paragraph, sharp and direct.\n'
        '## Context — domain, agent, version, relevant background.\n'
        '## Specific Requirements — numbered list of concrete requirements. No vague instructions.\n'
        '## Additional Mandatory Rules — present ONLY when the user selected checklist items; '
        'render each selected rule as a numbered bullet under this section; if no rules were selected, omit this section entirely.\n'
        '## Acceptance Criteria — numbered checklist the agent must verify before finishing. '
        'Every item from Specific Requirements and every Additional Mandatory Rule must map to at least one criterion here.\n'
        '## Delivery — mandatory export and publish instructions (Obsidian + GitHub dashboard).\n'
        'Mandatory rule: the Delivery section must explicitly require exporting the final improved files '
        'into the updated files destination in Obsidian and publishing the same deliverables to the GitHub '
        'repo behind https://html-redesign-dashboard.maximo-seo.ai/. '
        'Mandatory rule: the Delivery section must require replacing or updating the existing files for the '
        'same project/version path rather than leaving old files as the active deliverables. '
        'Mandatory rule: all date references in the generated prompt must use the current working date '
        'provided in the user message; stale dates must be updated. '
        'Writing style: direct, professional, zero filler. Every bullet point must be actionable and specific. '
        'Never use vague phrases like "make it look better" — always state the exact measurable change expected.'
    )

    if checklist_rules:
        numbered_rules = '\n'.join(f'{i+1}. {rule}' for i, rule in enumerate(checklist_rules))
        extra_rules_section = (
            '\n\n--- ADDITIONAL MANDATORY RULES (user-selected before clicking Improve) ---\n'
            'The rewritten prompt MUST include ALL of the following as hard requirements under the '
            '"## Additional Mandatory Rules" section, and MUST verify each one in "## Acceptance Criteria":\n'
            f'{numbered_rules}\n'
            '--- END ADDITIONAL MANDATORY RULES ---\n'
        )
    else:
        extra_rules_section = ''

    # Build file manifest block from payload
    file_manifest = payload.get('fileManifest') or []
    version_path = (payload.get('versionPath') or '').strip()
    github_repo_base = (payload.get('githubRepoBase') or '').strip()
    obsidian_base = (payload.get('obsidianBase') or '').strip()
    repo = 'maximoseo/webs-html-improvements-files'
    domain = payload.get('domain') or 'unknown'
    agent_name = payload.get('agentName') or 'unknown'
    version_name = payload.get('versionName') or 'unknown'

    if file_manifest:
        def _fmt_files(files, label):
            if not files:
                return ''
            lines = [f'### {label}']
            for f in files:
                name = f.get('name','')
                size = f.get('size',0)
                path = f.get('path','')
                dl   = f.get('download','')
                url  = f.get('url','')
                size_str = (f'{size/1024:.1f} KB' if size >= 1024 else f'{size} B') if size else ''
                lines.append(f'- {name} {size_str}')
                if url:  lines.append(f'  View on GitHub: {url}')
                if dl:   lines.append(f'  Raw download:   {dl}')
                if path: lines.append(f'  Repo path:      {path}')
            return '\n'.join(lines)

        html_files  = [f for f in file_manifest if f.get('name','').lower().endswith('.html')]
        txt_files   = [f for f in file_manifest if f.get('name','').lower().endswith('.txt')]
        json_files  = [f for f in file_manifest if f.get('name','').lower().endswith('.json')]
        other_files = [f for f in file_manifest if not f.get('name','').lower().endswith(('.html','.txt','.json'))]

        manifest_block = (
            f'\n\n--- CURRENT FILE MANIFEST (version: {version_name}) ---\n'
            + _fmt_files(html_files,  'HTML Templates') + '\n'
            + _fmt_files(txt_files,   'Prompts / Text Files') + '\n'
            + _fmt_files(json_files,  'Workflow / JSON Files') + '\n'
            + _fmt_files(other_files, 'Other Files') + '\n'
            + '--- END FILE MANIFEST ---\n'
        )
    else:
        manifest_block = ''

    # Build delivery paths block
    obs_path = obsidian_base or f'C:\\Obsidian\\HTML REDESIGN\\HTML REDESIGN\\{domain}\\{agent_name}\\updated files'
    gh_folder = version_path or f'{domain}/{version_name}'
    delivery_block = (
        f'\n\n--- DELIVERY DESTINATIONS ---\n'
        f'After completing all work, upload the final files to BOTH destinations below.\n'
        f'Replace the existing files in the same version folder — do not create a new parallel folder.\n\n'
        f'1. Obsidian vault (Windows path):\n'
        f'   {obs_path}\\updated files\\{current_date}\\\n'
        f'   Upload: HTML template, N8N prompt, N8N workflow, validation note, source map, summary.\n\n'
        f'2. GitHub repository:\n'
        f'   Repo:      https://github.com/{repo}\n'
        f'   Folder:    {gh_folder}\n'
        f'   Dashboard: https://html-redesign-dashboard.maximo-seo.ai/\n'
        f'   Commit message: "feat({domain}): [describe what changed] — {current_date}"\n'
        f'   After pushing, refresh the dashboard and confirm the updated files appear correctly.\n'
        f'--- END DELIVERY DESTINATIONS ---\n'
    )

    user = (
        f'Target domain:          {domain}\n'
        f'Target agent:           {agent_name}\n'
        f'Version folder:         {version_name}\n'
        f'GitHub folder URL:      {github_repo_base or f"https://github.com/{repo}/tree/main/{domain}"}\n'
        f'Obsidian base path:     {obs_path}\n'
        f'Current working date:   {current_date}\n'
        f'{manifest_block}'
        f'{delivery_block}'
        f'\n--- USER DRAFT PROMPT ---\n'
        f'{draft}\n'
        f'--- END DRAFT ---\n'
        f'{extra_rules_section}\n'
        'Rewrite the draft into the structured prompt format described in the system instructions. '
        'Every section must be present and populated. '
        'The Context section must list the exact file names from the manifest above so the agent knows exactly which files to work with. '
        'The Specific Requirements section must be a numbered list — not a flat paragraph. '
        'The Delivery section must copy the exact Obsidian path and GitHub repo path from the delivery destinations block above — '
        'include real folder paths, real file names from the manifest, and the exact commit message format. '
        'Use the current required working date above for all folder/date references and correct any stale dates found in the draft.'
    )

    body = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user},
        ],
    }
    response = fetch_json(f'{base}/chat/completions', headers=headers, method='POST', body=body, timeout=120)
    choices = response.get('choices') or []
    content = ''
    if choices:
        message = choices[0].get('message') or {}
        content = message.get('content') or ''
    if isinstance(content, list):
        content = ''.join(part.get('text', '') for part in content if isinstance(part, dict))
    content = str(content).strip()
    if not content:
        raise RuntimeError('Model returned empty content')
    return {'model': model, 'content': content}



# ---------- Palette extractor (Prompt Studio) ----------

_HEX_RE = re.compile(r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
_RGB_RE = re.compile(r'rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*[\d.]+)?\s*\)')

def _norm_hex(h):
    h = h.lower().lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    return '#' + h

def _hex_from_rgb(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(max(0,min(255,int(r))), max(0,min(255,int(g))), max(0,min(255,int(b))))

def _too_greyish(hex_color):
    h = hex_color.lstrip('#')
    r = int(h[0:2], 16); g = int(h[2:4], 16); b = int(h[4:6], 16)
    mx = max(r, g, b); mn = min(r, g, b)
    if mn >= 240 and mx >= 240: return True
    if mx <= 20: return True
    if (mx - mn) <= 8 and 40 <= mx <= 220: return True
    return False

def _luminance(hex_color):
    h = hex_color.lstrip('#')
    r = int(h[0:2], 16); g = int(h[2:4], 16); b = int(h[4:6], 16)
    return 0.2126*r + 0.7152*g + 0.0722*b

def _fetch_page_text(url, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (HermesPaletteExtractor/1.0)'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        encoding = resp.headers.get_content_charset() or 'utf-8'
        return data.decode(encoding, errors='replace'), resp.geturl()

def _collect_stylesheet_urls(html, base_url):
    out = []
    for m in re.finditer(r'<link\b[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*>', html, re.I):
        tag = m.group(0)
        href = re.search(r'href\s*=\s*["\']([^"\']+)["\']', tag)
        if href:
            out.append(urllib.parse.urljoin(base_url, href.group(1)))
        if len(out) >= 5:
            break
    return out

def extract_palette_from_url(url, max_colors=10):
    u = urllib.parse.urlparse(url)
    if u.scheme not in ('http','https'):
        raise ValueError('Only http/https URLs allowed')
    host = (u.hostname or '').lower()
    if host in ('localhost','127.0.0.1','0.0.0.0','::1'):
        raise ValueError('Private/loopback host not allowed')
    if host.startswith('10.') or host.startswith('192.168.') or host.startswith('169.254.') or re.match(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.', host):
        raise ValueError('Private host not allowed')

    html, final_url = _fetch_page_text(url)
    css_blobs = [html]
    for css_url in _collect_stylesheet_urls(html, final_url)[:3]:
        try:
            body, _ = _fetch_page_text(css_url, timeout=12)
            css_blobs.append(body)
        except Exception:
            continue

    combined = '\n'.join(css_blobs)

    counts = {}
    for m in _HEX_RE.finditer(combined):
        h = _norm_hex(m.group(0))
        counts[h] = counts.get(h, 0) + 1
    for m in _RGB_RE.finditer(combined):
        h = _hex_from_rgb(m.group(1), m.group(2), m.group(3))
        counts[h] = counts.get(h, 0) + 1

    brand = [(c, n) for c, n in counts.items() if not _too_greyish(c)]
    brand.sort(key=lambda x: (-x[1], abs(_luminance(x[0]) - 128)))
    neutrals = sorted([(c, n) for c, n in counts.items() if _too_greyish(c)], key=lambda x: -x[1])[:5]

    top_brand = brand[:max_colors]

    title = ''
    m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
    if m:
        title = m.group(1).strip()[:200]
    desc = ''
    m = re.search(r'<meta[^>]+name\s*=\s*["\']description["\'][^>]*content\s*=\s*["\']([^"\']+)["\']', html, re.I)
    if m:
        desc = m.group(1).strip()[:300]

    return {
        'ok': True,
        'url': final_url,
        'title': title,
        'description': desc,
        'totalDistinctColors': len(counts),
        'brandPalette': [{'hex': c, 'count': n} for c, n in top_brand],
        'neutrals': [{'hex': c, 'count': n} for c, n in neutrals],
    }


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = 'DashboardHTTP/1.0'

    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/health':
            return json_response(self, 200, {
                'ok': True,
                'n8nConfigured': bool(os.getenv('N8N_API_KEY')),
                'promptConfigured': bool(os.getenv('OPENAI_API_KEY') or os.getenv('OPENROUTER_API_KEY')),
                'brainstormConfigured': bool(os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')),
                'githubCommitConfigured': bool(os.getenv('GITHUB_TOKEN')),
                'brainstormModels': [{'id': m['id'], 'label': m['label']} for m in BRAINSTORM_MODELS],
                'synthModel': SYNTH_MODEL,
                'promptImproveDefaultModel': os.getenv('PROMPT_IMPROVER_MODEL', 'anthropic/claude-sonnet-4.6'),
                'promptTweakDefaultModel': os.getenv('PROMPT_TWEAK_MODEL', 'anthropic/claude-sonnet-4.6'),
                'promptSynthDefaultModel': SYNTH_MODEL,
                'paletteExtractorConfigured': True,
                'tweakConfigured': bool(os.getenv('OPENAI_API_KEY') or os.getenv('OPENROUTER_API_KEY')),
                'commentsConfigured': supabase_comments_config()['configured'],
                'commentsTable': supabase_comments_config()['table'],
            })
        if parsed.path == '/api/comments':
            query = urllib.parse.parse_qs(parsed.query)
            filters = {k: (v[0] if isinstance(v, list) and v else '') for k, v in query.items()}
            try:
                result = list_supabase_comments(filters)
                return json_response(self, 200, result)
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1000]
                return json_response(self, 502, {'ok': False, 'error': f'Supabase API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/n8n/status':
            query = urllib.parse.parse_qs(parsed.query)
            domain = (query.get('domain') or [''])[0]
            configured = bool(os.getenv('N8N_API_KEY'))
            payload = {'configured': configured, 'domain': normalize_domain(domain), 'mappingFile': MAP_FILE.name}
            if configured and domain:
                try:
                    workflow_id, details = resolve_workflow_id(domain)
                    payload.update({'ok': True, 'workflowId': workflow_id, 'details': details})
                except ValueError as exc:
                    payload.update({'ok': False, 'error': json.loads(str(exc))})
                except LookupError as exc:
                    payload.update({'ok': False, 'error': json.loads(str(exc))})
                except Exception as exc:
                    payload.update({'ok': False, 'error': {'code': 'unexpected_error', 'message': str(exc)}})
            return json_response(self, 200, payload)
        return self.serve_static(parsed.path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            payload = read_request_json(self)
        except Exception:
            return json_response(self, 400, {'ok': False, 'error': 'Invalid JSON body'})

        if parsed.path == '/api/prompt/improve':
            try:
                result = improve_prompt_with_model(payload)
                return json_response(self, 200, {'ok': True, **result})
            except RuntimeError as exc:
                return json_response(self, 503, {'ok': False, 'error': str(exc)})
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1000]
                return json_response(self, 502, {'ok': False, 'error': f'Model API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/prompt/palette':
            try:
                url = (payload.get('url') or '').strip()
                if not url:
                    return json_response(self, 400, {'ok': False, 'error': 'url is required'})
                max_colors = int(payload.get('maxColors') or 10)
                max_colors = max(3, min(max_colors, 20))
                result = extract_palette_from_url(url, max_colors=max_colors)
                return json_response(self, 200, result)
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except urllib.error.HTTPError as exc:
                return json_response(self, 502, {'ok': False, 'error': f'Fetch failed {exc.code}', 'details': str(exc)[:300]})
            except urllib.error.URLError as exc:
                return json_response(self, 502, {'ok': False, 'error': f'Fetch failed: {exc.reason}'})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)[:400]})

        if parsed.path == '/api/prompt/brainstorm':
            try:
                result = brainstorm_prompt_multi_model(payload)
                return json_response(self, 200, result)
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except RuntimeError as exc:
                msg = str(exc)
                try:
                    parsed_err = json.loads(msg)
                    return json_response(self, 502, {'ok': False, 'error': parsed_err})
                except Exception:
                    return json_response(self, 503, {'ok': False, 'error': msg})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/prompt/tweak':
            try:
                result = tweak_html_with_prompt(payload)
                return json_response(self, 200, result)
            except RuntimeError as exc:
                return json_response(self, 503, {'ok': False, 'error': str(exc)})
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1000]
                return json_response(self, 502, {'ok': False, 'error': f'Model API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/prompt/commit':
            try:
                result = commit_prompt_to_github(payload)
                return json_response(self, 200, result)
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except RuntimeError as exc:
                return json_response(self, 503, {'ok': False, 'error': str(exc)})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1000]
                return json_response(self, 502, {'ok': False, 'error': f'GitHub API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/comments':
            try:
                result = save_supabase_comment(payload)
                return json_response(self, 200, result)
            except ValueError as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except RuntimeError as exc:
                return json_response(self, 503, {'ok': False, 'error': str(exc)})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1200]
                return json_response(self, 502, {'ok': False, 'error': f'Supabase API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/n8n/deploy':
            domain = normalize_domain(payload.get('domain', ''))
            file_path = (payload.get('filePath') or '').strip().lstrip('/')
            if not domain or not file_path:
                return json_response(self, 400, {'ok': False, 'error': 'domain and filePath are required'})
            if not file_path.lower().endswith('.json'):
                return json_response(self, 400, {'ok': False, 'error': 'Only workflow JSON files can be deployed'})
            if not os.getenv('N8N_API_KEY'):
                return json_response(self, 503, {'ok': False, 'error': 'N8N_API_KEY is not configured on the server'})
            try:
                workflow_id, details = resolve_workflow_id(domain, payload.get('workflowId'))
                raw_url = f"{RAW_BASE}/{'/'.join(urllib.parse.quote(part) for part in file_path.split('/'))}"
                source = json.loads(fetch_text(raw_url))
                base = os.getenv('N8N_BASE_URL', DEFAULT_N8N_BASE).rstrip('/')
                headers = n8n_headers()
                live = fetch_json(f'{base}/api/v1/workflows/{workflow_id}', headers=headers)
                update_payload = build_workflow_payload(source, live)
                updated = fetch_json(f'{base}/api/v1/workflows/{workflow_id}', headers=headers, method='PUT', body=update_payload, timeout=120)
                return json_response(self, 200, {
                    'ok': True,
                    'domain': domain,
                    'filePath': file_path,
                    'workflowId': workflow_id,
                    'workflowName': updated.get('name') or live.get('name'),
                    'active': updated.get('active', live.get('active')),
                    'resolution': details,
                })
            except ValueError as exc:
                return json_response(self, 409, {'ok': False, 'error': json.loads(str(exc))})
            except LookupError as exc:
                return json_response(self, 404, {'ok': False, 'error': json.loads(str(exc)), 'mappingFile': MAP_FILE.name})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1500]
                return json_response(self, 502, {'ok': False, 'error': f'n8n API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        return json_response(self, 404, {'ok': False, 'error': 'Not found'})

    def serve_static(self, path):
        clean = posixpath.normpath(urllib.parse.unquote(path))
        if clean in ('', '.', '/'):
            target = INDEX
        else:
            target = (ROOT / clean.lstrip('/')).resolve()
            if ROOT not in target.parents and target != ROOT:
                return json_response(self, 403, {'ok': False, 'error': 'Forbidden'})
        if not target.exists() or not target.is_file():
            return json_response(self, 404, {'ok': False, 'error': 'Not found'})
        content_type, _ = mimetypes.guess_type(str(target))
        if not content_type:
            content_type = 'application/octet-stream'
        return text_response(self, 200, target.read_bytes(), content_type)


def main():
    port = int(os.getenv('PORT', '8000'))
    server = ThreadingHTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f'listening on {port}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
