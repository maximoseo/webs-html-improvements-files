"""
Email Notification System for N8N Stuck Projects
=================================================
Sends email alerts when critical stuck projects are detected.
Supports SMTP and Resend API.
"""

import os
import json
import smtplib
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone


class EmailNotifier:
    """Send email notifications for stuck project alerts."""

    def __init__(self):
        self.provider = os.getenv('NOTIFICATION_EMAIL_PROVIDER', 'smtp').lower()
        self.enabled = bool(os.getenv('NOTIFICATION_EMAIL_ENABLED', 'false').lower() == 'true')
        
        # SMTP config
        self.smtp_host = os.getenv('NOTIFICATION_SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('NOTIFICATION_SMTP_PORT', '587'))
        self.smtp_user = os.getenv('NOTIFICATION_SMTP_USER', '')
        self.smtp_password = os.getenv('NOTIFICATION_SMTP_PASSWORD', '')
        self.smtp_use_tls = os.getenv('NOTIFICATION_SMTP_TLS', 'true').lower() == 'true'
        
        # Resend config
        self.resend_api_key = os.getenv('RESEND_API_KEY', '')
        
        # Common
        self.from_email = os.getenv('NOTIFICATION_FROM_EMAIL', 'alerts@maximo-seo.ai')
        self.to_emails = os.getenv('NOTIFICATION_TO_EMAILS', '').split(',')
        self.to_emails = [e.strip() for e in self.to_emails if e.strip()]

    def is_configured(self):
        """Check if email is properly configured."""
        if not self.enabled:
            return False
        
        if self.provider == 'resend':
            return bool(self.resend_api_key and self.to_emails)
        else:  # smtp
            return bool(self.smtp_user and self.smtp_password and self.to_emails)

    def send_critical_alert(self, projects):
        """
        Send alert email for critical stuck projects.
        
        Args:
            projects: List of project dicts with name, error_summary, priority, etc.
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Email not configured'}
        
        if not projects:
            return {'success': False, 'error': 'No projects to alert about'}

        subject = f"🚨 {len(projects)} Critical N8N {'Project' if len(projects) == 1 else 'Projects'} Stuck!"
        html_body = self._generate_html_body(projects)
        text_body = self._generate_text_body(projects)

        try:
            if self.provider == 'resend':
                return self._send_via_resend(subject, html_body, text_body)
            else:
                return self._send_via_smtp(subject, html_body, text_body)
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _send_via_resend(self, subject, html_body, text_body):
        """Send email via Resend API."""
        url = 'https://api.resend.com/emails'
        payload = {
            'from': self.from_email,
            'to': self.to_emails,
            'subject': subject,
            'html': html_body,
            'text': text_body
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
            'Authorization': f'Bearer {self.resend_api_key}',
            'Content-Type': 'application/json'
        })
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode())

        return {
            'success': True,
            'message_id': result.get('id'),
            'provider': 'resend'
        }

    def _send_via_smtp(self, subject, html_body, text_body):
        """Send email via SMTP."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = ', '.join(self.to_emails)

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.smtp_use_tls:
                server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.from_email, self.to_emails, msg.as_string())

        return {
            'success': True,
            'provider': 'smtp',
            'sent_to': len(self.to_emails)
        }

    def _generate_html_body(self, projects):
        """Generate HTML email body."""
        rows = ''
        for i, p in enumerate(projects):
            priority_color = {'critical': '#ef4444', 'high': '#f97316', 'medium': '#eab308', 'low': '#3b82f6'}.get(p.get('priority', 'medium'), '#6b7280')
            rows += f'''
            <tr style="border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 12px 16px;">
                    <div style="font-weight: 600; color: #1f2937;">{p.get('name', 'Unknown')}</div>
                    <div style="font-size: 13px; color: #6b7280;">Client: {p.get('client_name', 'N/A')}</div>
                </td>
                <td style="padding: 12px 16px;">
                    <span style="background: {priority_color}20; color: {priority_color}; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">
                        {p.get('priority', 'medium').upper()}
                    </span>
                </td>
                <td style="padding: 12px 16px; color: #dc2626;">
                    {p.get('error_summary', 'No details')}
                </td>
                <td style="padding: 12px 16px; color: #6b7280; font-size: 13px;">
                    {p.get('stuck_since', 'Unknown')[:10] if p.get('stuck_since') else 'Unknown'}
                </td>
            </tr>'''

        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f3f4f6; }}
                .container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                .header {{ background: #ef4444; color: white; padding: 24px; }}
                .header h1 {{ margin: 0; font-size: 20px; }}
                .header p {{ margin: 8px 0 0; opacity: 0.9; font-size: 14px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ text-align: left; padding: 12px 16px; background: #f9fafb; font-size: 12px; text-transform: uppercase; color: #6b7280; border-bottom: 2px solid #e5e7eb; }}
                .footer {{ padding: 16px; background: #f9fafb; text-align: center; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 N8N Stuck Projects Alert</h1>
                    <p>{len(projects)} critical project(s) detected at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Project</th>
                            <th>Priority</th>
                            <th>Error</th>
                            <th>Stuck Since</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                <div class="footer">
                    <p>This alert was sent by Hermes N8N Stuck Projects Monitor.</p>
                    <p>Dashboard: https://html-redesign-dashboard.maximo-seo.ai/</p>
                </div>
            </div>
        </body>
        </html>'''

        return html

    def _generate_text_body(self, projects):
        """Generate plain text email body."""
        lines = [
            "🚨 N8N STUCK PROJECTS ALERT",
            "=" * 50,
            f"Detected {len(projects)} critical project(s) at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            ""
        ]

        for i, p in enumerate(projects, 1):
            lines.append(f"{i}. {p.get('name', 'Unknown')}")
            lines.append(f"   Priority: {p.get('priority', 'medium').upper()}")
            lines.append(f"   Client: {p.get('client_name', 'N/A')}")
            lines.append(f"   Error: {p.get('error_summary', 'No details')}")
            lines.append(f"   Stuck since: {p.get('stuck_since', 'Unknown')}")
            lines.append("")

        lines.append("-" * 50)
        lines.append("Dashboard: https://html-redesign-dashboard.maximo-seo.ai/")
        lines.append("Sent by Hermes N8N Stuck Projects Monitor")

        return "\n".join(lines)

    def test_email(self):
        """Send a test email to verify configuration."""
        test_project = {
            'name': 'Test Project',
            'client_name': 'Test Client',
            'priority': 'critical',
            'error_summary': 'This is a test alert',
            'stuck_since': datetime.now(timezone.utc).isoformat()
        }
        return self.send_critical_alert([test_project])


def create_notifier():
    """Factory function to create EmailNotifier."""
    return EmailNotifier()
