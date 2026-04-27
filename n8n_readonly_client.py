import json
import os
import urllib.parse
import urllib.request

DEFAULT_N8N_BASE_URL = 'https://websiseo.app.n8n.cloud'
_FORBIDDEN_PATH_TOKENS = ('/activate', '/deactivate', '/import', '/delete')


class N8NReadOnlyClient:
    """Tiny n8n public API client with hard read-only guards."""

    def __init__(self, base_url=None, api_key=None, timeout=30):
        self.base_url = (base_url or os.getenv('N8N_BASE_URL') or DEFAULT_N8N_BASE_URL).rstrip('/')
        self.api_key = api_key or os.getenv('N8N_API_KEY') or ''
        self.timeout = timeout

    def _headers(self):
        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers['X-N8N-API-KEY'] = self.api_key
        return headers

    def _validate_read_only(self, path, method):
        method = (method or 'GET').upper()
        parsed_path = urllib.parse.urlparse(path).path.lower()
        if method != 'GET':
            raise ValueError('n8n client is read-only: only GET is allowed')
        if any(token in parsed_path for token in _FORBIDDEN_PATH_TOKENS):
            raise ValueError('n8n mutating workflow endpoint is blocked by read-only policy')

    def request(self, path, method='GET', query=None):
        self._validate_read_only(path, method)
        if path.startswith('http://') or path.startswith('https://'):
            url = path
        else:
            url = self.base_url + '/' + path.lstrip('/')
        if query:
            separator = '&' if '?' in url else '?'
            url += separator + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers=self._headers(), method='GET')
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode('utf-8') or '{}')

    def get_all_workflows(self, limit=100):
        workflows = []
        cursor = None
        while True:
            query = {'limit': int(limit)}
            if cursor:
                query['cursor'] = cursor
            data = self.request('/api/v1/workflows', query=query)
            workflows.extend(data.get('data') or [])
            cursor = data.get('nextCursor')
            if not cursor:
                return workflows

    def get_workflow_detail(self, workflow_id):
        workflow_id = str(workflow_id).strip()
        if not workflow_id:
            raise ValueError('workflow_id is required')
        return self.request('/api/v1/workflows/' + urllib.parse.quote(workflow_id, safe=''))

    def get_executions(self, limit=100, status=None):
        query = {'limit': int(limit)}
        if status:
            query['status'] = status
        data = self.request('/api/v1/executions', query=query)
        return data.get('data') or []

    def get_execution_detail(self, execution_id):
        execution_id = str(execution_id).strip()
        if not execution_id:
            raise ValueError('execution_id is required')
        return self.request('/api/v1/executions/' + urllib.parse.quote(execution_id, safe=''))
