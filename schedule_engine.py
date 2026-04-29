#!/usr/bin/env python3
"""Pipeline Schedule Scheduler — background thread that checks and triggers scheduled runs."""
import os
import sys
import json
import time
import datetime
import threading
import urllib.request
import urllib.error
import hashlib

# Add project root to path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import supabase_helper as sh

# ============================================================
# Schedule Engine
# ============================================================

class ScheduleEngine:
    def __init__(self):
        self.running = False
        self.thread = None
        self.check_interval = 60  # Check every 60 seconds
        self.last_checks = {}  # Track last check time per schedule ID
    
    def start(self):
        """Start the scheduler background thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True, name='schedule-engine')
        self.thread.start()
        print('[ScheduleEngine] Started', flush=True)
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print('[ScheduleEngine] Stopped', flush=True)
    
    def _run_loop(self):
        """Main loop: check schedules periodically."""
        last_report_check = None
        while self.running:
            try:
                self._check_schedules()
                # Check report schedules every 6 hours
                now = datetime.datetime.utcnow()
                if not last_report_check or (now - last_report_check).total_seconds() > 21600:
                    self._check_report_schedules()
                    last_report_check = now
            except Exception as e:
                print(f'[ScheduleEngine] Error in check loop: {e}', flush=True)
            time.sleep(self.check_interval)
    
    def _check_report_schedules(self):
        """Check and process scheduled reports."""
        try:
            from client_reports_engine import get_report_generator
            gen = get_report_generator()
            gen.process_scheduled_reports()
        except Exception as e:
            print(f'[ScheduleEngine] Report schedule check error: {e}', flush=True)
    
    def _check_schedules(self):
        """Check all active schedules and trigger runs if due."""
        if not sh.SUPABASE_URL:
            return
        
        schedules = sh.supa_select('pipeline_schedules', filters={'is_active': 'eq.true'})
        if isinstance(schedules, dict) and 'error' in schedules:
            return
        
        now = datetime.datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%S')
        
        for sched in (schedules or []):
            sched_id = sched.get('id')
            cron = sched.get('cron_expression', '')
            if not cron:
                continue
            
            # Check if this schedule should run now
            if self._is_cron_due(cron, now):
                # Check if we already triggered it recently (avoid duplicates)
                last_check = self.last_checks.get(sched_id)
                if last_check and (now - last_check).total_seconds() < 300:  # 5 min cooldown
                    continue
                
                # Check budget before triggering
                budget_cap = sched.get('budget_cap')
                if budget_cap:
                    exceeded, _, spent = sh.check_budget_exceeded(limit_type='daily')
                    if exceeded:
                        print(f'[ScheduleEngine] Skipping {sched.get("name")}: budget exceeded (${spent:.2f} >= ${budget_cap:.2f})', flush=True)
                        self.last_checks[sched_id] = now
                        continue
                
                # Trigger the pipeline
                self._trigger_schedule(sched, now_str)
                self.last_checks[sched_id] = now
    
    def _is_cron_due(self, cron_expr, now):
        """Check if a cron expression matches the current time."""
        try:
            parts = cron_expr.strip().split()
            if len(parts) != 5:
                return False
            minute, hour, day, month, weekday = parts
            
            def _match(field, value):
                if field == '*':
                    return True
                if ',' in field:
                    return str(value) in field.split(',')
                if '-' in field:
                    start, end = field.split('-', 1)
                    return int(start) <= value <= int(end)
                if '/' in field:
                    base, step = field.split('/', 1)
                    if base == '*':
                        return value % int(step) == 0
                    return value >= int(base) and (value - int(base)) % int(step) == 0
                return str(value) == field
            
            return (
                _match(minute, now.minute) and
                _match(hour, now.hour) and
                _match(day, now.day) and
                _match(month, now.month) and
                _match(weekday, now.weekday() + 1)  # Cron: 0=Sun, Python: 0=Mon
            )
        except Exception:
            return False
    
    def _trigger_schedule(self, schedule, now_str):
        """Trigger a pipeline run for the schedule."""
        name = schedule.get('name', 'Unknown')
        domains = schedule.get('domains', [])
        max_concurrency = schedule.get('max_concurrency', 3)
        
        print(f'[ScheduleEngine] Triggering schedule "{name}" for {len(domains)} domains', flush=True)
        
        # Create a batch job to track this
        batch_job = {
            'batch_name': f'Scheduled: {name} ({now_str[:16]})',
            'action': 'scheduled_pipeline',
            'targets': domains,
            'parameters': {
                'schedule_id': schedule.get('id'),
                'schedule_name': name,
                'max_concurrency': max_concurrency,
                'budget_cap': schedule.get('budget_cap'),
            },
            'status': 'running',
            'progress': 0,
            'total': len(domains),
            'started_at': now_str,
        }
        
        result = sh.supa_insert('batch_jobs', batch_job)
        
        # Update schedule last_run time
        sh.supa_update('pipeline_schedules', 'id', schedule.get('id'), {
            'last_run': now_str,
        })
        
        # Create notification
        sh.supa_insert('notifications', {
            'type': 'info',
            'title': f'Scheduled run started: {name}',
            'message': f'Triggered pipeline for {len(domains)} domains',
            'link': '/batch',
        })
        
        # Log to audit
        sh.log_audit('pipeline_schedules', 'schedule_triggered', {
            'schedule_id': schedule.get('id'),
            'schedule_name': name,
            'domains': len(domains),
        })
        
        # Actually trigger the pipeline execution
        self._execute_pipeline_for_schedule(name, domains, batch_job.get('id'), schedule.get('id'))
        
        print(f'[ScheduleEngine] Scheduled "{name}" triggered, batch job created', flush=True)
    
    def _execute_pipeline_for_schedule(self, name, domains, batch_job_id, schedule_id):
        """Execute the pipeline for each domain in the schedule via n8n API."""
        n8n_api_key = os.environ.get('N8N_API_KEY', '').strip()
        n8n_base = os.environ.get('N8N_BASE_URL', 'https://websiseo.app.n8n.cloud').rstrip('/')
        
        if not n8n_api_key:
            # API key not configured - update batch job and notify
            sh.supa_update('batch_jobs', 'id', batch_job_id, {
                'status': 'pending_manual_trigger',
                'error_message': 'N8N_API_KEY not configured. Set it in Render env vars to enable automatic pipeline execution.',
            })
            sh.supa_insert('notifications', {
                'type': 'warning',
                'title': f'Schedule "{name}" paused - n8n API key missing',
                'message': 'Configure N8N_API_KEY in Render to enable automatic pipeline execution.',
                'link': '/settings',
            })
            print(f'[ScheduleEngine] N8N_API_KEY not set. Batch job {batch_job_id} pending manual trigger.', flush=True)
            return
        
        # Load workflow map for domain → workflowId resolution
        workflow_map = self._load_workflow_map()
        
        # Execute pipeline via n8n API for each domain
        success_count = 0
        failed_count = 0
        errors = []
        
        for domain in (domains or []):
            try:
                result = self._trigger_n8n_workflow(n8n_base, n8n_api_key, domain, name, schedule_id, workflow_map)
                if result.get('success'):
                    success_count += 1
                else:
                    failed_count += 1
                    errors.append(f'{domain}: {result.get("error", "unknown")}')
            except Exception as e:
                failed_count += 1
                errors.append(f'{domain}: {str(e)}')
            
            # Small delay between triggers to avoid overwhelming the API
            time.sleep(2)
        
        # Update batch job with results
        final_status = 'completed' if failed_count == 0 else ('partial' if success_count > 0 else 'failed')
        sh.supa_update('batch_jobs', 'id', batch_job_id, {
            'status': final_status,
            'progress': 100,
            'result_summary': {
                'success': success_count,
                'failed': failed_count,
                'errors': errors[:10],  # Keep only first 10 errors
            },
        })
        
        # Create completion notification
        if failed_count == 0:
            sh.supa_insert('notifications', {
                'type': 'success',
                'title': f'Schedule "{name}" completed',
                'message': f'Successfully triggered pipeline for {success_count} domains',
                'link': '/batch',
            })
        else:
            sh.supa_insert('notifications', {
                'type': 'error',
                'title': f'Schedule "{name}" had errors',
                'message': f'{success_count} succeeded, {failed_count} failed. Check batch job for details.',
                'link': '/batch',
            })
        
        print(f'[ScheduleEngine] Pipeline execution: {success_count} succeeded, {failed_count} failed', flush=True)
    
    def _load_workflow_map(self):
        """Load domain → workflowId mapping from n8n-workflow-map.json."""
        try:
            map_path = os.path.join(ROOT, 'n8n-workflow-map.json')
            if os.path.exists(map_path):
                with open(map_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('domains', {})
        except Exception as e:
            print(f'[ScheduleEngine] Warning: could not load workflow map: {e}', flush=True)
        return {}
    
    def _find_workflow_by_domain(self, n8n_base, api_key, domain):
        """Find the n8n workflow ID for a domain by searching the API."""
        # First check local workflow map
        workflow_map = self._load_workflow_map()
        if domain in workflow_map:
            wf_id = workflow_map[domain].get('workflowId', '')
            if wf_id:
                return wf_id, workflow_map[domain].get('workflowName', domain)
        
        # Search n8n API for workflow matching domain name
        try:
            url = f'{n8n_base}/api/v1/workflows?limit=100'
            req = urllib.request.Request(url, headers={
                'X-N8N-API-KEY': api_key,
                'Accept': 'application/json',
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for wf in data.get('data', []):
                    wf_name = wf.get('name', '').lower()
                    if domain.lower() in wf_name:
                        return wf['id'], wf['name']
        except Exception as e:
            print(f'[ScheduleEngine] Warning: could not search n8n workflows: {e}', flush=True)
        
        return None, None
    
    def _trigger_n8n_workflow(self, n8n_base, api_key, domain, schedule_name, schedule_id, workflow_map):
        """Trigger the n8n workflow for a domain via the n8n API.
        
        Strategy:
        1. Find workflow by domain name
        2. Check if it has a Schedule Trigger node (runs automatically)
        3. If not active, activate it so the next schedule tick fires
        4. For immediate execution, check if workflow has a webhook we can POST to
        """
        # Find the workflow for this domain
        workflow_id, workflow_name = self._find_workflow_by_domain(n8n_base, api_key, domain)
        
        if not workflow_id:
            return {'success': False, 'error': f'No n8n workflow found for domain: {domain}'}
        
        try:
            # Get workflow details to check its trigger type
            url = f'{n8n_base}/api/v1/workflows/{urllib.parse.quote(workflow_id)}'
            req = urllib.request.Request(url, headers={
                'X-N8N-API-KEY': api_key,
                'Accept': 'application/json',
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                wf_data = json.loads(resp.read().decode('utf-8'))
            
            nodes = wf_data.get('nodes', [])
            has_schedule_trigger = any(
                n.get('type', '').startswith('n8n-nodes-base.scheduleTrigger') or
                n.get('type', '').startswith('@n8n/n8n-nodes-langchain') or
                n.get('type') == 'n8n-nodes-base.manualTrigger'
                for n in nodes
            )
            
            is_active = wf_data.get('active', False)
            
            if not is_active:
                # Activate the workflow so its trigger fires
                activate_url = f'{n8n_base}/api/v1/workflows/{urllib.parse.quote(workflow_id)}/activate'
                activate_req = urllib.request.Request(
                    activate_url,
                    data=b'{}',
                    headers={
                        'X-N8N-API-KEY': api_key,
                        'Content-Type': 'application/json',
                    },
                    method='PUT'
                )
                with urllib.request.urlopen(activate_req, timeout=30) as resp:
                    resp.read()
                
                print(f'[ScheduleEngine] Activated workflow "{workflow_name}" for {domain}', flush=True)
                return {
                    'success': True,
                    'status': 200,
                    'workflow_id': workflow_id,
                    'workflow_name': workflow_name,
                    'action': 'activated',
                    'message': f'Workflow activated for domain {domain}. Pipeline will run on next schedule tick.',
                }
            else:
                return {
                    'success': True,
                    'status': 200,
                    'workflow_id': workflow_id,
                    'workflow_name': workflow_name,
                    'action': 'already_active',
                    'message': f'Workflow already active for domain {domain}.',
                }
                
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')[:200] if hasattr(e, 'read') else ''
            return {'success': False, 'error': f'HTTP {e.code}: {body}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# ============================================================
# Global instance
# ============================================================
_schedule_engine = None

def get_schedule_engine():
    global _schedule_engine
    if _schedule_engine is None:
        _schedule_engine = ScheduleEngine()
    return _schedule_engine

def start_scheduler():
    """Start the background schedule engine."""
    engine = get_schedule_engine()
    engine.start()
    return engine

