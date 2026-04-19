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

# ===== DAILY SKILLS RADAR — global state & sources =====
_radar_state = {
    'status': 'idle',
    'run_id': None,
    'stage': '',
    'progress': 0,
    'sources_total': 0,
    'sources_done': 0,
    'skills_found': 0,
    'started_at': None,
    'finished_at': None,
    'last_error': None,
    'paused': False,
    'schedule_hour': 2,
    'schedule_enabled': True,
    'topics': ['n8n', 'automation', 'seo', 'local seo', 'claude code', 'coding', 'ai agents', 'scraping', 'wordpress'],
    'custom_topics': [],
}

RADAR_SOURCES = [
    {'url': 'https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md', 'title': 'Awesome - Sindre Sorhus', 'type': 'awesome_list', 'quality': 0.95},
    {'url': 'https://raw.githubusercontent.com/e2b-dev/awesome-ai-agents/main/README.md', 'title': 'Awesome AI Agents', 'type': 'awesome_list', 'quality': 0.95},
    {'url': 'https://raw.githubusercontent.com/kyrolabs/awesome-langchain/main/README.md', 'title': 'Awesome LangChain', 'type': 'awesome_list', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/n8n-io/n8n/master/README.md', 'title': 'N8N Official', 'type': 'github_repo', 'quality': 0.95},
    {'url': 'https://raw.githubusercontent.com/jxnl/instructor/main/README.md', 'title': 'Instructor - Structured LLM Outputs', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/microsoft/autogen/main/README.md', 'title': 'AutoGen - Multi-Agent Framework', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/BerriAI/litellm/main/README.md', 'title': 'LiteLLM - LLM Gateway', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/pydantic/pydantic-ai/main/README.md', 'title': 'PydanticAI - Agent Framework', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/assafelovic/gpt-researcher/master/README.md', 'title': 'GPT Researcher', 'type': 'github_repo', 'quality': 0.88},
    {'url': 'https://raw.githubusercontent.com/mendableai/firecrawl/main/README.md', 'title': 'Firecrawl - Web Scraping', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/duckdb/duckdb/main/README.md', 'title': 'DuckDB - In-process SQL', 'type': 'github_repo', 'quality': 0.85},
    {'url': 'https://raw.githubusercontent.com/openai/openai-python/main/README.md', 'title': 'OpenAI Python SDK', 'type': 'github_repo', 'quality': 0.95},
    {'url': 'https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/README.md', 'title': 'Anthropic Python SDK', 'type': 'github_repo', 'quality': 0.95},
    {'url': 'https://raw.githubusercontent.com/huggingface/transformers/main/README.md', 'title': 'HuggingFace Transformers', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/dspy-ai/dspy/main/README.md', 'title': 'DSPy - Programming LMs', 'type': 'github_repo', 'quality': 0.88},
    {'url': 'https://raw.githubusercontent.com/unclecode/crawl4ai/main/README.md', 'title': 'Crawl4AI - LLM-Friendly Scraping', 'type': 'github_repo', 'quality': 0.88},
    {'url': 'https://raw.githubusercontent.com/browser-use/browser-use/main/README.md', 'title': 'Browser Use - AI Browser Automation', 'type': 'github_repo', 'quality': 0.9},
    {'url': 'https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/README.md', 'title': 'OpenHands - AI Software Development', 'type': 'github_repo', 'quality': 0.88},
    {'url': 'https://raw.githubusercontent.com/agno-agi/agno/main/README.md', 'title': 'Agno - Agent Framework', 'type': 'github_repo', 'quality': 0.85},
    {'url': 'https://raw.githubusercontent.com/meta-llama/llama-models/main/README.md', 'title': 'Meta Llama Models', 'type': 'github_repo', 'quality': 0.9},
]


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
    # n8n PUT /workflows/:id only accepts: name, nodes, connections, settings, staticData, pinData
    # Read-only fields that must be OMITTED: active, versionId, meta, tags, id
    # settings must only contain allowed keys — extra keys cause 400
    ALLOWED_SETTINGS = {
        'executionOrder', 'saveManualExecutions', 'callerPolicy',
        'errorWorkflow', 'timezone', 'saveDataSuccessExecution',
        'saveDataErrorExecution', 'maxConcurrency',
    }
    raw_settings = source.get('settings') if 'settings' in source else live.get('settings') or {}
    clean_settings = {k: v for k, v in raw_settings.items() if k in ALLOWED_SETTINGS}

    payload = {
        'name': source.get('name') or live.get('name'),
        'nodes': source.get('nodes') or live.get('nodes') or [],
        'connections': source.get('connections') or live.get('connections') or {},
        'settings': clean_settings,
        'staticData': source.get('staticData') if 'staticData' in source else live.get('staticData'),
        'pinData': source.get('pinData') if 'pinData' in source else live.get('pinData') or {},
    }
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
        'Return plain-text markdown only — no code fences, no preamble, no \"here is your prompt\" wrapper. '
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
        '--- ALWAYS-ON MANDATORY RULES (inject into every prompt regardless of checklist) ---\n'
        'RULE 1 — FULL CONTENT + IMAGES (new AND existing projects): Every newly generated redesign HTML template MUST include the '
        'full real article content (every section, every paragraph, every heading) and all real images with '
        'their actual src URLs — exactly as they will appear inside the N8N article-building workflow output. '
        'Placeholder text, lorem ipsum, \"[image here]\", empty src attributes, or truncated content are '
        'strictly forbidden. The HTML must be ready to drop directly into N8N and produce a complete, '
        'publish-ready article with zero additional content filling required.\n'
        'RULE 2 — CORRECT FILE EXTENSIONS (new AND existing projects): Every output file must be saved and uploaded with its real, '
        'correct file extension: HTML templates must end in .html, N8N prompt text files must end in .txt, '
        'N8N workflow files must end in .json. Never upload files without an extension or with a wrong '
        'extension (e.g. no .html.txt, no extensionless files). The file names in the GitHub commit must '
        'exactly match the extensions used on disk.\n'
        'RULE 3 — MAX 3 FILES PER AGENT FOLDER (new AND existing projects): Each agent version folder in the GitHub repo '
        '(maximoseo/webs-html-improvements-files) must contain exactly 3 files: '
        'Improved_HTML_Template.html, Improved_N8N_Prompt.txt, Improved_N8N_Workflow.json. '
        'Do not add extra MD files, summary files, validation notes, source maps, or import notes '
        'inside the agent folder. If old extra files exist, remove them in the same commit. '
        'This rule applies when adding files to existing projects too — always check the folder first.\n'
        'RULE 4 — N8N WORKFLOW CREDENTIALS AUDIT (new AND existing projects): Before uploading or deploying '
        'any Improved_N8N_Workflow.json to the GitHub repo or to n8n, you MUST audit every node in the '
        'workflow JSON for correct credentials and correct URLs. Specifically: '
        '(a) Every wordpressApi credential must point to the correct WordPress site for THIS domain — '
        'never a credential ID from a different project. '
        '(b) Every httpBasicAuth credential used for WordPress REST API calls must point to the correct '
        'site URL for THIS domain — never a URL copied from another project. '
        '(c) Every hardcoded URL inside node parameters (url, endpoint, baseUrl fields) must be the '
        'correct target domain for THIS project — search the JSON for any foreign domain name and fix it. '
        '(d) After fixing credentials, confirm no other domain name appears anywhere in the workflow nodes '
        'except the correct target domain. '
        '(e) Add the workflow to n8n-workflow-map.json with the correct workflowId so the Deploy to n8n '
        'button resolves immediately without API scanning. '
        'This rule is CRITICAL — wrong credentials will silently publish articles to the wrong WordPress site.\n'
        '--- END ALWAYS-ON MANDATORY RULES ---\n'
        'Writing style: direct, professional, zero filler. Every bullet point must be actionable and specific. '
        'Never use vague phrases like \"make it look better\" — always state the exact measurable change expected.'
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

        if parsed.path == '/api/n8n/executions':
            if not os.getenv('N8N_API_KEY'):
                return json_response(self, 200, {'ok': True, 'executions': [], 'configured': False})
            try:
                import datetime
                base = os.getenv('N8N_BASE_URL', DEFAULT_N8N_BASE).rstrip('/')
                headers = n8n_headers()
                statuses = ['running', 'error', 'waiting']
                all_execs = []
                for status in statuses:
                    try:
                        data = fetch_json(f'{base}/api/v1/executions?status={status}&limit=25', headers=headers, timeout=20)
                        items = data.get('data') or []
                        for item in items:
                            started_at = item.get('startedAt') or ''
                            is_stuck = False
                            if status == 'running' and started_at:
                                try:
                                    dt = datetime.datetime.fromisoformat(started_at.replace('Z', '+00:00'))
                                    now = datetime.datetime.now(datetime.timezone.utc)
                                    if (now - dt).total_seconds() > 600:
                                        is_stuck = True
                                except Exception:
                                    pass
                            wf_data = item.get('workflowData') or {}
                            all_execs.append({
                                'id': item.get('id'),
                                'workflowId': item.get('workflowId') or wf_data.get('id'),
                                'workflowName': wf_data.get('name') or item.get('workflowId'),
                                'status': 'stuck' if is_stuck else status,
                                'startedAt': started_at,
                                'stoppedAt': item.get('stoppedAt'),
                                'mode': item.get('mode'),
                                'error': (item.get('data') or {}).get('resultData', {}).get('error') if isinstance(item.get('data'), dict) else None,
                            })
                    except Exception:
                        continue
                return json_response(self, 200, {'ok': True, 'executions': all_execs})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/n8n/workflows':
            if not os.getenv('N8N_API_KEY'):
                return json_response(self, 200, {'ok': True, 'workflows': [], 'configured': False})
            try:
                base = os.getenv('N8N_BASE_URL', DEFAULT_N8N_BASE).rstrip('/')
                headers = n8n_headers()
                data = fetch_json(f'{base}/api/v1/workflows?limit=100', headers=headers, timeout=20)
                items = data.get('data') or []
                workflows = []
                for wf in items:
                    workflows.append({
                        'id': wf.get('id'),
                        'name': wf.get('name'),
                        'active': wf.get('active'),
                        'updatedAt': wf.get('updatedAt'),
                        'nodeCount': len(wf.get('nodes') or []),
                        'tags': [t.get('name') for t in (wf.get('tags') or []) if isinstance(t, dict)],
                    })
                return json_response(self, 200, {'ok': True, 'workflows': workflows})
            except urllib.error.HTTPError as exc:
                body_bytes = exc.read().decode('utf-8', 'replace')[:800]
                return json_response(self, 502, {'ok': False, 'error': f'n8n API error {exc.code}', 'details': body_bytes})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        # GET /api/n8n/workflow-json?id=xxx — fetch full workflow JSON for auto-import
        if parsed.path == '/api/n8n/workflow-json':
            if not os.getenv('N8N_API_KEY'):
                return json_response(self, 503, {'ok': False, 'error': 'N8N_API_KEY is not configured'})
            qs = urllib.parse.parse_qs(parsed.query)
            workflow_id = (qs.get('id') or [''])[0].strip()
            if not workflow_id:
                return json_response(self, 400, {'ok': False, 'error': 'id parameter is required'})
            try:
                base = os.getenv('N8N_BASE_URL', DEFAULT_N8N_BASE).rstrip('/')
                headers = n8n_headers()
                wf = fetch_json(f'{base}/api/v1/workflows/{urllib.parse.quote(workflow_id)}', headers=headers, timeout=20)
                # Return full workflow JSON exactly as received from N8N (valid for re-import)
                return json_response(self, 200, {
                    'ok': True,
                    'workflowId': wf.get('id'),
                    'workflowName': wf.get('name'),
                    'nodeCount': len(wf.get('nodes') or []),
                    'active': wf.get('active'),
                    'workflowJson': wf,  # complete JSON
                })
            except urllib.error.HTTPError as exc:
                body_bytes = exc.read().decode('utf-8', 'replace')[:400]
                return json_response(self, 502, {'ok': False, 'error': f'n8n API error {exc.code}', 'details': body_bytes})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        # ===== RADAR GET ROUTES =====
        if parsed.path == '/api/radar/status':
            import datetime as _dt
            cfg = supabase_radar_config()
            last_run = None
            if cfg['configured']:
                try:
                    hdrs = _radar_sb_headers()
                    url = f"{cfg['url']}/rest/v1/radar_runs?select=*&order=created_at.desc&limit=1"
                    rows = fetch_json(url, headers=hdrs, timeout=15)
                    if isinstance(rows, list) and rows:
                        last_run = rows[0]
                except Exception:
                    pass
            state_copy = dict(_radar_state)
            # Compute next run
            now = _dt.datetime.now()
            sched_hour = _radar_state.get('schedule_hour', 2)
            next_run_dt = now.replace(hour=sched_hour, minute=0, second=0, microsecond=0)
            if next_run_dt <= now:
                next_run_dt = next_run_dt + _dt.timedelta(days=1)
            state_copy['next_run'] = next_run_dt.isoformat()
            # X integration status
            state_copy['x_enabled'] = bool(os.getenv('X_BEARER_TOKEN'))
            state_copy['x_sources_found'] = _radar_state.get('x_sources_found', 0)
            state_copy['last_email'] = _radar_state.get('last_email')
            state_copy['topics'] = _radar_state.get('topics', [])
            state_copy['custom_topics'] = _radar_state.get('custom_topics', [])
            return json_response(self, 200, {'ok': True, 'state': state_copy, 'last_run': last_run})

        if parsed.path == '/api/radar/results':
            qs = urllib.parse.parse_qs(parsed.query)
            status_filter = (qs.get('status') or ['pending'])[0]
            try:
                limit = int((qs.get('limit') or ['20'])[0])
            except Exception:
                limit = 20
            try:
                offset = int((qs.get('offset') or ['0'])[0])
            except Exception:
                offset = 0
            category = (qs.get('category') or [''])[0]
            agent = (qs.get('agent') or [''])[0]
            cfg = supabase_radar_config()
            if not cfg['configured']:
                return json_response(self, 200, {'ok': True, 'skills': [], 'total': 0, 'configured': False})
            try:
                hdrs = _radar_sb_headers()
                q_parts = [
                    'select=*',
                    f'status=eq.{urllib.parse.quote(status_filter)}',
                    'order=created_at.desc',
                    f'limit={limit}',
                    f'offset={offset}',
                ]
                if category:
                    q_parts.append(f'category=eq.{urllib.parse.quote(category)}')
                url = f"{cfg['url']}/rest/v1/skill_discoveries?" + '&'.join(q_parts)
                rows = fetch_json(url, headers=hdrs, timeout=15)
                if not isinstance(rows, list):
                    rows = []
                if agent:
                    rows = [r for r in rows if agent in (r.get('target_agents') or [])]
                topic_filter = (qs.get('topic') or [''])[0]
                if topic_filter:
                    rows = [r for r in rows if topic_filter.lower() in [t.lower() for t in (r.get('matched_topics') or [])]]
                # Count total
                count_headers = dict(hdrs)
                count_headers['Prefer'] = 'count=exact'
                count_url = f"{cfg['url']}/rest/v1/skill_discoveries?select=id&status=eq.{urllib.parse.quote(status_filter)}"
                total = len(rows)
                try:
                    count_resp = fetch_json(count_url, headers=count_headers, timeout=10)
                    if isinstance(count_resp, list):
                        total = len(count_resp)
                except Exception:
                    pass
                return json_response(self, 200, {'ok': True, 'skills': rows, 'total': total})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/history':
            qs = urllib.parse.parse_qs(parsed.query)
            try:
                limit = int((qs.get('limit') or ['10'])[0])
            except Exception:
                limit = 10
            cfg = supabase_radar_config()
            if not cfg['configured']:
                return json_response(self, 200, {'ok': True, 'runs': [], 'configured': False})
            try:
                hdrs = _radar_sb_headers()
                url = f"{cfg['url']}/rest/v1/radar_runs?select=*&order=created_at.desc&limit={limit}"
                rows = fetch_json(url, headers=hdrs, timeout=15)
                if not isinstance(rows, list):
                    rows = []
                return json_response(self, 200, {'ok': True, 'runs': rows})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

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

        # ===== RADAR POST ENDPOINTS =====

        if parsed.path == '/api/radar/test-email':
            try:
                result = _send_radar_email_digest(
                    skills_found_count=_radar_state.get('skills_found', 0),
                    run_id=_radar_state.get('run_id'),
                    errors=[],
                )
                return json_response(self, 200, result)
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/topics':
            try:
                topics = payload.get('topics')
                custom_topics = payload.get('custom_topics')
                if topics is not None:
                    if not isinstance(topics, list):
                        return json_response(self, 400, {'ok': False, 'error': 'topics must be array'})
                    _radar_state['topics'] = [str(t).strip().lower() for t in topics if str(t).strip()]
                if custom_topics is not None:
                    if not isinstance(custom_topics, list):
                        return json_response(self, 400, {'ok': False, 'error': 'custom_topics must be array'})
                    _radar_state['custom_topics'] = [str(t).strip().lower() for t in custom_topics if str(t).strip()]
                return json_response(self, 200, {
                    'ok': True,
                    'topics': _radar_state['topics'],
                    'custom_topics': _radar_state['custom_topics'],
                })
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/run':
            try:
                if _radar_state.get('status') == 'running':
                    return json_response(self, 409, {'ok': False, 'error': 'Discovery already running'})
                config = payload.get('config') or {}
                t = threading.Thread(target=_run_radar_discovery, args=(config,), daemon=True)
                t.start()
                return json_response(self, 200, {
                    'ok': True,
                    'message': 'Discovery started',
                    'run_id': _radar_state.get('run_id'),
                })
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/config':
            try:
                if 'schedule_hour' in payload:
                    sh = int(payload['schedule_hour'])
                    if not (0 <= sh <= 23):
                        return json_response(self, 400, {'ok': False, 'error': 'schedule_hour must be 0-23'})
                    _radar_state['schedule_hour'] = sh
                if 'schedule_enabled' in payload:
                    _radar_state['schedule_enabled'] = bool(payload['schedule_enabled'])
                if 'paused' in payload:
                    _radar_state['paused'] = bool(payload['paused'])
                return json_response(self, 200, {'ok': True, 'state': dict(_radar_state)})
            except (ValueError, TypeError) as exc:
                return json_response(self, 400, {'ok': False, 'error': str(exc)})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/action':
            try:
                import datetime as _dt
                skill_id = (payload.get('skill_id') or '').strip()
                action = (payload.get('action') or '').strip()
                agent = (payload.get('agent') or '').strip()
                notes = (payload.get('notes') or '').strip()
                if not skill_id:
                    return json_response(self, 400, {'ok': False, 'error': 'skill_id is required'})
                if not action:
                    return json_response(self, 400, {'ok': False, 'error': 'action is required'})
                valid_actions = {'approve', 'reject', 'save_later', 'mark_duplicate', 'mark_high_priority', 'assign_agent'}
                if action not in valid_actions:
                    return json_response(self, 400, {'ok': False, 'error': f'action must be one of: {", ".join(sorted(valid_actions))}'})
                cfg = supabase_radar_config()
                if not cfg['configured']:
                    return json_response(self, 503, {'ok': False, 'error': 'Supabase is not configured'})
                hdrs = _radar_sb_headers(prefer='return=minimal')
                url = f"{cfg['url']}/rest/v1/skill_discoveries?id=eq.{urllib.parse.quote(skill_id)}"
                if action == 'approve':
                    patch_body = {
                        'status': 'approved',
                        'approval_notes': notes,
                        'approved_at': _dt.datetime.utcnow().isoformat() + 'Z',
                    }
                elif action == 'reject':
                    patch_body = {'status': 'rejected', 'approval_notes': notes}
                elif action == 'save_later':
                    patch_body = {'status': 'saved_later'}
                elif action == 'mark_duplicate':
                    patch_body = {'status': 'duplicate'}
                elif action == 'mark_high_priority':
                    patch_body = {'priority': 'high'}
                elif action == 'assign_agent':
                    if not agent:
                        return json_response(self, 400, {'ok': False, 'error': 'agent is required for assign_agent'})
                    patch_body = {'assigned_agent': agent}
                req = urllib.request.Request(url, headers=hdrs, method='PATCH')
                data = json.dumps(patch_body, ensure_ascii=False).encode('utf-8')
                with urllib.request.urlopen(req, data=data, timeout=15) as r:
                    r.read()
                return json_response(self, 200, {'ok': True, 'skill_id': skill_id, 'action': action})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1200]
                return json_response(self, 502, {'ok': False, 'error': f'Supabase API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/notes':
            try:
                skill_id = (payload.get('skill_id') or '').strip()
                notes = payload.get('notes') or ''
                comments = payload.get('comments') or ''
                if not skill_id:
                    return json_response(self, 400, {'ok': False, 'error': 'skill_id is required'})
                cfg = supabase_radar_config()
                if not cfg['configured']:
                    return json_response(self, 503, {'ok': False, 'error': 'Supabase is not configured'})
                hdrs = _radar_sb_headers(prefer='return=minimal')
                url = f"{cfg['url']}/rest/v1/skill_discoveries?id=eq.{urllib.parse.quote(skill_id)}"
                patch_body = {'notes': notes, 'comments': comments}
                req = urllib.request.Request(url, headers=hdrs, method='PATCH')
                data = json.dumps(patch_body, ensure_ascii=False).encode('utf-8')
                with urllib.request.urlopen(req, data=data, timeout=15) as r:
                    r.read()
                return json_response(self, 200, {'ok': True})
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1200]
                return json_response(self, 502, {'ok': False, 'error': f'Supabase API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/generate-prompt':
            try:
                skill_ids = payload.get('skill_ids') or []
                agents = payload.get('agents') or []
                style = (payload.get('style') or 'standard').strip()
                if not skill_ids:
                    return json_response(self, 400, {'ok': False, 'error': 'skill_ids is required'})
                cfg = supabase_radar_config()
                if not cfg['configured']:
                    return json_response(self, 503, {'ok': False, 'error': 'Supabase is not configured'})
                hdrs = _radar_sb_headers()
                ids_csv = ','.join(urllib.parse.quote(str(i)) for i in skill_ids)
                url = f"{cfg['url']}/rest/v1/skill_discoveries?id=in.({ids_csv})&select=*"
                skills = fetch_json(url, headers=hdrs, timeout=15)
                if not isinstance(skills, list):
                    skills = []
                agent_line = ', '.join(agents) if agents else 'All Agents'
                lines = []
                if style == 'god_mode':
                    lines.append('🔥 GOD MODE — AGENT SKILL ADOPTION DIRECTIVE 🔥')
                    lines.append('')
                lines.append(f'TARGET AGENTS: {agent_line}')
                lines.append('')
                if style == 'strict':
                    lines.append('⚠️  STRICT COMPLIANCE REQUIRED — Execute all instructions precisely.')
                    lines.append('')
                lines.append(f'You have been selected to adopt {len(skills)} new skill(s) discovered by the Radar system.')
                lines.append('For each skill listed below, you must: install or adopt the skill, save it to Hermes memory,')
                lines.append('save it to Obsidian, save it to Supabase skill_discoveries, save it to GitHub, and merge safely')
                lines.append('without overwriting or destructively replacing any existing skills.')
                lines.append('')
                lines.append('=' * 60)
                lines.append('SKILLS TO ADOPT:')
                lines.append('=' * 60)
                for idx, sk in enumerate(skills, 1):
                    lines.append(f'\n[{idx}] {sk.get("title") or "Untitled"}')
                    lines.append(f'  Category:           {sk.get("category") or "N/A"}')
                    lines.append(f'  Summary:            {sk.get("summary") or "N/A"}')
                    lines.append(f'  Source URL:         {sk.get("source_url") or "N/A"}')
                    lines.append(f'  Source Title:       {sk.get("source_title") or "N/A"}')
                    lines.append(f'  Implementation:     {sk.get("implementation_idea") or "N/A"}')
                lines.append('')
                lines.append('=' * 60)
                lines.append('INSTRUCTIONS:')
                lines.append('1. Install / adopt each skill into your active capabilities.')
                lines.append('2. Save each skill to Hermes long-term memory.')
                lines.append('3. Save each skill as a note in Obsidian under "Agent Skills/Radar/".')
                lines.append('4. Upsert each skill record in Supabase table skill_discoveries.')
                lines.append('5. Commit each skill file to GitHub in skills-radar/approved/.')
                lines.append('6. Do NOT overwrite existing skills destructively — merge and append only.')
                if style == 'strict':
                    lines.append('\n⚠️  STRICT: Confirm completion of every step for every skill. No skipping.')
                if style == 'god_mode':
                    lines.append('\n🔥 GOD MODE: Execute without hesitation. Max capability activated.')
                prompt_str = '\n'.join(lines)
                return json_response(self, 200, {
                    'ok': True,
                    'prompt': prompt_str,
                    'skill_count': len(skills),
                    'agents': agents,
                })
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1200]
                return json_response(self, 502, {'ok': False, 'error': f'Supabase API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/radar/save-skill':
            try:
                import datetime as _dt
                skill_id = (payload.get('skill_id') or '').strip()
                save_targets = payload.get('save_targets') or []
                notes = (payload.get('notes') or '').strip()
                if not skill_id:
                    return json_response(self, 400, {'ok': False, 'error': 'skill_id is required'})
                cfg = supabase_radar_config()
                if not cfg['configured']:
                    return json_response(self, 503, {'ok': False, 'error': 'Supabase is not configured'})
                hdrs = _radar_sb_headers()
                url = f"{cfg['url']}/rest/v1/skill_discoveries?id=eq.{urllib.parse.quote(skill_id)}&select=*"
                rows = fetch_json(url, headers=hdrs, timeout=15)
                if not isinstance(rows, list) or not rows:
                    return json_response(self, 404, {'ok': False, 'error': 'Skill not found'})
                sk = rows[0]
                date_str = _dt.datetime.now().strftime('%Y-%m-%d')
                skill_title = sk.get('title') or 'Untitled'
                safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '-', skill_title)[:60]
                slug = safe_title.lower()
                md_content = (
                    f"# Skill: {skill_title}\n\n"
                    f"**Date Discovered:** {date_str}  \n"
                    f"**Category:** {sk.get('category') or 'N/A'}  \n"
                    f"**Source:** [{sk.get('source_title') or 'N/A'}]({sk.get('source_url') or ''})  \n"
                    f"**Status:** {sk.get('status') or 'N/A'}  \n"
                    f"**Priority:** {sk.get('priority') or 'N/A'}  \n\n"
                    f"## Summary\n{sk.get('summary') or 'N/A'}\n\n"
                    f"## Implementation Idea\n{sk.get('implementation_idea') or 'N/A'}\n\n"
                    f"## Notes\n{notes or sk.get('notes') or 'N/A'}\n"
                )
                obsidian_path = None
                github_path = None
                supabase_update = {}

                if 'obsidian' in save_targets:
                    obsidian_key = os.getenv('OBSIDIAN_LOCAL_API_KEY', '')
                    if obsidian_key:
                        obs_file = f'Agent Skills/Radar/{date_str}-{safe_title}.md'
                        try:
                            obs_url = f'http://127.0.0.1:27123/vault/{urllib.parse.quote(obs_file)}'
                            obs_req = urllib.request.Request(obs_url, method='PUT')
                            obs_req.add_header('Authorization', f'Bearer {obsidian_key}')
                            obs_req.add_header('Content-Type', 'text/markdown')
                            obs_data = md_content.encode('utf-8')
                            with urllib.request.urlopen(obs_req, data=obs_data, timeout=15) as r:
                                r.read()
                            obsidian_path = obs_file
                            supabase_update['obsidian_synced'] = True
                        except Exception:
                            pass

                if 'github' in save_targets:
                    gh_token = os.getenv('GITHUB_TOKEN', '')
                    if gh_token:
                        filename = f'{date_str}-{slug}.md'
                        gh_path = f'skills-radar/approved/{filename}'
                        gh_headers = {
                            'Authorization': f'Bearer {gh_token}',
                            'Accept': 'application/vnd.github+json',
                            'X-GitHub-Api-Version': '2022-11-28',
                            'User-Agent': 'radar-save-bot',
                        }
                        api_url = f'https://api.github.com/repos/{REPO}/contents/{gh_path}'
                        sha = None
                        try:
                            existing = fetch_json(f'{api_url}?ref=main', headers=gh_headers, timeout=20)
                            if isinstance(existing, dict) and existing.get('sha'):
                                sha = existing['sha']
                        except urllib.error.HTTPError as e:
                            if e.code != 404:
                                raise
                        commit_body = {
                            'message': f'feat(radar): add approved skill {safe_title} [{date_str}]',
                            'content': base64.b64encode(md_content.encode('utf-8')).decode('ascii'),
                            'branch': 'main',
                        }
                        if sha:
                            commit_body['sha'] = sha
                        fetch_json(api_url, headers=gh_headers, method='PUT', body=commit_body, timeout=30)
                        github_path = gh_path
                        supabase_update['github_synced'] = True

                if supabase_update:
                    patch_hdrs = _radar_sb_headers(prefer='return=minimal')
                    patch_url = f"{cfg['url']}/rest/v1/skill_discoveries?id=eq.{urllib.parse.quote(skill_id)}"
                    req = urllib.request.Request(patch_url, headers=patch_hdrs, method='PATCH')
                    data = json.dumps(supabase_update, ensure_ascii=False).encode('utf-8')
                    with urllib.request.urlopen(req, data=data, timeout=15) as r:
                        r.read()

                return json_response(self, 200, {
                    'ok': True,
                    'obsidian_path': obsidian_path,
                    'github_path': github_path,
                })
            except urllib.error.HTTPError as exc:
                body = exc.read().decode('utf-8', 'replace')[:1200]
                return json_response(self, 502, {'ok': False, 'error': f'API error {exc.code}', 'details': body})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        # ===== END RADAR POST ENDPOINTS =====

        if parsed.path == '/api/fixer/analyze':
            try:
                wf_json_str = (payload.get('workflowJson') or '').strip()
                if not wf_json_str:
                    return json_response(self, 400, {'ok': False, 'error': 'workflowJson is required'})
                try:
                    wf_obj = json.loads(wf_json_str)
                except Exception:
                    return json_response(self, 400, {'ok': False, 'error': 'workflowJson is not valid JSON'})
                if not isinstance(wf_obj, dict):
                    return json_response(self, 400, {'ok': False, 'error': 'workflowJson must be a JSON object'})

                problem = (payload.get('problemDescription') or '').strip()
                comments = (payload.get('comments') or '').strip()
                notes = (payload.get('notes') or '').strip()
                model = (payload.get('model') or 'anthropic/claude-opus-4.7').strip()
                wf_name = (payload.get('workflowName') or wf_obj.get('name') or 'unnamed').strip()
                site_url = (payload.get('siteUrl') or '').strip()
                suspected_node = (payload.get('suspectedNode') or '').strip()
                target_id = (payload.get('targetWorkflowId') or '').strip()

                # Save backup
                import datetime
                date_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', wf_name)[:40]
                backup_dir = Path(f'/tmp/fixer_backups/{date_str}_{safe_name}')
                try:
                    backup_dir.mkdir(parents=True, exist_ok=True)
                    (backup_dir / 'original.json').write_text(json.dumps(wf_obj, indent=2, ensure_ascii=False), encoding='utf-8')
                except Exception:
                    pass

                base, headers = prompt_headers()
                if not headers:
                    return json_response(self, 503, {'ok': False, 'error': 'OPENROUTER_API_KEY is not configured'})

                system_prompt = (
                    "You are an expert N8N workflow debugger and repair engineer. Analyze the provided N8N workflow JSON and fix all issues.\n\n"
                    "Your analysis must cover:\n"
                    "- Malformed or disconnected nodes\n"
                    "- Broken node connections/references\n"
                    "- Invalid N8N expressions ({{ }}) with syntax errors\n"
                    "- Credential misconfiguration patterns (wrong IDs, missing credentials)\n"
                    "- Loop traps (SplitInBatches nodes that never reach 'done' output)\n"
                    "- Dead-end execution paths (nodes with no output connections)\n"
                    "- Wait nodes with missing webhook configurations\n"
                    "- Code nodes with JavaScript errors or corrupted output structures\n"
                    "- HTTP Request nodes with authentication issues (401, 403 patterns)\n"
                    "- Merge node input count mismatches\n"
                    "- Schedule triggers with invalid cron expressions\n"
                    "- Missing required node parameters\n\n"
                    "Use the problem description, comments, notes, and screenshots context provided.\n"
                    "Preserve original workflow intent. Fix only what is necessary.\n"
                    "Return a JSON response in this EXACT structure (no markdown, raw JSON only):\n"
                    "{\n"
                    '  "issue_summary": "...",\n'
                    '  "root_cause": "...",\n'
                    '  "changes_made": ["change 1", "change 2"],\n'
                    '  "confidence": 0.85,\n'
                    '  "warnings": ["warning if any"],\n'
                    '  "fixed_workflow": { ...complete corrected N8N workflow JSON... }\n'
                    "}"
                )

                context_parts = [f"WORKFLOW JSON:\n{json.dumps(wf_obj, indent=2)}"]
                if problem:
                    context_parts.append(f"\nPROBLEM DESCRIPTION:\n{problem}")
                if comments:
                    context_parts.append(f"\nCOMMENTS:\n{comments}")
                if notes:
                    context_parts.append(f"\nNOTES:\n{notes}")
                if suspected_node:
                    context_parts.append(f"\nSUSPECTED NODE: {suspected_node}")
                if site_url:
                    context_parts.append(f"\nSITE URL: {site_url}")
                if target_id:
                    context_parts.append(f"\nTARGET WORKFLOW ID: {target_id}")
                user_message = '\n'.join(context_parts)

                body = {
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_message},
                    ],
                    'max_tokens': 32000,
                }
                resp = fetch_json(f'{base}/chat/completions', headers=headers, method='POST', body=body, timeout=300)
                raw_content = ''
                choices = resp.get('choices') or []
                if choices:
                    msg = choices[0].get('message') or {}
                    raw_content = msg.get('content') or ''
                if isinstance(raw_content, list):
                    raw_content = ''.join(p.get('text', '') for p in raw_content if isinstance(p, dict))
                raw_content = str(raw_content).strip()

                # Strip markdown code fences if present
                if raw_content.startswith('```'):
                    raw_content = re.sub(r'^```[a-z]*\n?', '', raw_content)
                    raw_content = re.sub(r'\n?```$', '', raw_content.rstrip())

                try:
                    result = json.loads(raw_content)
                except Exception:
                    # Try to extract JSON from response
                    m = re.search(r'\{.*\}', raw_content, re.DOTALL)
                    if m:
                        try:
                            result = json.loads(m.group(0))
                        except Exception:
                            return json_response(self, 502, {'ok': False, 'error': 'Model returned non-JSON response', 'raw': raw_content[:2000]})
                    else:
                        return json_response(self, 502, {'ok': False, 'error': 'Model returned non-JSON response', 'raw': raw_content[:2000]})

                fixed_wf = result.get('fixed_workflow') or wf_obj
                fixed_str = json.dumps(fixed_wf, indent=2, ensure_ascii=False)

                # Save fixed backup
                try:
                    (backup_dir / 'fixed.json').write_text(fixed_str, encoding='utf-8')
                except Exception:
                    pass

                return json_response(self, 200, {
                    'ok': True,
                    'issueSummary': result.get('issue_summary', ''),
                    'rootCause': result.get('root_cause', ''),
                    'changesMade': result.get('changes_made', []),
                    'confidence': result.get('confidence', 0),
                    'warnings': result.get('warnings', []),
                    'fixedWorkflowJson': fixed_str,
                    'backupDir': str(backup_dir),
                })
            except urllib.error.HTTPError as exc:
                body_bytes = exc.read().decode('utf-8', 'replace')[:1500]
                return json_response(self, 502, {'ok': False, 'error': f'Model API error {exc.code}', 'details': body_bytes})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/fixer/save':
            try:
                import datetime
                wf_name = (payload.get('workflowName') or 'unnamed').strip()
                wf_id = (payload.get('workflowId') or '').strip()
                site_url = (payload.get('siteUrl') or '').strip()
                problem = (payload.get('problemDescription') or '').strip()
                comments_txt = (payload.get('comments') or '').strip()
                notes_txt = (payload.get('notes') or '').strip()
                model_used = (payload.get('modelUsed') or '').strip()
                issue_summary = (payload.get('issueSummary') or '').strip()
                root_cause = (payload.get('rootCause') or '').strip()
                changes_made = payload.get('changesMade') or []
                warnings_list = payload.get('warnings') or []
                confidence = payload.get('confidence') or 0
                deploy_status = (payload.get('deployStatus') or 'pending').strip()
                original_json = payload.get('originalJson')
                fixed_json = payload.get('fixedJson')

                supabase_id = None
                supabase_url = (os.getenv('SUPABASE_URL') or '').rstrip('/')
                supabase_key = (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_ANON_KEY') or '').strip()
                if supabase_url and supabase_key:
                    row = {
                        'workflow_name': wf_name,
                        'workflow_id': wf_id or None,
                        'site_url': site_url or None,
                        'problem_description': problem or None,
                        'comments': comments_txt or None,
                        'notes': notes_txt or None,
                        'model_used': model_used or None,
                        'issue_summary': issue_summary or None,
                        'root_cause': root_cause or None,
                        'changes_made': json.dumps(changes_made) if changes_made else None,
                        'original_json': original_json,
                        'fixed_json': fixed_json,
                        'deploy_status': deploy_status,
                        'confidence_score': confidence,
                    }
                    try:
                        sb_headers = {
                            'apikey': supabase_key,
                            'Authorization': f'Bearer {supabase_key}',
                            'Content-Type': 'application/json',
                            'Prefer': 'return=representation',
                        }
                        sb_result = fetch_json(f'{supabase_url}/rest/v1/n8n_fixer_records', headers=sb_headers, method='POST', body=row, timeout=30)
                        if isinstance(sb_result, list) and sb_result:
                            supabase_id = sb_result[0].get('id')
                    except Exception:
                        pass  # graceful fail

                # Save to Obsidian
                obsidian_path = None
                obsidian_key = os.getenv('OBSIDIAN_LOCAL_API_KEY', '')
                date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '-', wf_name)[:50]
                obs_file = f'HTML REDESIGN/n8n-fixer/{date_str}-{safe_name}.md'

                changes_md = '\n'.join(f'- {c}' for c in changes_made) if changes_made else '- None'
                warnings_md = '\n'.join(f'- {w}' for w in warnings_list) if warnings_list else '- None'
                md_content = (
                    f"# N8N Workflow Fixer Record — {wf_name} — {date_str}\n\n"
                    f"**Workflow:** {wf_name}  \n"
                    f"**Workflow ID:** {wf_id or 'N/A'}  \n"
                    f"**Site URL:** {site_url or 'N/A'}  \n"
                    f"**Date:** {date_str}  \n"
                    f"**Model Used:** {model_used or 'N/A'}  \n"
                    f"**Confidence:** {round(float(confidence)*100, 1)}%  \n"
                    f"**Deploy Status:** {deploy_status}  \n\n"
                    f"## Problem Description\n{problem or 'N/A'}\n\n"
                    f"## Comments\n{comments_txt or 'N/A'}\n\n"
                    f"## Notes\n{notes_txt or 'N/A'}\n\n"
                    f"## Issue Summary\n{issue_summary or 'N/A'}\n\n"
                    f"## Root Cause\n{root_cause or 'N/A'}\n\n"
                    f"## Changes Made\n{changes_md}\n\n"
                    f"## Warnings\n{warnings_md}\n"
                )

                if obsidian_key:
                    try:
                        obs_url = f'http://127.0.0.1:27123/vault/{urllib.parse.quote(obs_file)}'
                        obs_req = urllib.request.Request(obs_url, method='PUT')
                        obs_req.add_header('Authorization', f'Bearer {obsidian_key}')
                        obs_req.add_header('Content-Type', 'text/markdown')
                        obs_data = md_content.encode('utf-8')
                        with urllib.request.urlopen(obs_req, data=obs_data, timeout=15) as r:
                            r.read()
                        obsidian_path = obs_file
                    except Exception:
                        pass

                return json_response(self, 200, {'ok': True, 'supabaseId': supabase_id, 'obsidianPath': obsidian_path})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/fixer/deploy':
            fixed_json_str = (payload.get('fixedWorkflowJson') or '').strip()
            target_workflow_id = (payload.get('targetWorkflowId') or '').strip()
            if not fixed_json_str:
                return json_response(self, 400, {'ok': False, 'error': 'fixedWorkflowJson is required'})
            if not os.getenv('N8N_API_KEY'):
                return json_response(self, 503, {'ok': False, 'error': 'N8N_API_KEY is not configured'})
            try:
                source = json.loads(fixed_json_str)
            except Exception:
                return json_response(self, 400, {'ok': False, 'error': 'fixedWorkflowJson is not valid JSON'})
            if not isinstance(source, dict):
                return json_response(self, 400, {'ok': False, 'error': 'fixedWorkflowJson must be an object'})
            if not target_workflow_id:
                target_workflow_id = source.get('id') or ''
            if not target_workflow_id:
                return json_response(self, 400, {'ok': False, 'error': 'targetWorkflowId is required (no id in JSON)'})
            try:
                import datetime
                base = os.getenv('N8N_BASE_URL', DEFAULT_N8N_BASE).rstrip('/')
                headers = n8n_headers()
                live = fetch_json(f'{base}/api/v1/workflows/{target_workflow_id}', headers=headers)
                update_payload = build_workflow_payload(source, live)
                updated = fetch_json(f'{base}/api/v1/workflows/{target_workflow_id}', headers=headers, method='PUT', body=update_payload, timeout=120)
                return json_response(self, 200, {
                    'ok': True,
                    'workflowId': target_workflow_id,
                    'workflowName': updated.get('name') or live.get('name'),
                    'deployedAt': datetime.datetime.utcnow().isoformat() + 'Z',
                })
            except urllib.error.HTTPError as exc:
                body_bytes = exc.read().decode('utf-8', 'replace')[:1500]
                return json_response(self, 502, {'ok': False, 'error': f'n8n API error {exc.code}', 'details': body_bytes})
            except Exception as exc:
                return json_response(self, 500, {'ok': False, 'error': str(exc)})

        if parsed.path == '/api/fixer/history':
            try:
                supabase_url = (os.getenv('SUPABASE_URL') or '').rstrip('/')
                supabase_key = (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_ANON_KEY') or '').strip()
                if not (supabase_url and supabase_key):
                    return json_response(self, 200, {'ok': True, 'records': []})
                sb_headers = {
                    'apikey': supabase_key,
                    'Authorization': f'Bearer {supabase_key}',
                    'Accept': 'application/json',
                }
                url = f'{supabase_url}/rest/v1/n8n_fixer_records?select=id,created_at,workflow_name,workflow_id,site_url,model_used,confidence_score,deploy_status,issue_summary&order=created_at.desc&limit=10'
                rows = fetch_json(url, headers=sb_headers, timeout=20)
                if not isinstance(rows, list):
                    rows = []
                return json_response(self, 200, {'ok': True, 'records': rows})
            except Exception as exc:
                return json_response(self, 200, {'ok': True, 'records': [], 'warning': str(exc)})

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


# ===== DAILY SKILLS RADAR — helper functions =====

def supabase_radar_config():
    url = (os.getenv('SUPABASE_URL') or '').strip().rstrip('/')
    key = (
        (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or '').strip()
        or (os.getenv('SUPABASE_ANON_KEY') or '').strip()
        or (os.getenv('SUPABASE_API_KEY') or '').strip()
    )
    return {'url': url, 'key': key, 'configured': bool(url and key)}


def _radar_sb_headers(prefer=None):
    cfg = supabase_radar_config()
    if not cfg['configured']:
        return None
    h = {
        'apikey': cfg['key'],
        'Authorization': f"Bearer {cfg['key']}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    if prefer:
        h['Prefer'] = prefer
    return h


def _save_skill_to_supabase(skill_dict):
    cfg = supabase_radar_config()
    if not cfg['configured']:
        return None
    hdrs = _radar_sb_headers(prefer='return=representation')
    url = f"{cfg['url']}/rest/v1/skill_discoveries"
    try:
        result = fetch_json(url, headers=hdrs, method='POST', body=skill_dict, timeout=15)
        if isinstance(result, list) and result:
            return result[0].get('id')
        if isinstance(result, dict):
            return result.get('id')
    except Exception:
        pass
    return None


def _update_radar_run(run_id, updates_dict):
    cfg = supabase_radar_config()
    if not cfg['configured'] or not run_id:
        return
    hdrs = _radar_sb_headers()
    url = f"{cfg['url']}/rest/v1/radar_runs?id=eq.{urllib.parse.quote(str(run_id))}"
    try:
        fetch_json(url, headers=hdrs, method='PATCH', body=updates_dict, timeout=15)
    except Exception:
        pass


def _fetch_x_sources(max_results=50):
    """Fetch URLs from user's X/Twitter timeline and bookmarks using Bearer Token.
    Returns a list of source dicts compatible with RADAR_SOURCES format.
    Requires X_BEARER_TOKEN env var. Deduplicates by URL."""
    bearer = (os.getenv('X_BEARER_TOKEN') or '').strip()
    if not bearer:
        return []

    sources = []
    seen_urls = set()

    def _x_headers():
        return {
            'Authorization': f'Bearer {bearer}',
            'Content-Type': 'application/json',
        }

    def _extract_urls_from_tweets(tweets):
        found = []
        for tweet in (tweets or []):
            entities = tweet.get('entities') or {}
            for url_obj in (entities.get('urls') or []):
                expanded = url_obj.get('expanded_url', '')
                # Skip t.co redirects, twitter.com/x.com self-links, short internal links
                if not expanded:
                    continue
                if 'twitter.com' in expanded or 'x.com/i/' in expanded:
                    continue
                if len(expanded) < 15:
                    continue
                # Prefer GitHub, docs, README, official sites
                title = url_obj.get('title') or url_obj.get('display_url') or expanded
                desc = url_obj.get('description') or ''
                found.append({'url': expanded, 'title': title, 'description': desc})
        return found

    def _quality_score(url, title, description):
        score = 0.7  # base for X-sourced links
        u = url.lower()
        t = (title + ' ' + description).lower()
        # Boost for high-quality domains
        if 'github.com' in u:
            score += 0.15
        if any(d in u for d in ['docs.', 'documentation', 'readme', 'arxiv.org', 'huggingface.co', 'openai.com', 'anthropic.com']):
            score += 0.1
        if any(k in t for k in ['agent', 'llm', 'ai', 'automation', 'n8n', 'workflow', 'tool', 'framework', 'sdk', 'api', 'mcp']):
            score += 0.05
        if any(k in u for k in ['awesome', 'tutorial', 'guide', 'cookbook', 'playbook']):
            score += 0.05
        return min(round(score, 2), 0.99)

    # Step 1: Get the authenticated user ID
    try:
        me = fetch_json('https://api.twitter.com/2/users/me', headers=_x_headers(), timeout=15)
        user_id = (me.get('data') or {}).get('id')
        if not user_id:
            return []
    except Exception:
        return []

    # Step 2: Fetch home timeline (recent tweets from accounts user follows)
    try:
        params = f'max_results={min(max_results, 100)}&tweet.fields=entities,created_at&expansions=author_id'
        timeline = fetch_json(
            f'https://api.twitter.com/2/users/{user_id}/timelines/reverse_chronological?{params}',
            headers=_x_headers(), timeout=20
        )
        for item in _extract_urls_from_tweets((timeline.get('data') or [])):
            url = item['url']
            if url not in seen_urls:
                seen_urls.add(url)
                sources.append({
                    'url': url,
                    'title': item['title'] or url,
                    'type': 'x_timeline',
                    'quality': _quality_score(url, item['title'], item['description']),
                    'x_source': 'timeline',
                })
    except Exception:
        pass

    # Step 3: Fetch bookmarks (things the user saved)
    try:
        params = f'max_results={min(max_results, 100)}&tweet.fields=entities,created_at'
        bookmarks = fetch_json(
            f'https://api.twitter.com/2/users/{user_id}/bookmarks?{params}',
            headers=_x_headers(), timeout=20
        )
        for item in _extract_urls_from_tweets((bookmarks.get('data') or [])):
            url = item['url']
            if url not in seen_urls:
                seen_urls.add(url)
                # Bookmarks are higher quality — user intentionally saved them
                base_q = _quality_score(url, item['title'], item['description'])
                sources.append({
                    'url': url,
                    'title': item['title'] or url,
                    'type': 'x_bookmark',
                    'quality': min(base_q + 0.05, 0.99),
                    'x_source': 'bookmark',
                })
    except Exception:
        pass

    # Step 4: Fetch user's own likes (things user liked)
    try:
        params = f'max_results={min(max_results, 100)}&tweet.fields=entities,created_at'
        likes = fetch_json(
            f'https://api.twitter.com/2/users/{user_id}/liked_tweets?{params}',
            headers=_x_headers(), timeout=20
        )
        for item in _extract_urls_from_tweets((likes.get('data') or [])):
            url = item['url']
            if url not in seen_urls:
                seen_urls.add(url)
                sources.append({
                    'url': url,
                    'title': item['title'] or url,
                    'type': 'x_like',
                    'quality': _quality_score(url, item['title'], item['description']),
                    'x_source': 'like',
                })
    except Exception:
        pass

    # Filter out low-quality sources (below 0.65) and non-fetchable URLs
    filtered = []
    for s in sources:
        if s['quality'] < 0.65:
            continue
        u = s['url'].lower()
        # Skip non-content URLs
        if any(skip in u for skip in ['youtube.com/watch', 'youtu.be', 'instagram.com', 'tiktok.com', 'facebook.com', 'linkedin.com/in/']):
            continue
        filtered.append(s)

    return filtered


def _get_recent_skill_titles(limit=200):
    cfg = supabase_radar_config()
    if not cfg['configured']:
        return []
    hdrs = _radar_sb_headers()
    url = f"{cfg['url']}/rest/v1/skill_discoveries?select=title&order=created_at.desc&limit={limit}"
    try:
        rows = fetch_json(url, headers=hdrs, timeout=15)
        if isinstance(rows, list):
            return [r.get('title', '') for r in rows if r.get('title')]
    except Exception:
        pass
    return []


def _is_duplicate_skill(title, existing_titles_list):
    def normalize(t):
        t = t.lower()
        t = re.sub(r'[^a-z0-9\s]', ' ', t)
        return set(t.split())
    words_a = normalize(title)
    if not words_a:
        return False
    for existing in existing_titles_list:
        words_b = normalize(existing)
        if not words_b:
            continue
        intersection = words_a & words_b
        union = words_a | words_b
        if union and len(intersection) / len(union) > 0.8:
            return True
    return False


def _extract_skills_from_source(source, content_text, topics=None):
    base, headers = prompt_headers()
    if not headers:
        return []
    content_trimmed = content_text[:8000]
    topics_str = ', '.join(topics) if topics else ''
    topics_instruction = (
        f'\nFocus on skills related to these topics: {topics_str}. '
        f'Prioritize results matching these topics. '
        f'Add a "topics" field to each skill with matching topics from this list.\n'
    ) if topics_str else ''
    system_prompt = (
        "You are an expert agent skill analyst. Extract actionable skills from the provided source content.\n"
        "For each skill, return ONLY a JSON array (no markdown, no explanation) with objects containing:\n"
        "- title: short skill name (5-60 chars)\n"
        "- summary: one clear sentence what this skill enables (max 150 chars)\n"
        "- category: one of: automation, coding, seo, ai_agents, scraping, data, prompting, integration, research, ui_ux, n8n, memory, other\n"
        "- skill_type: one of: tool_integration, workflow_pattern, api_capability, framework, prompt_pattern, automation_recipe, knowledge_artifact\n"
        "- target_agents: array of relevant agents from: [\"Hermes\", \"Claude Code\", \"Manus\", \"CTO\", \"CEO\", \"Prompt Studio\", \"General\"]\n"
        "- usefulness_score: 0.0 to 1.0 float\n"
        "- implementation_idea: one sentence how to implement or use this skill\n"
        "- topics: array of matching topic strings from the focus list (empty array if none match)\n\n"
        "Return 3-8 skills maximum. Only include genuinely useful, actionable skills. Skip obvious/generic ones.\n"
        + topics_instruction
        + f"Source: {source['title']} ({source['type']})"
    )
    body = {
        'model': 'anthropic/claude-sonnet-4.6',
        'max_tokens': 2048,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Extract skills from this content:\n\n{content_trimmed}"},
        ],
    }
    try:
        resp = fetch_json(f'{base}/chat/completions', headers=headers, method='POST', body=body, timeout=60)
        raw = resp.get('choices', [{}])[0].get('message', {}).get('content', '')
        raw = raw.strip()
        # Strip markdown fences if present
        if raw.startswith('```'):
            raw = re.sub(r'^```[a-z]*\n?', '', raw)
            raw = re.sub(r'\n?```$', '', raw)
        skills = json.loads(raw)
        if isinstance(skills, list):
            return skills
    except Exception:
        pass
    return []


def _run_radar_discovery(config=None):
    import datetime as _dt
    global _radar_state
    _radar_state['status'] = 'running'
    _radar_state['progress'] = 0
    _radar_state['skills_found'] = 0
    _radar_state['sources_done'] = 0
    _radar_state['last_error'] = None
    _radar_state['started_at'] = _dt.datetime.utcnow().isoformat() + 'Z'
    _radar_state['finished_at'] = None
    _radar_state['stage'] = 'Initializing'

    sources = list(RADAR_SOURCES)

    # Fetch dynamic sources from X/Twitter (timeline, bookmarks, likes)
    _radar_state['stage'] = 'Fetching X sources'
    try:
        x_sources = _fetch_x_sources(max_results=50)
        if x_sources:
            # Dedupe against static RADAR_SOURCES urls
            static_urls = {s['url'] for s in RADAR_SOURCES}
            new_x = [s for s in x_sources if s['url'] not in static_urls]
            sources = sources + new_x
            _radar_state['x_sources_found'] = len(new_x)
    except Exception as _xe:
        _radar_state['x_sources_found'] = 0
        _radar_state['last_error'] = f'X fetch: {_xe}'

    if config and config.get('source_types'):
        types = config['source_types']
        # Keep x_timeline/x_bookmark/x_like if 'x' is in the filter, else apply strict filter
        if 'x' not in types:
            sources = [s for s in sources if s.get('type') in types]

    # Apply quality threshold filter
    quality_threshold = float((config or {}).get('quality_threshold') or 0.0)
    if quality_threshold > 0:
        sources = [s for s in sources if s.get('quality', 0) >= quality_threshold]

    _radar_state['sources_total'] = len(sources)
    run_id = None

    # Create radar_run record
    _radar_state['stage'] = 'Sources Queued'
    cfg = supabase_radar_config()
    if cfg['configured']:
        try:
            hdrs = _radar_sb_headers(prefer='return=representation')
            run_body = {
                'status': 'running',
                'sources_count': len(sources),
                'started_at': _radar_state['started_at'],
                'skills_found': 0,
                'skills_approved': 0,
                'errors': [],
            }
            result = fetch_json(f"{cfg['url']}/rest/v1/radar_runs", headers=hdrs, method='POST', body=run_body, timeout=15)
            if isinstance(result, list) and result:
                run_id = result[0].get('id')
            elif isinstance(result, dict):
                run_id = result.get('id')
            _radar_state['run_id'] = run_id
        except Exception as e:
            _radar_state['last_error'] = str(e)

    # Get existing titles for dedup
    _radar_state['stage'] = 'Fetching'
    existing_titles = _get_recent_skill_titles(limit=500)
    errors = []
    skills_found = 0

    for i, source in enumerate(sources):
        if _radar_state.get('paused'):
            import time as _time
            while _radar_state.get('paused'):
                _time.sleep(2)

        _radar_state['stage'] = f"Fetching {source['title']}"
        _radar_state['progress'] = int((i / len(sources)) * 60)

        try:
            content = fetch_text(source['url'], timeout=20)
        except Exception as e:
            errors.append({'source': source['title'], 'error': str(e)})
            _radar_state['sources_done'] = i + 1
            continue

        _radar_state['stage'] = f"Extracting Skills: {source['title']}"
        _radar_state['progress'] = int((i / len(sources)) * 60) + 5

        try:
            active_topics = list((_radar_state.get('topics') or []) + (_radar_state.get('custom_topics') or []))
            skills = _extract_skills_from_source(source, content, topics=active_topics if active_topics else None)
        except Exception as e:
            errors.append({'source': source['title'], 'error': f'LLM error: {e}'})
            _radar_state['sources_done'] = i + 1
            continue

        _radar_state['stage'] = 'Deduplicating'
        for skill in skills:
            title = skill.get('title', '').strip()
            if not title:
                continue
            if _is_duplicate_skill(title, existing_titles):
                continue

            # Save to Supabase
            _radar_state['stage'] = 'Saving Results'
            import datetime as _dt2
            skill_row = {
                'title': title,
                'summary': skill.get('summary', ''),
                'category': skill.get('category', 'other'),
                'skill_type': skill.get('skill_type', 'knowledge_artifact'),
                'target_agents': skill.get('target_agents', ['General']),
                'usefulness_score': float(skill.get('usefulness_score', 0.5)),
                'implementation_idea': skill.get('implementation_idea', ''),
                'source_title': source['title'],
                'source_url': source['url'],
                'source_type': source['type'],
                'source_quality': source['quality'],
                'status': 'pending',
                'run_id': run_id,
                'supabase_synced': False,
                'github_path': None,
                'obsidian_path': None,
                'approval_notes': None,
                'matched_topics': skill.get('topics', []),
                'created_at': _dt2.datetime.utcnow().isoformat() + 'Z',
            }
            try:
                _save_skill_to_supabase(skill_row)
                existing_titles.append(title)
                skills_found += 1
                _radar_state['skills_found'] = skills_found
            except Exception as e:
                errors.append({'source': source['title'], 'error': f'Save error: {e}'})

        _radar_state['sources_done'] = i + 1
        _radar_state['progress'] = int(((i + 1) / len(sources)) * 90)

    import datetime as _dt3
    finished_at = _dt3.datetime.utcnow().isoformat() + 'Z'
    _radar_state['status'] = 'done'
    _radar_state['finished_at'] = finished_at
    _radar_state['progress'] = 100
    _radar_state['stage'] = 'Complete'

    if run_id:
        _update_radar_run(run_id, {
            'status': 'completed',
            'finished_at': finished_at,
            'skills_found': skills_found,
            'errors': errors,
        })

    # Send email digest after every run
    _radar_state['stage'] = 'Sending email digest'
    try:
        email_result = _send_radar_email_digest(
            skills_found_count=skills_found,
            run_id=run_id,
            errors=errors,
        )
        _radar_state['last_email'] = email_result
    except Exception as _ee:
        _radar_state['last_email'] = {'ok': False, 'error': str(_ee)}

    _radar_state['stage'] = 'Complete'


def _send_radar_email_digest(skills_found_count, run_id=None, errors=None):
    """Send a clean HTML digest email via Resend API after each discovery run."""
    import datetime as _dt
    api_key  = (os.getenv('RESEND_API_KEY') or '').strip()
    to_addr  = (os.getenv('RADAR_EMAIL_TO')  or 'service@maximo-seo.com').strip()
    from_addr= (os.getenv('RADAR_EMAIL_FROM') or 'onboarding@resend.dev').strip()
    if not api_key:
        return {'ok': False, 'error': 'RESEND_API_KEY not configured'}

    now_str = _dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    date_str = _dt.datetime.utcnow().strftime('%A, %d %B %Y')

    # Fetch the latest pending skills for this run
    skills_rows = []
    cfg = supabase_radar_config()
    if cfg['configured']:
        try:
            hdrs = _radar_sb_headers()
            url = f"{cfg['url']}/rest/v1/skill_discoveries?select=*&status=eq.pending&order=created_at.desc&limit=30"
            if run_id:
                url += f"&run_id=eq.{urllib.parse.quote(str(run_id))}"
            rows = fetch_json(url, headers=hdrs, timeout=15)
            if isinstance(rows, list):
                skills_rows = rows
        except Exception:
            pass

    # X sources count
    x_count = sum(1 for s in skills_rows if (s.get('source_type') or '').startswith('x_'))

    # ── Category breakdown
    from collections import Counter
    cat_counts = Counter(s.get('category', 'other') for s in skills_rows)
    cat_rows_html = ''.join(
        f'<tr><td style="padding:6px 12px;color:#94a3b8;font-size:13px">{cat}</td>'
        f'<td style="padding:6px 12px;color:#e2e8f0;font-size:13px;font-weight:700;text-align:right">{cnt}</td></tr>'
        for cat, cnt in cat_counts.most_common()
    )

    # ── Skill cards HTML (top 20)
    type_labels = {
        'github_repo': 'GitHub', 'awesome_list': 'Awesome List',
        'x_timeline': 'X Timeline', 'x_bookmark': 'X Bookmark',
        'x_like': 'X Like', 'official_docs': 'Docs',
    }
    type_colors = {
        'github_repo': '#22c55e', 'awesome_list': '#f59e0b',
        'x_timeline': '#60a5fa', 'x_bookmark': '#3b82f6',
        'x_like': '#f9a8d4', 'official_docs': '#a78bfa',
    }
    cat_icons = {
        'automation': '⚙️', 'coding': '💻', 'ai_agents': '🤖', 'seo': '🔍',
        'scraping': '🕷️', 'data': '📊', 'prompting': '💬', 'integration': '🔗',
        'n8n': '🔀', 'research': '🔬', 'ui_ux': '🎨', 'memory': '🧠', 'other': '📦',
    }

    def _esc(s):
        return str(s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

    skill_cards_html = ''
    for s in skills_rows[:20]:
        src_type  = s.get('source_type','')
        src_label = type_labels.get(src_type, src_type)
        src_color = type_colors.get(src_type, '#94a3b8')
        icon      = cat_icons.get(s.get('category','other'), '📦')
        score     = int(float(s.get('usefulness_score') or s.get('source_quality') or 0.5) * 100)
        agents    = ', '.join(s.get('target_agents') or ['General'])
        src_url   = _esc(s.get('source_url') or '#')
        src_title = _esc(s.get('source_title') or s.get('source_url') or '—')
        skill_cards_html += f'''
        <tr>
          <td style="padding:16px;border-bottom:1px solid #1e293b">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td width="36" valign="top" style="padding-right:12px">
                  <div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#312e81,#4c1d95);text-align:center;line-height:34px;font-size:16px">{icon}</div>
                </td>
                <td valign="top">
                  <div style="font-size:15px;font-weight:700;color:#e2e8f0;margin-bottom:4px">{_esc(s.get("title","Untitled"))}</div>
                  <div style="font-size:12px;color:#64748b;margin-bottom:6px">
                    <span style="display:inline-block;padding:2px 7px;border-radius:8px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);color:{src_color};font-weight:700;font-size:10px">{src_label}</span>
                    &nbsp;<a href="{src_url}" style="color:#a78bfa;text-decoration:none">{src_title}</a>
                  </div>
                  <div style="font-size:13px;color:#94a3b8;line-height:1.55;margin-bottom:8px">{_esc(s.get("summary",""))}</div>
                  <div style="font-size:11px;color:#64748b">
                    Agents: <span style="color:#c4b5fd">{_esc(agents)}</span>
                    &nbsp;·&nbsp; Score: <span style="color:#e2e8f0;font-weight:700">{score}%</span>
                    {("&nbsp;·&nbsp; <span style='color:#94a3b8'>" + _esc(s.get("implementation_idea","")) + "</span>") if s.get("implementation_idea") else ""}
                  </div>
                </td>
                <td width="80" valign="top" style="text-align:right">
                  <a href="https://html-redesign-dashboard.maximo-seo.ai/#radar"
                     style="display:inline-block;padding:6px 12px;border-radius:8px;background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;font-size:11px;font-weight:700;text-decoration:none">Review</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>'''

    if not skill_cards_html:
        skill_cards_html = '<tr><td style="padding:24px;text-align:center;color:#64748b;font-size:13px">No new skill candidates found this run.</td></tr>'

    # ── Error rows
    error_section = ''
    if errors:
        err_rows = ''.join(
            f'<tr><td style="padding:4px 0;font-size:12px;color:#f87171">⚠ {_esc(e.get("source","?"))}: {_esc(e.get("error",""))}</td></tr>'
            for e in (errors or [])[:5]
        )
        error_section = f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:24px;background:#1e1b4b;border-radius:10px;overflow:hidden">
          <tr><td style="padding:12px 16px;font-size:12px;font-weight:700;color:#f87171;border-bottom:1px solid #312e81">⚠ Errors ({len(errors)})</td></tr>
          {err_rows}
        </table>'''

    # ── Full HTML email
    html_body = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#0f172a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0f172a;padding:32px 16px">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">

  <!-- Header -->
  <tr><td style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:16px 16px 0 0;padding:28px 32px">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td>
          <div style="font-size:11px;font-weight:700;color:#7c3aed;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Maximo SEO · Daily Radar</div>
          <div style="font-size:24px;font-weight:800;color:#f1f5f9">📡 Skills Radar Digest</div>
          <div style="font-size:13px;color:#94a3b8;margin-top:6px">{date_str} · {now_str}</div>
        </td>
        <td align="right" valign="top">
          <a href="https://html-redesign-dashboard.maximo-seo.ai/#radar"
             style="display:inline-block;padding:10px 20px;border-radius:10px;background:#7c3aed;color:#fff;font-size:13px;font-weight:700;text-decoration:none">Open Dashboard →</a>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- Stats bar -->
  <tr><td style="background:#1e293b;padding:20px 32px">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="text-align:center;border-right:1px solid #334155">
          <div style="font-size:28px;font-weight:800;color:#a78bfa">{skills_found_count}</div>
          <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.05em">New Skills</div>
        </td>
        <td style="text-align:center;border-right:1px solid #334155">
          <div style="font-size:28px;font-weight:800;color:#60a5fa">{x_count}</div>
          <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.05em">From X Feed</div>
        </td>
        <td style="text-align:center;border-right:1px solid #334155">
          <div style="font-size:28px;font-weight:800;color:#fbbf24">{len(cat_counts)}</div>
          <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.05em">Categories</div>
        </td>
        <td style="text-align:center">
          <div style="font-size:28px;font-weight:800;color:#4ade80">{len(errors or [])}</div>
          <div style="font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.05em">Errors</div>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- Category breakdown -->
  {'<tr><td style="background:#0f172a;padding:20px 32px"><div style="font-size:12px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px">By Category</div><table width="100%" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:10px;overflow:hidden">' + cat_rows_html + '</table></td></tr>' if cat_counts else ''}

  <!-- Skill cards heading -->
  <tr><td style="background:#0f172a;padding:20px 32px 8px">
    <div style="font-size:16px;font-weight:800;color:#e2e8f0">🎯 Top Discovered Skills</div>
    <div style="font-size:12px;color:#64748b;margin-top:4px">Showing up to 20 · Pending your review</div>
  </td></tr>

  <!-- Skill cards -->
  <tr><td style="background:#0f172a;padding:0 32px">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#1e293b;border-radius:12px;overflow:hidden">
      {skill_cards_html}
    </table>
  </td></tr>

  {error_section}

  <!-- CTA -->
  <tr><td style="background:#0f172a;padding:24px 32px;text-align:center">
    <a href="https://html-redesign-dashboard.maximo-seo.ai/#radar"
       style="display:inline-block;padding:14px 32px;border-radius:12px;background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;font-size:15px;font-weight:800;text-decoration:none">
      Review &amp; Approve Skills →
    </a>
    <div style="font-size:11px;color:#475569;margin-top:12px">Runs daily at 02:00 UTC · maximo-seo.com</div>
  </td></tr>

  <!-- Footer -->
  <tr><td style="background:#0f172a;border-top:1px solid #1e293b;padding:16px 32px;border-radius:0 0 16px 16px">
    <div style="font-size:11px;color:#475569;text-align:center">
      Daily Skills Radar · HTML Redesign Dashboard · Maximo SEO<br>
      Sent to {_esc(to_addr)} · {now_str}
    </div>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>'''

    # ── Plain text fallback
    text_lines = [
        f"DAILY SKILLS RADAR DIGEST — {date_str}",
        f"New Skills: {skills_found_count}  |  From X: {x_count}  |  Errors: {len(errors or [])}",
        "",
        "TOP DISCOVERED SKILLS:",
    ]
    for s in skills_rows[:20]:
        text_lines.append(f"  • {s.get('title','?')} [{s.get('category','?')}] — {s.get('summary','')[:80]}")
        if s.get('source_url'):
            text_lines.append(f"    Source: {s.get('source_url','')}")
    text_lines += ["", f"Review at: https://html-redesign-dashboard.maximo-seo.ai/#radar"]
    plain_text = '\n'.join(text_lines)

    subject = f"📡 Skills Radar: {skills_found_count} new skills found — {date_str}"

    # ── Send via Resend API
    payload = {
        'from': from_addr,
        'to': [to_addr],
        'subject': subject,
        'html': html_body,
        'text': plain_text,
    }
    try:
        req = urllib.request.Request(
            'https://api.resend.com/emails',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            resp = json.loads(r.read())
            return {'ok': True, 'email_id': resp.get('id'), 'to': to_addr}
    except urllib.error.HTTPError as exc:
        body_err = exc.read().decode('utf-8', 'replace')[:400]
        return {'ok': False, 'error': f'Resend HTTP {exc.code}: {body_err}'}
    except Exception as exc:
        return {'ok': False, 'error': str(exc)}


def _radar_scheduler_loop():
    import datetime as _dt
    import time as _time
    last_run_date = None
    while True:
        try:
            _time.sleep(60)
            if not _radar_state.get('schedule_enabled'):
                continue
            now = _dt.datetime.now()
            today = now.date()
            if now.hour == _radar_state.get('schedule_hour', 2) and last_run_date != today:
                if _radar_state['status'] != 'running':
                    last_run_date = today
                    _run_radar_discovery()
        except Exception:
            pass


threading.Thread(target=_radar_scheduler_loop, daemon=True).start()


def main():
    port = int(os.getenv('PORT', '8000'))
    server = ThreadingHTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f'listening on {port}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
