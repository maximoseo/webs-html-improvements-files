#!/usr/bin/env python3
"""Screenshot-to-Code client for the Maximo SEO Dashboard.

Connects to a self-hosted or external screenshot-to-code instance
(https://github.com/abi/screenshot-to-code) to convert images/screenshots
into clean HTML/Tailwind/React code.

Environment variables:
    SCREENSHOT_TO_CODE_URL - Base URL of the screenshot-to-code service
    SCREENSHOT_TO_CODE_API_KEY - Optional API key for hosted version
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request


def create_s2c_client():
    """Create and return a ScreenshotToCode client, or None if not configured."""
    url = os.getenv('SCREENSHOT_TO_CODE_URL')
    if not url:
        return None
    api_key = os.getenv('SCREENSHOT_TO_CODE_API_KEY', '')
    return ScreenshotToCodeClient(url.rstrip('/'), api_key)


class ScreenshotToCodeClient:
    """Client for the screenshot-to-code API."""

    def __init__(self, base_url, api_key=''):
        self.base_url = base_url
        self.api_key = api_key

    def _headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def _post(self, path, data):
        """Send POST request to the screenshot-to-code API."""
        url = f'{self.base_url}{path}'
        body = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=self._headers(), method='POST')
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.URLError as e:
            return {'error': f'Connection failed: {str(e)}', 'code': None}
        except Exception as e:
            return {'error': str(e), 'code': None}

    def check_connection(self):
        """Check if the screenshot-to-code service is reachable."""
        try:
            url = f'{self.base_url}/api/health'
            req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {'connected': True, 'status': resp.status}
        except Exception as e:
            return {'connected': False, 'error': str(e)}

    def convert_image(self, image_source, output_format='html_tailwind', model=''):
        """Convert a screenshot/image to code.

        Args:
            image_source: URL of image or base64-encoded data
            output_format: html_tailwind, html_css, react, vue, bootstrap, ionic, svg
            model: Optional model override (e.g., 'claude-3-5-sonnet', 'gpt-4o')

        Returns:
            dict with generated code and metadata
        """
        # Determine if it's a URL or base64
        is_url = image_source.startswith(('http://', 'https://', 'data:'))

        payload = {
            'image': image_source,
            'is_url': is_url,
            'output_format': output_format,
        }
        if model:
            payload['model'] = model

        result = self._post('/api/generate-code', payload)
        return result

    def convert_url(self, url, output_format='html_tailwind', model=''):
        """Convert a live website URL to code by taking a screenshot first."""
        payload = {
            'url': url,
            'output_format': output_format,
        }
        if model:
            payload['model'] = model

        result = self._post('/api/generate-code', payload)
        return result


if __name__ == '__main__':
    # Test connection
    client = create_s2c_client()
    if client:
        print("Screenshot-to-Code client created:")
        print(f"  URL: {client.base_url}")
        print(f"  Connection: {client.check_connection()}")
    else:
        print("Not configured. Set SCREENSHOT_TO_CODE_URL env var.")
