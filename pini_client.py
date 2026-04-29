"""
Pini Integration Client - Hybrid Approach (Strategy C)
=====================================================
Connects to Pini (pini.websmail.net) to fetch stuck n8n projects.
Uses Puppeteer to login and capture API token, then uses API directly.
Falls back to full scraping if API is not available.
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone


class PiniClient:
    """Hybrid Pini client - API preferred, scraping fallback."""

    def __init__(self):
        self.base_url = os.getenv('PINI_URL', 'https://pini.websmail.net').rstrip('/')
        self.username = os.getenv('PINI_USERNAME', '')
        self.password = os.getenv('PINI_PASSWORD', '')
        self.token = None
        self.cookies = None
        self.api_endpoints = {}
        self.use_api = True  # Start with API mode

    def _discover_and_login(self):
        """
        Phase 1: Discover API endpoints via browser login.
        Requires puppeteer/playwright - not available in this environment.
        For initial implementation, we use direct API calls instead.
        """
        # Puppeteer not available in production Docker environment
        # Direct API calls are used via _try_api_login() instead
        return False

    def _try_api_login(self):
        """
        Try common API login patterns.
        """
        patterns = [
            ('/api/auth/login', {'username': self.username, 'password': self.password}),
            ('/api/login', {'email': self.username, 'password': self.password}),
            ('/auth/login', {'username': self.username, 'password': self.password}),
            ('/login', {'username': self.username, 'password': self.password}),
        ]

        for endpoint, payload in patterns:
            try:
                url = f"{self.base_url}{endpoint}"
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'HermesAgent/1.0'
                })
                resp = urllib.request.urlopen(req, timeout=15)
                result = json.loads(resp.read().decode())

                # Check for token in response
                token = (result.get('token') or result.get('access_token') or
                         result.get('data', {}).get('token') or
                         result.get('data', {}).get('access_token'))

                if token:
                    self.token = token
                    self.use_api = True
                    # Store discovered endpoints
                    self.api_endpoints['login'] = endpoint
                    return True
            except Exception:
                continue

        return False

    def _scrape_projects(self):
        """
        Phase B: Scrape projects page if API not available.
        Requires puppeteer/playwright - not available in production.
        """
        # Puppeteer scraping requires headless browser — not available
        # in the production Docker container. API fallback is preferred.
        return {
            'projects': [],
            'error': 'Puppeteer scraping not available. API login failed or PINI credentials not configured.',
            'method': 'scrape_unavailable'
        }

    def fetch_projects(self):
        """
        Fetch all projects from Pini.
        Returns list of project dicts with stuck/error status.
        """
        if not self.username or not self.password:
            return {
                'projects': [],
                'error': 'PINI_USERNAME and PINI_PASSWORD environment variables not configured',
                'method': 'not_configured'
            }

        # Try API first
        if self._try_api_login():
            return self._fetch_projects_api()

        # Fallback to scraping (TODO)
        return self._scrape_projects()

    def _fetch_projects_api(self):
        """
        Fetch projects using discovered API token.
        """
        # Try common project endpoints
        endpoints = [
            '/api/projects',
            '/api/projects?status=stuck',
            '/api/projects?status=error',
            '/api/projects?status=failed',
            '/api/n8n/projects',
            '/api/workflows',
            '/api/workflows?status=stuck',
        ]

        all_projects = []

        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                headers = {
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'HermesAgent/1.0'
                }
                req = urllib.request.Request(url, headers=headers)
                resp = urllib.request.urlopen(req, timeout=15)
                data = json.loads(resp.read().decode())

                # Parse response (handle different formats)
                projects = self._parse_projects_response(data)
                all_projects.extend(projects)

                # If we got results, save the endpoint
                if projects:
                    self.api_endpoints['projects'] = endpoint
                    break
            except Exception:
                continue

        # Filter for stuck/error/failed projects
        stuck_projects = self._filter_stuck_projects(all_projects)

        return {
            'projects': stuck_projects,
            'total': len(stuck_projects),
            'method': 'api',
            'token_valid': True
        }

    def _parse_projects_response(self, data):
        """
        Parse API response into standard project format.
        Handles different response structures.
        """
        projects = []

        # Handle array response
        if isinstance(data, list):
            projects = data
        # Handle object with data array
        elif isinstance(data, dict):
            projects = (data.get('data') or data.get('projects') or
                        data.get('results') or data.get('items') or [])
            if isinstance(projects, dict):
                projects = [projects]

        # Normalize project format
        normalized = []
        for p in projects:
            if isinstance(p, dict):
                normalized.append({
                    'pini_project_id': str(p.get('id') or p.get('project_id') or p.get('_id') or ''),
                    'name': p.get('name') or p.get('title') or p.get('project_name') or 'Unknown',
                    'client_name': p.get('client') or p.get('client_name') or p.get('customer') or None,
                    'workflow_id': p.get('workflow_id') or p.get('n8n_workflow_id') or p.get('workflow') or None,
                    'workflow_url': p.get('workflow_url') or p.get('n8n_url') or None,
                    'status': (p.get('status') or p.get('state') or 'stuck').lower(),
                    'priority': (p.get('priority') or p.get('severity') or 'medium').lower(),
                    'error_summary': p.get('error') or p.get('error_message') or p.get('error_summary') or p.get('last_error') or None,
                    'error_details': p.get('error_details') or p.get('error_log') or p.get('details') or None,
                    'error_type': p.get('error_type') or p.get('error_category') or None,
                    'stuck_since': p.get('stuck_since') or p.get('failed_at') or p.get('last_error_at') or p.get('created_at') or None,
                    'last_successful': p.get('last_successful') or p.get('last_success') or p.get('last_run_success') or None,
                    'assigned_to': p.get('assigned_to') or p.get('assignee') or p.get('owner') or None,
                    'tags': p.get('tags') or p.get('labels') or [],
                    'notes': p.get('notes') or p.get('description') or None,
                    'pini_raw_data': p,  # Store raw data for reference
                })

        return normalized

    def _filter_stuck_projects(self, projects):
        """
        Filter projects to only include stuck/error/failed ones.
        """
        stuck_keywords = ['stuck', 'error', 'failed', 'stopped', 'תקוע', 'שגיאה', 'כשל']

        filtered = []
        for p in projects:
            status = p.get('status', '').lower()
            error = (p.get('error_summary') or '').lower()
            error_type = (p.get('error_type') or '').lower()

            # Check if status indicates stuck
            is_stuck = any(kw in status for kw in stuck_keywords)

            # Also check error fields for stuck indicators
            if not is_stuck:
                is_stuck = any(kw in error for kw in stuck_keywords) or any(kw in error_type for kw in stuck_keywords)

            if is_stuck:
                # Normalize status
                if any(kw in status for kw in ['error', 'שגיאה']):
                    p['status'] = 'error'
                elif any(kw in status for kw in ['failed', 'כשל']):
                    p['status'] = 'failed'
                elif any(kw in status for kw in ['stopped']):
                    p['status'] = 'stuck'
                elif 'תקוע' in status or 'תקוע' in error:
                    p['status'] = 'stuck'
                else:
                    p['status'] = 'stuck'  # Default

                # Normalize priority
                priority = p.get('priority', 'medium').lower()
                if priority in ['critical', 'high', 'medium', 'low']:
                    pass  # Already valid
                elif priority in ['urgent', 'p0', 'p1', 'critical']:
                    p['priority'] = 'critical'
                elif priority in ['high', 'p2']:
                    p['priority'] = 'high'
                elif priority in ['low', 'p4']:
                    p['priority'] = 'low'
                else:
                    p['priority'] = 'medium'

                filtered.append(p)

        return filtered

    def get_client_status(self):
        """
        Get client configuration status.
        """
        return {
            'configured': bool(self.username and self.password),
            'base_url': self.base_url,
            'token_valid': self.token is not None,
            'api_endpoints': self.api_endpoints,
            'use_api': self.use_api
        }


def create_pini_client():
    """Factory function to create PiniClient."""
    return PiniClient()
