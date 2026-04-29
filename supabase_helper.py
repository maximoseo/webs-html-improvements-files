#!/usr/bin/env python3
"""Supabase helper for Hermes Dashboard — REST API wrapper."""
import json
import os
import urllib.request
import urllib.error
import urllib.parse

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')

def _headers(use_service=False):
    key = SUPABASE_SERVICE_KEY if use_service else SUPABASE_ANON_KEY
    return {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    }

def _url(table):
    return f"{SUPABASE_URL}/rest/v1/{table}"

def _rpc_url(func):
    return f"{SUPABASE_URL}/rest/v1/rpc/{func}"

def _request(method, url, headers, data=None, timeout=15):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            if raw.strip():
                return json.loads(raw)
            return []
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ''
        return {'error': f'HTTP {e.code}', 'detail': err_body[:500]}
    except Exception as e:
        return {'error': str(e)}

# --- Generic CRUD helpers ---

def supa_select(table, select='*', filters=None, order=None, limit=100, offset=0, use_service=False):
    """SELECT from Supabase table."""
    url = _url(table)
    params = {'select': select, 'limit': limit, 'offset': offset}
    if filters:
        params.update(filters)
    if order:
        params['order'] = order
    url += '?' + urllib.parse.urlencode(params)
    return _request('GET', url, _headers(use_service))

def supa_insert(table, data, use_service=False):
    """INSERT into Supabase table."""
    url = _url(table)
    return _request('POST', url, _headers(use_service), data)

def supa_update(table, match_col, match_val, data, use_service=False):
    """UPDATE row(s) in Supabase table."""
    url = f"{_url(table)}?{match_col}=eq.{match_val}"
    return _request('PATCH', url, _headers(use_service), data)

def supa_delete(table, match_col, match_val, use_service=False):
    """DELETE row(s) from Supabase table."""
    url = f"{_url(table)}?{match_col}=eq.{match_val}"
    return _request('DELETE', url, _headers(use_service))

def supa_rpc(func, data, use_service=False):
    """Call Supabase RPC function."""
    url = _rpc_url(func)
    return _request('POST', url, _headers(use_service), data)

# --- Feature-specific helpers ---

def is_feature_enabled(flag_name):
    """Check if a feature flag is enabled."""
    result = supa_select('feature_flags', select='is_enabled', filters={'flag_name': f'eq.{flag_name}'}, limit=1)
    if isinstance(result, list) and len(result) > 0:
        return result[0].get('is_enabled', False)
    return False  # default to disabled if flag not found

def log_audit(table_name, action, changes=None, previous_values=None, user_id=None, ip_address=None, record_id=None):
    """Write to audit_log table."""
    if not SUPABASE_URL:
        return  # skip if no Supabase configured
    supa_insert('audit_log', {
        'table_name': table_name,
        'action': action,
        'changes': changes or {},
        'previous_values': previous_values,
        'user_id': user_id,
        'ip_address': ip_address,
        'record_id': record_id,
    })

def check_budget_exceeded(domain=None, limit_type='daily'):
    """Check if current spending exceeds budget limit."""
    # Get budget limits
    filters = {'is_active': 'eq.true', 'period': f'eq.{limit_type}'}
    if domain:
        filters['domain'] = f'eq.{domain}'
    else:
        filters['scope'] = 'eq.global'
    
    limits = supa_select('budget_limits', filters=filters)
    if isinstance(limits, dict) and 'error' in limits:
        return False, None
    
    for limit in (limits or []):
        lim = limit.get('limit_usd', 0)
        # Query cost for the period
        cost = supa_select('agent_traces', select='cost_usd', filters={})
        if isinstance(cost, dict) and 'error' in cost:
            continue
        total = sum(c.get('cost_usd', 0) for c in (cost or []) if isinstance(c, dict))
        if total >= lim:
            return True, limit
    return False, None
