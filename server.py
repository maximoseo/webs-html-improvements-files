#!/usr/bin/env python3
import json
import mimetypes
import os
import posixpath
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


def improve_prompt_with_model(payload):
    draft = (payload.get('draftPrompt') or '').strip()
    if not draft:
        raise ValueError('Draft prompt is required')
    base, headers = prompt_headers()
    if not headers:
        raise RuntimeError('OPENAI_API_KEY or OPENROUTER_API_KEY is not configured')
    # Accept model override from the browser payload; fall back to env / default
    default_model = os.getenv('PROMPT_IMPROVER_MODEL', 'openai/gpt-5.4')
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
            })
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
