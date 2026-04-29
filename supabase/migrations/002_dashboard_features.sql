-- ============================================================
-- Migration 002: Hermes Dashboard — Missing Features Tables
-- Created: 2026-04-28
-- Purpose: 12 new tables + views for the 15-feature roadmap
-- Source: hermes-dashboard-missing-features-plan.md
-- ALL ADDITIVE — no existing tables modified
-- ============================================================

-- 1. Notifications
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT,
  type TEXT CHECK (type IN ('error','warning','info','success')),
  title TEXT NOT NULL,
  message TEXT,
  link TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(is_read, created_at DESC) WHERE is_read = FALSE;
CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at DESC);

-- 2. Alert Rules
CREATE TABLE IF NOT EXISTS alert_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_type TEXT NOT NULL,
  threshold JSONB,
  channels TEXT[],
  is_active BOOLEAN DEFAULT TRUE
);

-- 3. Agent Traces (observability)
CREATE TABLE IF NOT EXISTS agent_traces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID,
  domain TEXT,
  subdomain TEXT,
  agent_name TEXT NOT NULL,
  model_name TEXT NOT NULL,
  step_order INT NOT NULL,
  prompt_tokens INT,
  completion_tokens INT,
  cost_usd DECIMAL(10,6),
  duration_ms INT,
  status TEXT CHECK (status IN ('success','warning','error')),
  score INT,
  prompt_text TEXT,
  response_text TEXT,
  error_message TEXT,
  cache_hit_ratio DECIMAL(3,2),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_traces_run ON agent_traces(run_id);
CREATE INDEX IF NOT EXISTS idx_traces_domain ON agent_traces(domain, subdomain);
CREATE INDEX IF NOT EXISTS idx_traces_created ON agent_traces(created_at DESC);

-- 4. Template Versions (for A/B testing)
CREATE TABLE IF NOT EXISTS template_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain TEXT NOT NULL,
  subdomain TEXT NOT NULL,
  page_path TEXT NOT NULL,
  agent_name TEXT NOT NULL,
  model_name TEXT NOT NULL,
  html_content TEXT NOT NULL,
  scores JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_templates_domain ON template_versions(domain, subdomain);
CREATE INDEX IF NOT EXISTS idx_templates_active ON template_versions(domain, subdomain, is_active) WHERE is_active = TRUE;

-- 5. A/B Tests
CREATE TABLE IF NOT EXISTS ab_tests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain TEXT NOT NULL,
  page_path TEXT NOT NULL,
  version_a UUID REFERENCES template_versions(id),
  version_b UUID REFERENCES template_versions(id),
  winner UUID REFERENCES template_versions(id),
  decided_at TIMESTAMPTZ,
  decided_by TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ab_domain ON ab_tests(domain, page_path);

-- 6. Client Reports
CREATE TABLE IF NOT EXISTS client_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain TEXT NOT NULL,
  report_type TEXT CHECK (report_type IN ('weekly','monthly','custom')),
  date_from DATE,
  date_to DATE,
  content JSONB,
  pdf_url TEXT,
  sent_at TIMESTAMPTZ,
  sent_to TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reports_domain ON client_reports(domain, created_at DESC);

-- 7. Report Schedules
CREATE TABLE IF NOT EXISTS report_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain TEXT NOT NULL,
  frequency TEXT CHECK (frequency IN ('weekly','monthly')),
  day_of_week INT,
  day_of_month INT,
  send_to TEXT[],
  is_active BOOLEAN DEFAULT TRUE
);

-- 8. Batch Jobs
CREATE TABLE IF NOT EXISTS batch_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  batch_name TEXT,
  action TEXT NOT NULL,
  targets JSONB NOT NULL,
  parameters JSONB,
  status TEXT DEFAULT 'queued',
  progress INT DEFAULT 0,
  total INT NOT NULL,
  cost_usd DECIMAL(10,4) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_batch_status ON batch_jobs(status, created_at DESC);

-- 9. Budget Limits
CREATE TABLE IF NOT EXISTS budget_limits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scope TEXT CHECK (scope IN ('global','client')),
  domain TEXT,
  period TEXT CHECK (period IN ('daily','weekly','monthly')),
  limit_usd DECIMAL(10,2),
  action TEXT DEFAULT 'alert' CHECK (action IN ('alert','pause')),
  is_active BOOLEAN DEFAULT TRUE
);

-- 10. Pipeline Schedules
CREATE TABLE IF NOT EXISTS pipeline_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  domains JSONB NOT NULL,
  cron_expression TEXT,
  trigger_type TEXT DEFAULT 'cron',
  agent_config JSONB,
  budget_cap DECIMAL(10,2),
  max_concurrency INT DEFAULT 3,
  is_active BOOLEAN DEFAULT TRUE,
  last_run TIMESTAMPTZ,
  next_run TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_schedules_active ON pipeline_schedules(is_active) WHERE is_active = TRUE;

-- 11. Notes (Collaboration)
CREATE TABLE IF NOT EXISTS notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT CHECK (entity_type IN ('domain','subdomain','template','run')),
  entity_id TEXT NOT NULL,
  content TEXT NOT NULL,
  author TEXT,
  is_pinned BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_notes_entity ON notes(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_notes_pinned ON notes(entity_type, entity_id, is_pinned) WHERE is_pinned = TRUE;

-- 12. Audit Log
CREATE TABLE IF NOT EXISTS audit_log (
  id BIGSERIAL PRIMARY KEY,
  table_name TEXT NOT NULL,
  action TEXT NOT NULL,
  record_id UUID,
  changes JSONB,
  previous_values JSONB,
  user_id TEXT,
  ip_address TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_table ON audit_log(table_name, created_at DESC);

-- 13. Feature Flags
CREATE TABLE IF NOT EXISTS feature_flags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  flag_name TEXT UNIQUE NOT NULL,
  is_enabled BOOLEAN DEFAULT TRUE,
  description TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 14. Cost Summary View
CREATE OR REPLACE VIEW v_cost_summary AS
SELECT
  DATE(created_at) as date,
  COALESCE(run_id::text, 'unknown') as run_id,
  agent_name,
  model_name,
  COUNT(*) as run_count,
  COALESCE(SUM(cost_usd), 0) as total_cost,
  COALESCE(AVG(cost_usd), 0) as avg_cost
FROM agent_traces
GROUP BY DATE(created_at), run_id, agent_name, model_name;

-- 15. Client Overview View
CREATE OR REPLACE VIEW v_client_overview AS
SELECT 
  COALESCE(domain, 'unknown') as domain,
  COUNT(DISTINCT subdomain) as subdomain_count,
  COUNT(*) FILTER (WHERE status = 'success') as success_count,
  COUNT(*) as total_count,
  MAX(created_at) as last_run,
  COALESCE(SUM(cost_usd) FILTER (WHERE created_at > NOW() - INTERVAL '1 day'), 0) as daily_cost,
  COALESCE(AVG(score), 0) as avg_health
FROM agent_traces
GROUP BY domain;

-- ==========================================
-- RLS Policies (public read for dashboard)
-- ==========================================
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_traces ENABLE ROW LEVEL SECURITY;
ALTER TABLE template_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ab_tests ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE batch_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_limits ENABLE ROW LEVEL SECURITY;
ALTER TABLE pipeline_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE feature_flags ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE
  t TEXT;
BEGIN
  FOR t IN SELECT unnest(ARRAY[
    'notifications','alert_rules','agent_traces','template_versions',
    'ab_tests','client_reports','report_schedules','batch_jobs',
    'budget_limits','pipeline_schedules','notes','audit_log','feature_flags'
  ]) LOOP
    EXECUTE format('DROP POLICY IF EXISTS "public_read" ON %I', t);
    EXECUTE format('CREATE POLICY "public_read" ON %I FOR SELECT USING (true)', t);
  END LOOP;
END $$;

-- ==========================================
-- Seed Data: Feature Flags
-- ==========================================
INSERT INTO feature_flags (flag_name, description) VALUES
  ('notification_center', 'Notification bell + alerts system'),
  ('search_filters', 'Global search with Cmd+K'),
  ('quick_actions', 'Keyboard shortcuts + command palette'),
  ('cost_tracker', 'Cost tracking and budget alerts'),
  ('client_overview', 'Client overview home page'),
  ('agent_traces', 'Agent observability trace viewer'),
  ('batch_operations', 'Batch operations and bulk actions'),
  ('audit_log', 'Audit log and change history'),
  ('ab_testing', 'A/B testing and template comparison'),
  ('automated_reports', 'Automated client reporting'),
  ('scheduled_runs', 'Scheduled pipeline runs'),
  ('data_export', 'Data export hub'),
  ('collaboration_notes', 'Team collaboration notes'),
  ('pwa_mobile', 'Progressive web app features')
ON CONFLICT (flag_name) DO NOTHING;

-- ==========================================
-- Seed Data: Default Alert Rules
-- ==========================================
INSERT INTO alert_rules (rule_type, threshold, channels, is_active) VALUES
  ('pipeline_failure', '{"severity": "critical"}', ARRAY['dashboard','telegram'], true),
  ('low_score', '{"threshold": 70, "severity": "warning"}', ARRAY['dashboard'], true),
  ('budget_exceeded', '{"severity": "warning"}', ARRAY['dashboard','telegram'], true),
  ('rate_limited', '{"severity": "warning"}', ARRAY['dashboard'], true)
ON CONFLICT DO NOTHING;
