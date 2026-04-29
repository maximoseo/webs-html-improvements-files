#!/usr/bin/env python3
"""WPGraphQL Connector for Dashboard Project.

Connects to WordPress sites via WPGraphQL to:
- Query complex nested content
- Access ACF fields directly
- Custom post types and taxonomies
- User data and author info
- Media with custom fields
- WooCommerce products (if WooGraphQL installed)
"""
import json
import urllib.error
import urllib.request
import urllib.parse
from typing import Optional


class WPGraphQLClient:
    """Client for WPGraphQL API."""

    def __init__(self, site_url: str, api_key: str = None):
        self.site_url = site_url.rstrip('/')
        self.endpoint = f"{self.site_url}/graphql"
        self.api_key = api_key

    def _query(self, query: str, variables: dict = None) -> dict:
        """Execute GraphQL query."""
        payload = {'query': query}
        if variables:
            payload['variables'] = variables

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"

        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode(),
            headers=headers,
            method='POST'
        )
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            result = json.loads(resp.read().decode())
            if result.get('errors'):
                return {'success': False, 'error': result['errors']}
            return {'success': True, 'data': result.get('data', {})}
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f"HTTP {e.code}: {e.read().decode()}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # --- Basic Content ---
    def get_posts(self, first: int = 10, after: str = None, status: str = 'PUBLISH') -> dict:
        """Fetch posts with pagination."""
        query = """
        query GetPosts($first: Int = 10, $after: String, $status: PostStatusEnum = PUBLISH) {
          posts(first: $first, after: $after, where: {status: $status}) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id databaseId title content(excerpt: true) date uri
              author { node { name } }
              categories { nodes { name slug } }
              featuredImage { node { sourceUrl mediaDetails { sizes { name width height sourceUrl } } } }
            }
          }
        }
        """
        return self._query(query, {'first': first, 'after': after, 'status': status})

    def get_pages(self, first: int = 50) -> dict:
        """Get pages with full content."""
        query = """
        query GetPages($first: Int = 50) {
          pages(first: $first) {
            nodes {
              id databaseId title content uri date modified
              parent { node { databaseId title } }
              children { nodes { databaseId title } }
              featuredImage { node { sourceUrl } }
            }
          }
        }
        """
        return self._query(query, {'first': first})

    def get_page_by_uri(self, uri: str) -> dict:
        """Get page by URL path."""
        query = """
        query GetPageByUri($uri: String!) {
          pageBy(uri: $uri) {
            id databaseId title content uri date modified
            seo { title description canonical }
            editorBlocks { name renderedHtml }
          }
        }
        """
        return self._query(query, {'uri': uri})

    # --- Taxonomies ---
    def get_categories(self, first: int = 100) -> dict:
        """Get all categories."""
        query = """
        query GetCategories($first: Int = 100) {
          categories(first: $first) {
            nodes { databaseId name slug description count }
          }
        }
        """
        return self._query(query, {'first': first})

    def get_tags(self, first: int = 100) -> dict:
        """Get all tags."""
        query = """
        query GetTags($first: Int = 100) {
          tags(first: $first) {
            nodes { databaseId name slug description count }
          }
        }
        """
        return self._query(query, {'first': first})

    # --- Media ---
    def get_media(self, first: int = 20) -> dict:
        """Get media items."""
        query = """
        query GetMedia($first: Int = 20) {
          mediaItems(first: $first) {
            nodes {
              id databaseId title sourceUrl mimeType altText
              mediaDetails { width height sizes { name width height sourceUrl } }
            }
          }
        }
        """
        return self._query(query, {'first': first})

    # --- Users ---
    def get_users(self, first: int = 20) -> dict:
        """Get users."""
        query = """
        query GetUsers($first: Int = 20) {
          users(first: $first) {
            nodes { databaseId name slug avatar { url } description }
          }
        }
        """
        return self._query(query, {'first': first})

    # --- SEO (requires Yoast/WPGraphQL SEO plugin) ---
    def get_seo_info(self) -> dict:
        """Get site SEO settings."""
        query = """
        query GetSEO {
          generalSettings { title description }
          seo { webmaster { googleSearchConsole } schema { siteName siteUrl } }
        }
        """
        return self._query(query)

    # --- Menu ---
    def get_menu(self, location: str = 'PRIMARY') -> dict:
        """Get navigation menu by location."""
        query = """
        query GetMenu($location: MenuLocationEnum = PRIMARY) {
          menuItems(where: {location: $location}) {
            nodes {
              label uri target cssClasses
              parent { node { label } }
            }
          }
        }
        """
        return self._query(query, {'location': location})

    # --- Custom Query ---
    def custom_query(self, query: str, variables: dict = None) -> dict:
        """Execute any custom GraphQL query."""
        return self._query(query, variables)

    def check_connection(self) -> dict:
        """Test WPGraphQL connectivity."""
        result = self._query('query { generalSettings { title url } }')
        if result['success'] and result.get('data', {}).get('generalSettings'):
            settings = result['data']['generalSettings']
            return {'connected': True, 'site_url': settings.get('url', ''), 'site_title': settings.get('title', '')}
        return {'connected': False, 'error': result.get('error', 'No data returned')}


def create_wp_graphql_client(site_url: str = None, api_key: str = None):
    """Factory function to create WPGraphQL client."""
    import os
    site_url = site_url or os.getenv('WORDPRESS_SITE_URL', '')
    api_key = api_key or os.getenv('WPGRAPHQL_API_KEY', '')

    if not site_url:
        return None
    return WPGraphQLClient(site_url, api_key)
