import json
import re
import unicodedata

_DOMAIN_RE = re.compile(r'(?<!@)\b(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:/[\w./?%&=+#:;,@!~*-]*)?')
_HTML_HINT_RE = re.compile(r'<!doctype|<html\b|<table\b|<body\b|<div\b|<p\b|<h[1-6]\b', re.I)


def looks_like_html(value):
    return isinstance(value, str) and bool(_HTML_HINT_RE.search(value))


def sanitize_filename_part(value, default='untitled'):
    value = unicodedata.normalize('NFKD', str(value or '')).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9._-]+', '-', value).strip('-._').lower()
    value = re.sub(r'-{2,}', '-', value)
    return value or default


def _append_html_node(out, node, html_content, source, **extra):
    if not html_content:
        return
    out.append({
        'node_name': node.get('name') or 'Unnamed Node',
        'node_type': node.get('type') or '',
        'html_content': html_content,
        'source': source,
        **extra,
    })


def extract_html_nodes(workflow):
    """Extract HTML-containing n8n nodes while preserving expressions verbatim."""
    html_nodes = []
    for node in workflow.get('nodes') or []:
        node_type = node.get('type') or ''
        parameters = node.get('parameters') or {}
        lowered = node_type.lower()

        if node_type == 'n8n-nodes-base.html':
            _append_html_node(html_nodes, node, parameters.get('html') or '', 'html_node', operation=parameters.get('operation') or '')
            continue

        if node_type == 'n8n-nodes-base.code':
            code = parameters.get('jsCode') or parameters.get('pythonCode') or ''
            if looks_like_html(code):
                _append_html_node(html_nodes, node, code, 'code_node')
            continue

        if node_type == 'n8n-nodes-base.set':
            values = (parameters.get('values') or {}).get('string') or []
            for value in values:
                val = value.get('value') if isinstance(value, dict) else ''
                if looks_like_html(val):
                    _append_html_node(html_nodes, node, val, 'set_node', field_name=value.get('name', '') if isinstance(value, dict) else '')
            continue

        if node_type in ('n8n-nodes-base.function', 'n8n-nodes-base.functionItem'):
            code = parameters.get('functionCode') or ''
            if looks_like_html(code):
                _append_html_node(html_nodes, node, code, 'function_node')
            continue

        if 'email' in lowered or 'sendemail' in lowered:
            html_body = parameters.get('html') or parameters.get('htmlBody') or parameters.get('message') or ''
            if looks_like_html(html_body) or html_body:
                _append_html_node(html_nodes, node, html_body, 'email_node')

    return html_nodes


def _find_domains_in_text(text):
    domains = set()
    for match in _DOMAIN_RE.finditer(str(text or '')):
        domain = match.group(1).strip('.').lower()
        if domain and not domain.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.css', '.js')):
            domains.add(domain)
    return domains


def identify_domain(workflow):
    domains = set()
    name = workflow.get('name') or ''
    domains.update(_find_domains_in_text(name))
    tags = []
    for tag in workflow.get('tags') or []:
        tag_name = tag.get('name') if isinstance(tag, dict) else str(tag)
        tags.append(tag_name)
        domains.update(_find_domains_in_text(tag_name))
    for node in workflow.get('nodes') or []:
        try:
            domains.update(_find_domains_in_text(json.dumps(node.get('parameters') or {}, ensure_ascii=False)))
        except Exception:
            pass
    ordered = sorted(domains)
    return {
        'workflow_name': name,
        'tags': tags,
        'domains_found': ordered,
        'primary_domain': ordered[0] if ordered else 'uncategorized',
    }
