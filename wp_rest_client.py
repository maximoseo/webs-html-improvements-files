#!/usr/bin/env python3
"""WordPress REST API Connector for Dashboard Project.

Connects to WordPress sites via REST API to:
- Fetch posts, pages, custom post types
- Extract themes, plugins, settings
- Pull media library
- Get categories, tags, taxonomies
- Access ACF fields (if ACF to REST plugin installed)
"""
import json
import urllib.error
import urllib.request
import urllib.parse
from typing import Optional


class WordPressRESTClient:
    """Client for WordPress REST API."""

    def __init__(self, site_url: str, username: str = None, password: str = None, app_password: str = None):
        self.site_url = site_url.rstrip('/')
        self.api_base = f"{self.site_url}/wp-json"
        self.auth_header = None

        if username and app_password:
            import base64
            creds = f"{username}:{app_password}".encode()
            self.auth_header = f"Basic {base64.b64encode(creds).decode()}"
        elif username and password:
            import base64
            creds = f"{username}:{password}".encode()
            self.auth_header = f"Basic {base64.b64encode(creds).decode()}"

    def _request(self, endpoint: str, params: dict = None, method: str = 'GET', data: dict = None) -> dict:
        """Make authenticated or unauthenticated request."""
        url = f"{self.api_base}{endpoint}"
        if params:
            url += '?' + urllib.parse.urlencode(params)

        headers = {'Accept': 'application/json'}
        if self.auth_header:
            headers['Authorization'] = self.auth_header

        body = None
        if data and method in ('POST', 'PUT', 'PATCH'):
            body = json.dumps(data).encode()
            headers['Content-Type'] = 'application/json'

        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return {'success': True, 'data': json.loads(resp.read().decode()), 'status': resp.status}
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f"HTTP {e.code}: {e.read().decode()}", 'status': e.code}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # --- Site Info ---
    def get_site_info(self) -> dict:
        """Get site name, description, URL, timezone, etc."""
        return self._request('/wp/v2/settings')

    # --- Posts & Pages ---
    def get_posts(self, per_page: int = 10, page: int = 1, post_type: str = 'post', status: str = 'publish') -> dict:
        """Fetch posts with pagination."""
        return self._request(f'/wp/v2/{post_type}', {'per_page': per_page, 'page': page, 'status': status})

    def get_page(self, page_id: int) -> dict:
        """Get single page by ID."""
        return self._request(f'/wp/v2/pages/{page_id}')

    def get_pages(self, per_page: int = 100) -> dict:
        """Get all pages."""
        return self._request('/wp/v2/pages', {'per_page': per_page})

    def search_content(self, search: str, post_type: str = 'any') -> dict:
        """Search content."""
        return self._request('/wp/v2/search', {'search': search, 'type': post_type, 'per_page': 20})

    # --- Media ---
    def get_media(self, per_page: int = 20, page: int = 1) -> dict:
        """Get media library items."""
        return self._request('/wp/v2/media', {'per_page': per_page, 'page': page})

    def get_media_item(self, media_id: int) -> dict:
        """Get single media item."""
        return self._request(f'/wp/v2/media/{media_id}')

    # --- Taxonomies ---
    def get_categories(self) -> dict:
        """Get all categories."""
        return self._request('/wp/v2/categories', {'per_page': 100})

    def get_tags(self) -> dict:
        """Get all tags."""
        return self._request('/wp/v2/tags', {'per_page': 100})

    # --- Users ---
    def get_users(self) -> dict:
        """Get users (requires auth)."""
        return self._request('/wp/v2/users', {'per_page': 100})

    # --- Themes & Plugins ---
    def get_themes(self) -> dict:
        """Get installed themes (requires auth)."""
        return self._request('/wp/v2/themes')

    def get_plugins(self) -> dict:
        """Get installed plugins (requires auth)."""
        return self._request('/wp/v2/plugins')

    # --- Templates & Template Parts ---
    def get_templates(self) -> dict:
        """Get block templates (requires auth, block themes)."""
        return self._request('/wp/v2/templates', {'per_page': 100})

    def get_template_parts(self) -> dict:
        """Get template parts (requires auth, block themes)."""
        return self._request('/wp/v2/template-parts', {'per_page': 100})

    # --- Navigation ---
    def get_menus(self) -> dict:
        """Get navigation menus."""
        return self._request('/wp/v2/navigation', {'per_page': 100})

    # --- ACF (requires ACF to REST plugin) ---
    def get_acf_options(self) -> dict:
        """Get ACF options page data."""
        return self._request('/acf/v3/options/options')

    def get_post_acf(self, post_id: int, post_type: str = 'posts') -> dict:
        """Get ACF fields for a post."""
        return self._request(f'/acf/v3/{post_type}/{post_id}')

    # --- Custom ---
    def get_custom_endpoint(self, endpoint: str, params: dict = None) -> dict:
        """Call any custom REST endpoint."""
        return self._request(endpoint, params)

    def check_connection(self) -> dict:
        """Test WordPress REST API connectivity."""
        result = self._request('/wp/v2/posts', {'per_page': 1})
        if result['success']:
            return {'connected': True, 'site_url': self.site_url, 'posts_available': len(result.get('data', []))}
        return {'connected': False, 'error': result.get('error')}


def create_wp_rest_client(site_url: str = None, username: str = None, password: str = None, app_password: str = None):
    """Factory function to create WordPress REST client."""
    import os
    site_url = site_url or os.getenv('WORDPRESS_SITE_URL', '')
    username = username or os.getenv('WORDPRESS_USERNAME', '')
    password = password or os.getenv('WORDPRESS_PASSWORD', '')
    app_password = app_password or os.getenv('WORDPRESS_APP_PASSWORD', '')

    if not site_url:
        return None
    return WordPressRESTClient(site_url, username, password, app_password)
