#!/usr/bin/env python3
"""Figma API Connector for Dashboard Project.

Connects to Figma API to extract:
- Frames and components
- Colors and styles
- Typography
- Measurements and spacing
- Assets and images
- Design tokens

Supports:
- Figma REST API (personal access token)
- Figma MCP (via external MCP server)
"""
import json
import urllib.error
import urllib.request
import urllib.parse
from typing import Optional


class FigmaAPIClient:
    """Client for Figma REST API."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.api_base = "https://api.figma.com/v1"

    def _request(self, endpoint: str, method: str = 'GET') -> dict:
        """Make authenticated request to Figma API."""
        url = f"{self.api_base}{endpoint}"
        headers = {
            'X-Figma-Token': self.access_token,
            'Accept': 'application/json'
        }

        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return {'success': True, 'data': json.loads(resp.read().decode())}
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f"HTTP {e.code}: {e.read().decode()}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # --- File Info ---
    def get_file(self, file_key: str) -> dict:
        """Get entire Figma file structure."""
        return self._request(f"/files/{file_key}")

    def get_file_nodes(self, file_key: str, ids: list) -> dict:
        """Get specific nodes from a file."""
        ids_str = ','.join(ids)
        return self._request(f"/files/{file_key}/nodes?ids={ids_str}")

    def get_file_versions(self, file_key: str) -> dict:
        """Get file version history."""
        return self._request(f"/files/{file_key}/versions")

    # --- Images ---
    def get_image(self, file_key: str, node_ids: list, format: str = 'png', scale: float = 2) -> dict:
        """Get rendered images of nodes."""
        ids_str = ','.join(node_ids)
        return self._request(f"/images/{file_key}?ids={ids_str}&format={format}&scale={scale}")

    # --- Styles ---
    def get_styles(self, file_key: str) -> dict:
        """Get all styles in a file."""
        return self._request(f"/files/{file_key}/styles")

    # --- Comments ---
    def get_comments(self, file_key: str) -> dict:
        """Get comments on a file."""
        return self._request(f"/files/{file_key}/comments")

    # --- Projects ---
    def get_project(self, project_id: str) -> dict:
        """Get files in a project."""
        return self._request(f"/projects/{project_id}/files")

    # --- Team ---
    def get_team_projects(self, team_id: str) -> dict:
        """Get projects for a team."""
        return self._request(f"/teams/{team_id}/projects")

    # --- User ---
    def get_me(self) -> dict:
        """Get current user info."""
        return self._request("/me")

    # --- Design Extraction Helpers ---
    def extract_colors(self, file_key: str) -> dict:
        """Extract color palette from file."""
        result = self.get_file(file_key)
        if not result['success']:
            return result

        colors = {}
        styles_result = self.get_styles(file_key)
        if styles_result['success']:
            for style in styles_result['data'].get('meta', {}).get('styles', []):
                if style.get('styleType') == 'FILL':
                    colors[style['name']] = {
                        'type': style.get('styleType'),
                        'nodes': style.get('nodeIds', []),
                        'key': style.get('key')
                    }

        # Also extract from document
        doc = result['data'].get('document', {})
        self._extract_colors_from_node(doc, colors)

        return {'success': True, 'colors': colors, 'count': len(colors)}

    def _extract_colors_from_node(self, node: dict, colors: dict):
        """Recursively extract colors from node tree."""
        if not node:
            return

        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'SOLID' and fill.get('color'):
                c = fill['color']
                hex_color = f"#{int(c['r']*255):02x}{int(c['g']*255):02x}{int(c['b']*255):02x}"
                name = node.get('name', 'unnamed')
                if hex_color not in colors:
                    colors[hex_color] = {'name': name, 'opacity': c.get('a', 1), 'rgb': f"rgb({int(c['r']*255)}, {int(c['g']*255)}, {int(c['b']*255)})"}

        for child in node.get('children', []):
            self._extract_colors_from_node(child, colors)

    def extract_typography(self, file_key: str) -> dict:
        """Extract typography styles from file."""
        result = self.get_file(file_key)
        if not result['success']:
            return result

        typography = {}
        self._extract_typography_from_node(result['data'].get('document', {}), typography)
        return {'success': True, 'typography': typography, 'count': len(typography)}

    def _extract_typography_from_node(self, node: dict, typography: dict):
        """Recursively extract typography from node tree."""
        if not node:
            return

        if node.get('type') == 'TEXT':
            style = node.get('style', {})
            key = f"{style.get('fontFamily', 'unknown')}_{style.get('fontSize', 0)}_{style.get('fontWeight', 400)}"
            if key not in typography:
                typography[key] = {
                    'fontFamily': style.get('fontFamily'),
                    'fontSize': style.get('fontSize'),
                    'fontWeight': style.get('fontWeight'),
                    'lineHeightPx': style.get('lineHeightPx'),
                    'letterSpacing': style.get('letterSpacing'),
                    'textAlign': style.get('textAlignHorizontal'),
                    'examples': []
                }
            typography[key]['examples'].append({
                'text': node.get('characters', '')[:50],
                'nodeId': node.get('id')
            })

        for child in node.get('children', []):
            self._extract_typography_from_node(child, typography)

    def extract_spacing(self, file_key: str) -> dict:
        """Extract spacing/measurements from file."""
        result = self.get_file(file_key)
        if not result['success']:
            return result

        spacing = {}
        self._extract_spacing_from_node(result['data'].get('document', {}), spacing)
        return {'success': True, 'spacing': spacing}

    def _extract_spacing_from_node(self, node: dict, spacing: dict):
        """Extract spacing values from node tree."""
        if not node:
            return

        padding = node.get('paddingTop') or node.get('paddingLeft')
        if padding:
            key = f"{padding}px"
            spacing[key] = spacing.get(key, 0) + 1

        gap = node.get('itemSpacing')
        if gap:
            key = f"{gap}px"
            spacing[key] = spacing.get(key, 0) + 1

        for child in node.get('children', []):
            self._extract_spacing_from_node(child, spacing)

    def extract_components(self, file_key: str) -> dict:
        """Extract component list from file."""
        result = self.get_file(file_key)
        if not result['success']:
            return result

        components = []
        self._extract_components_from_node(result['data'].get('document', {}), components)
        return {'success': True, 'components': components, 'count': len(components)}

    def _extract_components_from_node(self, node: dict, components: list):
        """Extract component instances and definitions."""
        if not node:
            return

        if node.get('type') in ('COMPONENT', 'COMPONENT_SET'):
            components.append({
                'id': node.get('id'),
                'name': node.get('name'),
                'type': node.get('type'),
                'description': node.get('description', ''),
                'width': node.get('absoluteBoundingBox', {}).get('width'),
                'height': node.get('absoluteBoundingBox', {}).get('height')
            })

        for child in node.get('children', []):
            self._extract_components_from_node(child, components)

    def extract_design_tokens(self, file_key: str) -> dict:
        """Extract complete design tokens from file."""
        colors = self.extract_colors(file_key)
        typography = self.extract_typography(file_key)
        spacing = self.extract_spacing(file_key)
        components = self.extract_components(file_key)

        tokens = {
            'colors': colors.get('colors', {}),
            'typography': typography.get('typography', {}),
            'spacing': spacing.get('spacing', {}),
            'components': components.get('components', [])
        }
        return {'success': True, 'tokens': tokens}

    def check_connection(self) -> dict:
        """Test Figma API connectivity."""
        result = self.get_me()
        if result['success']:
            return {'connected': True, 'user': result['data'].get('email', 'unknown')}
        return {'connected': False, 'error': result.get('error')}


def create_figma_client(access_token: str = None):
    """Factory function to create Figma API client."""
    import os
    access_token = access_token or os.getenv('FIGMA_ACCESS_TOKEN', '')

    if not access_token:
        return None
    return FigmaAPIClient(access_token)
