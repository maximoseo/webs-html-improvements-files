"""
Auto-Sync Scheduler for N8N Stuck Projects
============================================
Runs periodic sync with Pini and triggers alerts for critical projects.
Uses threading for background execution without blocking the main server.
"""

import os
import threading
import time
import json
import urllib.request
from datetime import datetime, timezone, timedelta


class StuckProjectsSyncScheduler:
    """Background scheduler for automatic Pini sync."""

    def __init__(self, interval_minutes=None):
        self.interval_minutes = interval_minutes or int(os.getenv('STUCK_PROJECTS_SYNC_INTERVAL', '30'))
        self.running = False
        self.thread = None
        self.last_sync_time = None
        self.last_sync_result = None
        self.sync_count = 0
        self.lock = threading.Lock()

    def start(self):
        """Start the background sync scheduler."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.thread.start()
        print(f"[SyncScheduler] Started with {self.interval_minutes}min interval")

    def stop(self):
        """Stop the background sync scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("[SyncScheduler] Stopped")

    def _sync_loop(self):
        """Main sync loop - runs in background thread."""
        while self.running:
            try:
                self._run_sync()
            except Exception as e:
                print(f"[SyncScheduler] Error in sync loop: {e}")

            # Sleep for interval (check running flag every minute)
            for _ in range(self.interval_minutes):
                if not self.running:
                    break
                time.sleep(60)

    def _run_sync(self):
        """Execute a single sync operation."""
        with self.lock:
            try:
                # Import Pini client
                try:
                    from pini_client import create_pini_client
                except ImportError:
                    print("[SyncScheduler] pini_client not available")
                    return

                client = create_pini_client()
                if not client.username or not client.password:
                    print("[SyncScheduler] Pini credentials not configured")
                    return

                # Fetch projects
                result = client.fetch_projects()
                projects = result.get('projects', [])

                # Store in Supabase
                cfg = self._get_supabase_config()
                synced = 0
                new_critical = []

                if cfg.get('url') and cfg.get('key'):
                    for p in projects:
                        try:
                            is_new = self._upsert_project(cfg, p)
                            if is_new and p.get('priority') == 'critical':
                                new_critical.append(p)
                            synced += 1
                        except Exception as e:
                            print(f"[SyncScheduler] Error syncing project {p.get('name', 'unknown')}: {e}")

                # Trigger alerts for new critical projects
                if new_critical:
                    self._trigger_alerts(new_critical)

                self.last_sync_time = datetime.now(timezone.utc)
                self.last_sync_result = {
                    'success': True,
                    'projects_synced': synced,
                    'new_critical': len(new_critical),
                    'total_stuck': len(projects)
                }
                self.sync_count += 1

                print(f"[SyncScheduler] Sync complete: {synced} projects, {len(new_critical)} new critical")

            except Exception as e:
                self.last_sync_result = {'success': False, 'error': str(e)}
                print(f"[SyncScheduler] Sync failed: {e}")

    def _get_supabase_config(self):
        """Get Supabase configuration."""
        url = (os.getenv('SUPABASE_URL') or '').strip().rstrip('/')
        key = (
            (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or '').strip()
            or (os.getenv('SUPABASE_ANON_KEY') or '').strip()
        )
        return {'url': url, 'key': key}

    def _upsert_project(self, cfg, project):
        """
        Upsert a project to Supabase.
        Returns True if the project is new.
        """
        pini_id = project.get('pini_project_id', '')
        if not pini_id:
            return False

        # Check if exists
        check_url = f"{cfg['url']}/rest/v1/stuck_projects?pini_project_id=eq.{pini_id}"
        check_req = urllib.request.Request(check_url, headers={
            'apikey': cfg['key'], 'Authorization': f"Bearer {cfg['key']}",
            'Content-Type': 'application/json'
        })
        check_resp = urllib.request.urlopen(check_req, timeout=10)
        existing = json.loads(check_resp.read().decode())

        payload = {
            'pini_project_id': pini_id,
            'name': project.get('name', 'Unknown'),
            'client_name': project.get('client_name'),
            'workflow_id': project.get('workflow_id'),
            'workflow_url': project.get('workflow_url'),
            'status': project.get('status', 'stuck'),
            'priority': project.get('priority', 'medium'),
            'error_summary': project.get('error_summary'),
            'error_details': project.get('error_details'),
            'error_type': project.get('error_type'),
            'stuck_since': project.get('stuck_since'),
            'last_successful': project.get('last_successful'),
            'assigned_to': project.get('assigned_to'),
            'tags': project.get('tags', []),
            'notes': project.get('notes'),
            'pini_raw_data': project.get('pini_raw_data', {})
        }

        if existing:
            # Update
            update_url = f"{cfg['url']}/rest/v1/stuck_projects?id=eq.{existing[0]['id']}"
            update_req = urllib.request.Request(update_url, data=json.dumps(payload).encode(), headers={
                'apikey': cfg['key'], 'Authorization': f"Bearer {cfg['key']}",
                'Content-Type': 'application/json'
            }, method='PATCH')
            urllib.request.urlopen(update_req, timeout=10)
            return False
        else:
            # Insert
            insert_url = f"{cfg['url']}/rest/v1/stuck_projects"
            insert_req = urllib.request.Request(insert_url, data=json.dumps(payload).encode(), headers={
                'apikey': cfg['key'], 'Authorization': f"Bearer {cfg['key']}",
                'Content-Type': 'application/json'
            })
            urllib.request.urlopen(insert_req, timeout=10)
            return True

    def _trigger_alerts(self, critical_projects):
        """Trigger alerts for new critical projects."""
        # Log to console
        for p in critical_projects:
            print(f"[ALERT] 🚨 NEW CRITICAL: {p.get('name', 'Unknown')} - {p.get('error_summary', 'No details')}")

        # Send email notification if configured
        try:
            from email_notifier import create_notifier
            notifier = create_notifier()
            if notifier.is_configured():
                result = notifier.send_critical_alert(critical_projects)
                if result.get('success'):
                    print(f"[ALERT] 📧 Email sent to {notifier.to_emails}")
                else:
                    print(f"[ALERT] 📧 Email failed: {result.get('error', 'unknown')}")
        except ImportError:
            print("[ALERT] email_notifier not available")
        except Exception as e:
            print(f"[ALERT] Email notification failed: {e}")



# Global scheduler instance
scheduler = None

def get_scheduler():
    """Get or create the global scheduler instance."""
    global scheduler
    if scheduler is None:
        scheduler = StuckProjectsSyncScheduler()
    return scheduler

def start_scheduler():
    """Start the global scheduler."""
    s = get_scheduler()
    s.start()
    return s

def stop_scheduler():
    """Stop the global scheduler."""
    global scheduler
    if scheduler:
        scheduler.stop()
        scheduler = None
