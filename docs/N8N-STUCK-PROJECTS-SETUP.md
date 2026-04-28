# N8N Stuck Projects - Setup Guide

## Overview
This feature adds a new "N8N Stuck Projects" tab to the Hermes dashboard that monitors and alerts on stuck n8n automation workflows.

## Quick Start

### 1. Create Supabase Tables

Run the SQL migration in your Supabase dashboard:
- File: `docs/supabase-migrations/001_create_stuck_projects.sql`
- Go to Supabase → SQL Editor → paste and run

This creates:
- `stuck_projects` - Main table for tracking stuck projects
- `stuck_projects_history` - Change history for audit trail

### 2. Configure Environment Variables (Render)

Add these to your Render environment variables:

#### Pini Integration
```
PINI_URL=https://pini.websmail.net
PINI_USERNAME=tomer
PINI_PASSWORD=your_password_here
```

#### Email Notifications (Optional)
Choose one provider:

**Option A: Resend (Recommended)**
```
NOTIFICATION_EMAIL_ENABLED=true
NOTIFICATION_EMAIL_PROVIDER=resend
NOTIFICATION_FROM_EMAIL=alerts@maximo-seo.ai
NOTIFICATION_TO_EMAILS=tomer@example.com
RESEND_API_KEY=re_xxxxxxxx
```

**Option B: SMTP**
```
NOTIFICATION_EMAIL_ENABLED=true
NOTIFICATION_EMAIL_PROVIDER=smtp
NOTIFICATION_FROM_EMAIL=alerts@maximo-seo.ai
NOTIFICATION_TO_EMAILS=tomer@example.com
NOTIFICATION_SMTP_HOST=smtp.gmail.com
NOTIFICATION_SMTP_PORT=587
NOTIFICATION_SMTP_USER=your@gmail.com
NOTIFICATION_SMTP_PASSWORD=your_app_password
NOTIFICATION_SMTP_TLS=true
```

#### Sync Interval (Optional)
```
STUCK_PROJECTS_SYNC_INTERVAL=30  # minutes (default: 30)
```

### 3. Deploy

The feature auto-deploys when you push to main:
```bash
git add -A
git commit -m "feat: add N8N stuck projects monitoring"
git push origin main
```

### 4. Verify

1. Open the dashboard
2. Click "⚠️ N8N Stuck Projects" tab
3. Click "🔄 Sync from Pini" to manually sync
4. Check that projects appear in the list

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stuck-projects` | List stuck projects (with filters) |
| GET | `/api/stuck-projects/{id}` | Get single project details |
| GET | `/api/stuck-projects/summary` | Get summary counts |
| GET | `/api/stuck-projects/sync/status` | Get sync scheduler status |
| POST | `/api/stuck-projects/sync` | Trigger manual sync |
| PATCH | `/api/stuck-projects/{id}` | Update project (resolve, snooze, etc.) |
| GET | `/api/stuck-projects/alerts/test-email` | Send test email |

### Query Parameters for GET /api/stuck-projects
- `status` - Filter by status (default: "stuck,error,failed")
- `priority` - Filter by priority (default: "all")
- `client` - Filter by client name
- `search` - Search in name, error, client
- `sort` - Sort field (default: "stuck_since")
- `order` - asc or desc (default: "desc")
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 50, max: 200)

## Files Added

| File | Purpose |
|------|---------|
| `pini_client.py` | Pini API integration client |
| `sync_scheduler.py` | Background auto-sync scheduler |
| `email_notifier.py` | Email notification system |
| `docs/supabase-migrations/001_create_stuck_projects.sql` | Database migration |

## Files Modified

| File | Changes |
|------|---------|
| `server.py` | Added 7 new API endpoints + scheduler startup |
| `index.html` | Added tab button, page content, and JavaScript |

## Features

### Dashboard Tab
- Summary bar showing counts by priority
- Search and filter by status, priority
- Project cards with error details
- Manual sync button
- Auto-refresh on tab open

### Auto-Sync
- Runs every 30 minutes (configurable)
- Fetches stuck projects from Pini
- Stores in Supabase
- Triggers email alerts for critical projects

### Email Alerts
- Sent when new critical projects are detected
- Beautiful HTML email with project details
- Supports Resend API and SMTP

### Pini Integration
- Hybrid approach: API first, scraping fallback
- Auto-discovers API endpoints
- Handles different response formats
- Filters for stuck/error/failed projects

## Troubleshooting

### Tab not showing
- Clear browser cache
- Check that index.html deployed successfully

### Sync fails
- Check Render logs for error messages
- Verify PINI_URL, PINI_USERNAME, PINI_PASSWORD are set
- Test with manual sync button

### Email not sending
- Check NOTIFICATION_EMAIL_ENABLED=true
- Verify email provider credentials
- Test with `/api/stuck-projects/alerts/test-email`

### Supabase errors
- Ensure migration SQL was run
- Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set
- Verify table names match (stuck_projects, stuck_projects_history)

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Pini      │────>│  Pini Client │────>│   Server    │
│   (n8n PM)  │     │  (hybrid)    │     │  (Python)   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    ▼                           ▼                           ▼
              ┌───────────┐            ┌──────────────┐            ┌────────────┐
              │  Supabase │            │  Dashboard   │            │   Email    │
              │ (storage) │            │  (React/HTML)│            │  (alerts)  │
              └───────────┘            └──────────────┘            └────────────┘
```
