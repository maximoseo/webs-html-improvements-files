#!/usr/bin/env python3
"""Dashboard Features API — all 15-feature roadmap endpoints.
Import and call register_features_routes(server_class) from server.py.
"""
import json
import os
import datetime
import urllib.parse
from http.server import BaseHTTPRequestHandler

# Import from server.py helpers
import supabase_helper as sh

def _supa_available():
    return bool(os.environ.get('SUPABASE_URL', '').strip())


# ============================================================
# Integration helpers - connect existing ops with new features
# ============================================================

def log_existing_operation(table_name, action, changes=None, user_id=None, ip_address=None, record_id=None):
    """Log an existing operation to the audit log (if Supabase is available)."""
    try:
        import supabase_helper as sh
        sh.log_audit(table_name, action, changes, None, user_id, ip_address, record_id)
    except Exception:
        pass

def notify_operation(type_, title, message, link=''):
    """Create a notification for an operation."""
    try:
        import supabase_helper as sh
        sh.supa_insert('notifications', {
            'type': type_,
            'title': title,
            'message': message,
            'link': link,
        })
    except Exception:
        pass

def _json_resp(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    try:
        handler._r2_status = status
    except Exception:
        pass
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.send_header('Cache-Control', 'no-store, must-revalidate')
    handler.end_headers()
    handler.wfile.write(body)

def _read_body(handler):
    length = int(handler.headers.get('Content-Length', 0))
    if length > 0:
        raw = handler.rfile.read(length)
        try:
            return json.loads(raw.decode('utf-8'))
        except Exception:
            return {}
    return {}

def _user_from_handler(handler):
    """Extract user from auth cookie if available."""
    try:
        token = handler.headers.get('Cookie', '')
        for part in token.split(';'):
            part = part.strip()
            if part.startswith('dash_auth='):
                # Decode token to get user
                return 'admin'
    except Exception:
        pass
    return 'system'

def _client_ip(handler):
    try:
        for header in ('CF-Connecting-IP', 'X-Forwarded-For', 'X-Real-IP'):
            raw = (handler.headers.get(header) or '').strip()
            if raw:
                return raw.split(',')[0].strip()
    except Exception:
        pass
    try:
        return handler.client_address[0]
    except Exception:
        return 'unknown'

# ============================================================
# GET route handlers
# ============================================================

def handle_get(handler, parsed):
    path = parsed.path
    qs = urllib.parse.parse_qs(parsed.query)

    # --- Notifications ---
    if path == '/api/notifications':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'notifications': [], 'source': 'local'})
        limit = int((qs.get('limit') or ['50'])[0])
        offset = int((qs.get('offset') or ['0'])[0])
        unread = qs.get('unread', ['false'])[0].lower() == 'true'
        filters = {}
        if unread:
            filters['is_read'] = 'eq.false'
        result = sh.supa_select('notifications', order='created_at.desc', limit=limit, offset=offset, filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'notifications': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'notifications': result or []})

    # --- Unread count ---
    if path == '/api/notifications/unread-count':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'count': 0})
        result = sh.supa_select('notifications', select='count', filters={'is_read': 'eq.false'})
        count = len(result) if isinstance(result, list) else 0
        return _json_resp(handler, 200, {'ok': True, 'count': count})

    # --- Alert Rules ---
    if path == '/api/alert-rules':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'rules': []})
        result = sh.supa_select('alert_rules')
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'rules': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'rules': result or []})

    # --- Cost Summary ---
    if path == '/api/cost/summary':
        period = qs.get('period', ['daily'])[0]  # daily, weekly, monthly
        domain = qs.get('domain', [None])[0]
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'summary': {'total': 0, 'by_model': [], 'by_domain': []}})
        
        # Get cost data from agent_traces
        filters = {}
        if domain:
            filters['domain'] = f'eq.{domain}'
        result = sh.supa_select('agent_traces', select='agent_name,model_name,cost_usd,domain,created_at', filters=filters, limit=5000)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'summary': {'total': 0, 'by_model': [], 'by_domain': []}})
        
        traces = result or []
        total = sum(t.get('cost_usd', 0) for t in traces if isinstance(t, dict))
        
        # By model
        by_model = {}
        for t in traces:
            if not isinstance(t, dict):
                continue
            m = t.get('model_name', 'unknown')
            by_model.setdefault(m, {'model_name': m, 'total': 0, 'count': 0})
            by_model[m]['total'] += t.get('cost_usd', 0)
            by_model[m]['count'] += 1
        
        # By domain
        by_domain = {}
        for t in traces:
            if not isinstance(t, dict):
                continue
            d = t.get('domain', 'unknown')
            by_domain.setdefault(d, {'domain': d, 'total': 0, 'count': 0})
            by_domain[d]['total'] += t.get('cost_usd', 0)
            by_domain[d]['count'] += 1
        
        return _json_resp(handler, 200, {
            'ok': True,
            'summary': {
                'total': round(total, 4),
                'by_model': sorted(by_model.values(), key=lambda x: x['total'], reverse=True),
                'by_domain': sorted(by_domain.values(), key=lambda x: x['total'], reverse=True),
            }
        })

    # --- Cost by Model ---
    if path == '/api/cost/by-model':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'data': []})
        result = sh.supa_select('agent_traces', select='model_name,cost_usd,agent_name', limit=5000)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'data': []})
        by_model = {}
        for t in (result or []):
            if not isinstance(t, dict):
                continue
            m = t.get('model_name', 'unknown')
            by_model.setdefault(m, {'model_name': m, 'total': 0, 'count': 0, 'agents': set()})
            by_model[m]['total'] += t.get('cost_usd', 0)
            by_model[m]['count'] += 1
            by_model[m]['agents'].add(t.get('agent_name', 'unknown'))
        for m in by_model.values():
            m['agents'] = list(m['agents'])
        return _json_resp(handler, 200, {'ok': True, 'data': sorted(by_model.values(), key=lambda x: x['total'], reverse=True)})

    # --- Budget Limits ---
    if path == '/api/budget-limits':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'limits': []})
        result = sh.supa_select('budget_limits')
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'limits': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'limits': result or []})

    # --- Budget Check (auto-check all budgets) ---
    if path == '/api/budget/check':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'checked': 0, 'violations': []})
        try:
            violations = []
            for period in ['daily', 'weekly', 'monthly']:
                exceeded, limit, spent = sh.check_budget_exceeded(limit_type=period)
                if exceeded and limit:
                    violations.append({
                        'period': period,
                        'limit': limit.get('limit_usd', 0),
                        'spent': spent,
                        'domain': limit.get('domain'),
                        'action': limit.get('action', 'alert'),
                    })
                    sh.create_budget_notification(limit.get('domain'), limit, spent)
            return _json_resp(handler, 200, {'ok': True, 'checked': 1, 'violations': violations})
        except Exception as e:
            return _json_resp(handler, 500, {'ok': False, 'error': str(e)})


    # --- Budget Status (current spending vs limits) ---
    if path == '/api/budget/status':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'budgets': []})
        try:
            limits = sh.supa_select('budget_limits', filters={'is_active': 'eq.true'})
            if isinstance(limits, dict) and 'error' in limits:
                return _json_resp(handler, 200, {'ok': True, 'budgets': []})
            budgets = []
            for lim in (limits or []):
                period = lim.get('period', 'daily')
                domain = lim.get('domain')
                exceeded, _, spent = sh.check_budget_exceeded(domain=domain, limit_type=period)
                budgets.append({
                    'id': lim.get('id'),
                    'scope': lim.get('scope'),
                    'domain': domain,
                    'period': period,
                    'limit_usd': lim.get('limit_usd', 0),
                    'current_spent': spent,
                    'exceeded': exceeded,
                    'action': lim.get('action', 'alert'),
                    'remaining': max(0, lim.get('limit_usd', 0) - spent),
                })
            return _json_resp(handler, 200, {'ok': True, 'budgets': budgets})
        except Exception as e:
            return _json_resp(handler, 500, {'ok': False, 'error': str(e)})

    # --- Agent Traces ---
    if path == '/api/traces':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'traces': []})
        limit = int((qs.get('limit') or ['100'])[0])
        filters = {}
        run_id = qs.get('run_id', [None])[0]
        domain = qs.get('domain', [None])[0]
        if run_id:
            filters['run_id'] = f'eq.{run_id}'
        if domain:
            filters['domain'] = f'eq.{domain}'
        result = sh.supa_select('agent_traces', order='created_at.desc', limit=limit, filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'traces': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'traces': result or []})

    # Single trace by run_id
    if path.startswith('/api/traces/') and path.count('/') == 3:
        run_id = path.rsplit('/', 1)[-1]
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'traces': []})
        result = sh.supa_select('agent_traces', filters={'run_id': f'eq.{run_id}'}, order='step_order.asc', limit=50)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'traces': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'traces': result or []})

    # --- Template Versions ---
    if path == '/api/template-versions':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'versions': []})
        filters = {}
        domain = qs.get('domain', [None])[0]
        subdomain = qs.get('subdomain', [None])[0]
        if domain:
            filters['domain'] = f'eq.{domain}'
        if subdomain:
            filters['subdomain'] = f'eq.{subdomain}'
        result = sh.supa_select('template_versions', order='created_at.desc', limit=200, filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'versions': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'versions': result or []})

    # --- A/B Tests ---
    if path == '/api/ab-tests':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'tests': []})
        result = sh.supa_select('ab_tests', order='created_at.desc', limit=100)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'tests': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'tests': result or []})

    # --- Client Overview ---
    if path == '/api/client-overview':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'clients': []})
        result = sh.supa_select('v_client_overview', select='*')
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'clients': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'clients': result or []})

    if path.startswith('/api/client-overview/') and path.count('/') == 3:
        domain = path.rsplit('/', 1)[-1]
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'client': {}})
        result = sh.supa_select('agent_traces', filters={'domain': f'eq.{domain}'}, limit=500)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'client': {}, 'error': result['error']})
        traces = result or []
        total_cost = sum(t.get('cost_usd', 0) for t in traces if isinstance(t, dict))
        avg_score = sum(t.get('score', 0) for t in traces if isinstance(t, dict) and t.get('score')) / max(len([t for t in traces if isinstance(t, dict) and t.get('score')]), 1)
        return _json_resp(handler, 200, {
            'ok': True,
            'client': {
                'domain': domain,
                'total_runs': len(traces),
                'total_cost': round(total_cost, 4),
                'avg_score': round(avg_score, 1),
            }
        })

    # --- Batch Jobs ---
    if path == '/api/batch-jobs':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'jobs': []})
        status_filter = qs.get('status', [None])[0]
        filters = {}
        if status_filter:
            filters['status'] = f'eq.{status_filter}'
        result = sh.supa_select('batch_jobs', order='created_at.desc', limit=100, filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'jobs': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'jobs': result or []})

    # --- Reports ---
    if path == '/api/reports':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'reports': []})
        result = sh.supa_select('client_reports', order='created_at.desc', limit=50)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'reports': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'reports': result or []})

    # --- Report Schedules ---
    if path == '/api/report-schedules':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'schedules': []})
        result = sh.supa_select('report_schedules')
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'schedules': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'schedules': result or []})

    # --- Pipeline Schedules ---
    if path == '/api/pipeline-schedules':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'schedules': []})
        result = sh.supa_select('pipeline_schedules', order='created_at.desc', limit=100)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'schedules': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'schedules': result or []})

    # --- Notes ---
    if path == '/api/notes':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'notes': []})
        filters = {}
        entity_type = qs.get('entity_type', [None])[0]
        entity_id = qs.get('entity_id', [None])[0]
        if entity_type:
            filters['entity_type'] = f'eq.{entity_type}'
        if entity_id:
            filters['entity_id'] = f'eq.{entity_id}'
        result = sh.supa_select('notes', order='created_at.desc', limit=200, filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'notes': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'notes': result or []})

    # --- Audit Log ---
    if path == '/api/audit-log':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'events': []})
        limit = int((qs.get('limit') or ['100'])[0])
        offset = int((qs.get('offset') or ['0'])[0])
        action = qs.get('action', [None])[0]
        filters = {}
        if action:
            filters['action'] = f'eq.{action}'
        result = sh.supa_select('audit_log', order='created_at.desc', limit=limit, offset=offset, filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'events': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'events': result or []})

    # --- Feature Flags ---
    if path == '/api/feature-flags':
        if not _supa_available():
            return _json_resp(handler, 200, {'ok': True, 'flags': []})
        result = sh.supa_select('feature_flags', order='flag_name.asc')
        if isinstance(result, dict) and 'error' in result:
            return _json_resp(handler, 200, {'ok': True, 'flags': [], 'error': result['error']})
        return _json_resp(handler, 200, {'ok': True, 'flags': result or []})

    # --- Global Search ---
    if path == '/api/search':
        q = qs.get('q', [''])[0].strip().lower()
        if not q:
            return _json_resp(handler, 200, {'ok': True, 'results': []})
        
        results = []
        # Search domains from data.json
        try:
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
            if os.path.exists(data_path):
                with open(data_path, 'r') as f:
                    data = json.load(f)
                tree = data.get('tree', []) if isinstance(data, dict) else []
                domains = set()
                for item in tree:
                    p = item.get('path', '')
                    if p and '/' in p:
                        domain = p.split('/')[0]
                        if domain not in ('index.html', 'server.py', 'data.json'):
                            domains.add(domain)
                for d in sorted(domains):
                    if q in d.lower():
                        results.append({'type': 'domain', 'name': d, 'url': f'/{d}'})
        except Exception:
            pass
        
        # Search feature names
        features = [
            ('Notifications', 'notification center', '/notifications'),
            ('Cost Tracker', 'cost tracker budget', '/cost-tracker'),
            ('Traces', 'agent traces observability', '/traces'),
            ('Batch Jobs', 'batch operations bulk', '/batch-jobs'),
            ('Client Overview', 'client overview', '/client-overview'),
            ('A/B Testing', 'ab testing compare templates', '/ab-tests'),
            ('Reports', 'client reports automated', '/reports'),
            ('Schedules', 'pipeline scheduled runs', '/pipeline-schedules'),
            ('Settings', 'dashboard settings', '/settings'),
            ('Analytics', 'analytics statistics', '/analytics'),
        ]
        for name, keywords, url in features:
            if q in name.lower() or any(q in kw for kw in keywords.split()):
                results.append({'type': 'feature', 'name': name, 'url': url})
        
        return _json_resp(handler, 200, {'ok': True, 'results': results[:50]})

    # --- Enhanced Health Check ---
    if path == '/api/health/enhanced':
        flags = []
        if _supa_available():
            flags = sh.supa_select('feature_flags') or []
        return _json_resp(handler, 200, {
            'ok': True,
            'supabase_connected': _supa_available(),
            'feature_flags': {f['flag_name']: f['is_enabled'] for f in flags} if isinstance(flags, list) else {},
            'timestamp': datetime.datetime.utcnow().isoformat(),
        })

    return None  # Not handled

# ============================================================
# POST route handlers
# ============================================================

def handle_post(handler, parsed, payload):
    path = parsed.path

    # --- Create Notification ---
    if path == '/api/notifications':
        payload = payload or {}
        note = {
            'type': payload.get('type', 'info'),
            'title': payload.get('title', ''),
            'message': payload.get('message', ''),
            'link': payload.get('link', ''),
            'is_read': False,
        }
        if _supa_available():
            result = sh.supa_insert('notifications', note)
            if isinstance(result, list) and len(result) > 0:
                return _json_resp(handler, 201, {'ok': True, 'notification': result[0]})
            return _json_resp(handler, 500, {'ok': False, 'error': 'Failed to insert', 'detail': result})
        return _json_resp(handler, 201, {'ok': True, 'notification': note})

    # --- Mark Read ---
    if path == '/api/notifications/mark-read':
        payload = payload or {}
        note_id = payload.get('id')
        if not note_id:
            return _json_resp(handler, 400, {'ok': False, 'error': 'id required'})
        if _supa_available():
            result = sh.supa_update('notifications', 'id', note_id, {'is_read': True})
            if isinstance(result, list) and len(result) > 0:
                return _json_resp(handler, 200, {'ok': True, 'notification': result[0]})
            return _json_resp(handler, 500, {'ok': False, 'error': 'Update failed'})
        return _json_resp(handler, 200, {'ok': True})

    # --- Mark All Read ---
    if path == '/api/notifications/mark-all-read':
        if _supa_available():
            result = sh.supa_select('notifications', select='id', filters={'is_read': 'eq.false'})
            if isinstance(result, list):
                for n in result:
                    sh.supa_update('notifications', 'id', n['id'], {'is_read': True})
            return _json_resp(handler, 200, {'ok': True, 'marked': len(result) if isinstance(result, list) else 0})
        return _json_resp(handler, 200, {'ok': True})

    # --- Create Alert Rule ---
    if path == '/api/alert-rules':
        payload = payload or {}
        rule = {
            'rule_type': payload.get('rule_type', ''),
            'threshold': payload.get('threshold', {}),
            'channels': payload.get('channels', ['dashboard']),
            'is_active': payload.get('is_active', True),
        }
        if _supa_available():
            result = sh.supa_insert('alert_rules', rule)
            if isinstance(result, list) and len(result) > 0:
                return _json_resp(handler, 201, {'ok': True, 'rule': result[0]})
            return _json_resp(handler, 500, {'ok': False, 'error': result})
        return _json_resp(handler, 201, {'ok': True, 'rule': rule})

    # --- Create Budget Limit ---
    if path == '/api/budget-limits':
        payload = payload or {}
        limit_data = {
            'scope': payload.get('scope', 'global'),
            'domain': payload.get('domain'),
            'period': payload.get('period', 'daily'),
            'limit_usd': float(payload.get('limit_usd', 5)),
            'action': payload.get('action', 'alert'),
            'is_active': True,
        }
        if _supa_available():
            result = sh.supa_insert('budget_limits', limit_data)
            if isinstance(result, list) and len(result) > 0:
                return _json_resp(handler, 201, {'ok': True, 'limit': result[0]})
            return _json_resp(handler, 500, {'ok': False, 'error': result})
        return _json_resp(handler, 201, {'ok': True, 'limit': limit_data})

    # --- Save Template Version ---
    if path == '/api/template-versions':
        payload = payload or {}
        version = {
            'domain': payload.get('domain', ''),
            'subdomain': payload.get('subdomain', ''),
            'page_path': payload.get('page_path', ''),
            'agent_name': payload.get('agent_name', ''),
            'model_name': payload.get('model_name', ''),
            'html_content': payload.get('html_content', ''),
            'scores': payload.get('scores', {}),
            'is_active': payload.get('is_active', False),
        }
        if _supa_available():
            result = sh.supa_insert('template_versions', version)
            if isinstance(result, list) and len(result) > 0:
                return _json_resp(handler, 201, {'ok': True, 'version': result[0]})
