#!/usr/bin/env python3
"""Client Reports Engine — auto-generate weekly/monthly reports from dashboard data."""
import os
import sys
import json
import csv
import io
import datetime
import threading
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import supabase_helper as sh

# ============================================================
# Report Generator
# ============================================================

class ReportGenerator:
    """Generate client reports from Supabase data."""

    def generate_report(self, domain, report_type='weekly', date_from=None, date_to=None, send_to=None):
        """Generate a report for a domain and save to client_reports table."""
        now = datetime.datetime.utcnow()

        # Default date range
        if not date_to:
            date_to = now.strftime('%Y-%m-%d')
        if not date_from:
            if report_type == 'weekly':
                date_from = (now - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            elif report_type == 'monthly':
                date_from = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            else:
                date_from = (now - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

        # Collect data sections
        sections = {}
        sections['summary'] = self._get_summary(domain, date_from, date_to)
        sections['agent_activity'] = self._get_agent_activity(domain, date_from, date_to)
        sections['cost_breakdown'] = self._get_cost_breakdown(domain, date_from, date_to)
        sections['batch_jobs'] = self._get_batch_jobs(domain, date_from, date_to)
        sections['budget_status'] = self._get_budget_status(domain)

        report_content = {
            'domain': domain,
            'report_type': report_type,
            'date_from': date_from,
            'date_to': date_to,
            'generated_at': now.isoformat(),
            'sections': sections,
        }

        # Save to Supabase
        report_record = {
            'domain': domain,
            'report_type': report_type,
            'date_from': date_from,
            'date_to': date_to,
            'content': report_content,
            'sent_to': send_to,
        }

        result = sh.supa_insert('client_reports', report_record)

        return {
            'success': isinstance(result, list) and len(result) > 0,
            'report_id': result[0].get('id') if isinstance(result, list) and result else None,
            'content': report_content,
        }

    def export_csv(self, domain, date_from=None, date_to=None):
        """Export report data as CSV."""
        now = datetime.datetime.utcnow()
        if not date_to:
            date_to = now.strftime('%Y-%m-%d')
        if not date_from:
            date_from = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            'Domain', 'Date', 'Agent', 'Model', 'Action',
            'Status', 'Tokens In', 'Tokens Out', 'Cost USD',
            'Batch Name', 'Duration (ms)'
        ])

        # Agent traces
        filters = {'domain': f'eq.{domain}'}
        traces = sh.supa_select('agent_traces', filters=filters, limit=5000, order='created_at.desc')
        if isinstance(traces, list):
            for t in traces:
                if not isinstance(t, dict):
                    continue
                created = t.get('created_at', '')[:10] if t.get('created_at') else ''
                if created and (created < date_from or created > date_to):
                    continue
                writer.writerow([
                    t.get('domain', ''),
                    t.get('created_at', '')[:10] if t.get('created_at') else '',
                    t.get('agent_name', ''),
                    t.get('model_name', ''),
                    'trace',
                    'completed',
                    t.get('tokens_in', ''),
                    t.get('tokens_out', ''),
                    round(t.get('cost_usd', 0), 4),
                    '',
                    t.get('duration_ms', ''),
                ])

        # Batch jobs
        filters = {}
        jobs = sh.supa_select('batch_jobs', filters=filters, limit=200, order='created_at.desc')
        if isinstance(jobs, list):
            for j in jobs:
                if not isinstance(j, dict):
                    continue
                created = j.get('created_at', '')[:10] if j.get('created_at') else ''
                if created and (created < date_from or created > date_to):
                    continue
                writer.writerow([
                    domain,
                    created,
                    '',
                    '',
                    j.get('action', ''),
                    j.get('status', ''),
                    '',
                    '',
                    '',
                    j.get('batch_name', ''),
                    '',
                ])

        return output.getvalue()

    def get_existing_reports(self, domain=None, limit=50):
        """Get list of previously generated reports."""
        filters = {}
        if domain:
            filters['domain'] = f'eq.{domain}'
        result = sh.supa_select('client_reports', filters=filters, limit=limit, order='created_at.desc')
        if isinstance(result, dict) and 'error' in result:
            return []
        return result or []

    def get_report_schedules(self, domain=None):
        """Get report schedules."""
        filters = {}
        if domain:
            filters['domain'] = f'eq.{domain}'
        result = sh.supa_select('report_schedules', filters=filters)
        if isinstance(result, dict) and 'error' in result:
            return []
        return result or []

    def process_scheduled_reports(self):
        """Check and generate reports for active schedules."""
        schedules = sh.supa_select('report_schedules', filters={'is_active': 'eq.true'})
        if isinstance(schedules, dict) and 'error' in schedules:
            return

        now = datetime.datetime.utcnow()
        today = now.strftime('%A').lower()
        day_of_month = now.day

        for sched in (schedules or []):
            try:
                freq = sched.get('frequency', '')
                if freq == 'weekly':
                    sched_day = sched.get('day_of_week', 0)
                    if sched_day != now.weekday():
                        continue
                elif freq == 'monthly':
                    sched_dom = sched.get('day_of_month', 1)
                    if sched_dom != day_of_month:
                        continue

                domain = sched.get('domain', '')
                recipients = sched.get('send_to', [])
                if not domain:
                    continue

                result = self.generate_report(domain, report_type=freq, send_to=recipients)
                if result.get('success'):
                    print(f'[ReportEngine] Generated {freq} report for {domain}', flush=True)
            except Exception as e:
                print(f'[ReportEngine] Error processing schedule for {sched.get("domain")}: {e}', flush=True)

    # --- Data Collection Methods ---

    def _get_summary(self, domain, date_from, date_to):
        """Get high-level summary statistics."""
        summary = {
            'total_traces': 0,
            'total_cost': 0,
            'total_tokens_in': 0,
            'total_tokens_out': 0,
            'avg_cost_per_trace': 0,
            'unique_models': [],
            'unique_agents': [],
        }

        filters = {'domain': f'eq.{domain}'}
        traces = sh.supa_select('agent_traces', filters=filters, limit=5000)
        if isinstance(traces, list):
            for t in traces:
                if not isinstance(t, dict):
                    continue
                created = t.get('created_at', '')[:10] if t.get('created_at') else ''
                if created and (created < date_from or created > date_to):
                    continue
                summary['total_traces'] += 1
                summary['total_cost'] += t.get('cost_usd', 0) or 0
                summary['total_tokens_in'] += t.get('tokens_in', 0) or 0
                summary['total_tokens_out'] += t.get('tokens_out', 0) or 0
                model = t.get('model_name', 'unknown')
                agent = t.get('agent_name', 'unknown')
                if model not in summary['unique_models']:
                    summary['unique_models'].append(model)
                if agent not in summary['unique_agents']:
                    summary['unique_agents'].append(agent)

            if summary['total_traces'] > 0:
                summary['avg_cost_per_trace'] = round(
                    summary['total_cost'] / summary['total_traces'], 4
                )

        summary['total_cost'] = round(summary['total_cost'], 4)
        return summary

    def _get_agent_activity(self, domain, date_from, date_to):
        """Get per-agent activity breakdown."""
        by_agent = {}
        filters = {'domain': f'eq.{domain}'}
        traces = sh.supa_select('agent_traces', filters=filters, limit=5000)
        if isinstance(traces, list):
            for t in traces:
                if not isinstance(t, dict):
                    continue
                created = t.get('created_at', '')[:10] if t.get('created_at') else ''
                if created and (created < date_from or created > date_to):
                    continue
                agent = t.get('agent_name', 'unknown')
                if agent not in by_agent:
                    by_agent[agent] = {
                        'agent_name': agent,
                        'count': 0,
                        'cost': 0,
                        'tokens_in': 0,
                        'tokens_out': 0,
                    }
                by_agent[agent]['count'] += 1
                by_agent[agent]['cost'] += t.get('cost_usd', 0) or 0
                by_agent[agent]['tokens_in'] += t.get('tokens_in', 0) or 0
                by_agent[agent]['tokens_out'] += t.get('tokens_out', 0) or 0

        for a in by_agent.values():
            a['cost'] = round(a['cost'], 4)

        return sorted(by_agent.values(), key=lambda x: x['cost'], reverse=True)

    def _get_cost_breakdown(self, domain, date_from, date_to):
        """Get per-model cost breakdown."""
        by_model = {}
        filters = {'domain': f'eq.{domain}'}
        traces = sh.supa_select('agent_traces', filters=filters, limit=5000)
        if isinstance(traces, list):
            for t in traces:
                if not isinstance(t, dict):
                    continue
                created = t.get('created_at', '')[:10] if t.get('created_at') else ''
                if created and (created < date_from or created > date_to):
                    continue
                model = t.get('model_name', 'unknown')
                if model not in by_model:
                    by_model[model] = {
                        'model_name': model,
                        'count': 0,
                        'cost': 0,
                    }
                by_model[model]['count'] += 1
                by_model[model]['cost'] += t.get('cost_usd', 0) or 0

        for m in by_model.values():
            m['cost'] = round(m['cost'], 4)

        return sorted(by_model.values(), key=lambda x: x['cost'], reverse=True)

    def _get_batch_jobs(self, domain, date_from, date_to):
        """Get batch jobs summary."""
        jobs = sh.supa_select('batch_jobs', limit=100, order='created_at.desc')
        if not isinstance(jobs, list):
            return []

        result = []
        for j in jobs:
            if not isinstance(j, dict):
                continue
            created = j.get('created_at', '')[:10] if j.get('created_at') else ''
            if created and (created < date_from or created > date_to):
                continue
            result.append({
                'batch_name': j.get('batch_name', ''),
                'action': j.get('action', ''),
                'status': j.get('status', ''),
                'total': j.get('total', 0),
                'progress': j.get('progress', 0),
                'created_at': j.get('created_at', ''),
            })
        return result

    def _get_budget_status(self, domain):
        """Get current budget status."""
        exceeded, limit_info, spent = sh.check_budget_exceeded(limit_type='daily')
        return {
            'budget_exceeded': exceeded,
            'daily_spent': round(spent, 4) if spent else 0,
            'daily_limit': round(limit_info.get('limit_usd', 0), 2) if limit_info else 0,
        }


# ============================================================
# Global instance
# ============================================================
_report_generator = None

def get_report_generator():
    global _report_generator
    if _report_generator is None:
        _report_generator = ReportGenerator()
    return _report_generator
