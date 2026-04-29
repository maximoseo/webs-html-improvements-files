#!/usr/bin/env python3
"""Google PageSpeed Insights API Connector for Dashboard Project.

Connects to Google PageSpeed Insights API to:
- Analyze mobile and desktop performance
- Get Core Web Vitals (LCP, CLS, INP, FCP, TTFB)
- Receive optimization suggestions
- Check accessibility, best practices, SEO
- Compare scores over time
"""
import json
import urllib.error
import urllib.request
import urllib.parse
from typing import Optional


class PageSpeedClient:
    """Client for Google PageSpeed Insights API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.api_base = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def analyze(self, url: str, strategy: str = 'both', categories: list = None, locale: str = 'en') -> dict:
        """Run PageSpeed analysis on a URL.

        Args:
            url: URL to analyze
            strategy: 'mobile', 'desktop', or 'both'
            categories: List of categories to analyze (PERFORMANCE, ACCESSIBILITY, BEST_PRACTICES, SEO, PWA)
            locale: Language for results
        """
        if categories is None:
            categories = ['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO']

        results = {}

        strategies = ['MOBILE', 'DESKTOP'] if strategy == 'both' else [strategy.upper()]

        for strat in strategies:
            params = {
                'url': url,
                'strategy': strat,
                'category': ','.join(categories),
                'locale': locale
            }
            if self.api_key:
                params['key'] = self.api_key

            api_url = f"{self.api_base}?{urllib.parse.urlencode(params)}"

            req = urllib.request.Request(api_url, method='GET')
            try:
                resp = urllib.request.urlopen(req, timeout=60)
                data = json.loads(resp.read().decode())
                results[strat.lower()] = self._parse_result(data)
            except urllib.error.HTTPError as e:
                results[strat.lower()] = {'success': False, 'error': f"HTTP {e.code}: {e.read().decode()}"}
            except Exception as e:
                results[strat.lower()] = {'success': False, 'error': str(e)}

        return {'success': True, 'url': url, 'results': results}

    def _parse_result(self, data: dict) -> dict:
        """Parse PageSpeed API response into clean format."""
        lighthouse = data.get('lighthouseResult', {})
        if not lighthouse:
            return {'success': False, 'error': 'No Lighthouse data'}

        # Overall scores
        categories = {}
        for cat_key, cat in lighthouse.get('categories', {}).items():
            score = cat.get('score', 0)
            categories[cat_key] = {
                'score': score,
                'percentage': int(score * 100) if score else 0,
                'title': cat.get('title', cat_key)
            }

        # Core Web Vitals
        audits = lighthouse.get('audits', {})
        cwv = {}
        for metric in ['largest-contentful-paint', 'cumulative-layout-shift', 'interactive',
                       'first-contentful-paint', 'total-blocking-time', 'speed-index']:
            if metric in audits:
                audit = audits[metric]
                cwv[metric] = {
                    'value': audit.get('numericValue'),
                    'score': audit.get('score', 0),
                    'displayValue': audit.get('displayValue', ''),
                    'rating': audit.get('scoreDisplayMode', ''),
                    'description': audit.get('description', '')
                }

        # Diagnostics
        diagnostics = []
        for audit_id, audit in audits.items():
            if audit.get('score') is not None and audit.get('score') < 0.9:
                if audit.get('scoreDisplayMode') != 'notApplicable':
                    diagnostics.append({
                        'id': audit_id,
                        'title': audit.get('title', ''),
                        'score': audit.get('score', 0),
                        'description': audit.get('description', ''),
                        'details': audit.get('details', {})
                    })

        # Opportunities
        opportunities = []
        opp_audit = audits.get('opportunities', {})
        if opp_audit and opp_audit.get('details', {}).get('items'):
            for item in opp_audit['details']['items']:
                opportunities.append({
                    'url': item.get('url', ''),
                    'savings': item.get('overallSavingsMs', 0),
                    'bytes': item.get('overallSavingsBytes', 0)
                })

        # Page stats
        fetch_time = data.get('analysisUTCTimestamp', '')
        final_url = lighthouse.get('finalUrl', '')

        return {
            'success': True,
            'categories': categories,
            'core_web_vitals': cwv,
            'diagnostics': diagnostics[:20],  # Top 20 issues
            'opportunities': opportunities[:10],  # Top 10 opportunities
            'fetch_time': fetch_time,
            'final_url': final_url
        }

    def analyze_multiple(self, urls: list, strategy: str = 'mobile') -> dict:
        """Analyze multiple URLs."""
        results = {}
        for url in urls:
            results[url] = self.analyze(url, strategy)
        return results

    def get_score_summary(self, result: dict) -> dict:
        """Get simplified score summary."""
        summary = {}
        for platform, data in result.get('results', {}).items():
            if data.get('success') and data.get('categories'):
                perf = data['categories'].get('PERFORMANCE', {})
                summary[platform] = {
                    'performance': perf.get('percentage', 0),
                    'accessibility': data['categories'].get('ACCESSIBILITY', {}).get('percentage', 0),
                    'best_practices': data['categories'].get('BEST_PRACTICES', {}).get('percentage', 0),
                    'seo': data['categories'].get('SEO', {}).get('percentage', 0),
                    'lcp': data.get('core_web_vitals', {}).get('largest-contentful-paint', {}).get('displayValue', 'N/A'),
                    'cls': data.get('core_web_vitals', {}).get('cumulative-layout-shift', {}).get('displayValue', 'N/A'),
                    'inp': data.get('core_web_vitals', {}).get('interactive', {}).get('displayValue', 'N/A')
                }
        return summary


def create_pagespeed_client(api_key: str = None):
    """Factory function to create PageSpeed client."""
    import os
    api_key = api_key or os.getenv('PAGESPEED_API_KEY', '')
    return PageSpeedClient(api_key)
