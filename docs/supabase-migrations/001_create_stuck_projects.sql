-- ============================================================
-- Migration 001: N8N Stuck Projects Table
-- Created: 2026-04-28
-- Purpose: Track n8n automation projects that are stuck/broken
-- Source: Synced from Pini (pini.websmail.net)
-- ============================================================

-- Main table: stuck projects
CREATE TABLE IF NOT EXISTS stuck_projects (
  id                UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  pini_project_id   TEXT NOT NULL,
  name              TEXT NOT NULL,
  client_name       TEXT,
  workflow_id       TEXT,
  workflow_url      TEXT,

  -- Status & Priority
  status            TEXT NOT NULL DEFAULT 'stuck'
    CHECK (status IN ('stuck', 'error', 'failed', 'resolved', 'snoozed')),
  priority          TEXT NOT NULL DEFAULT 'medium'
    CHECK (priority IN ('critical', 'high', 'medium', 'low')),

  -- Error Information
  error_summary     TEXT,
  error_details     TEXT,
  error_type        TEXT,

  -- Timestamps
  stuck_since       TIMESTAMPTZ,
  last_successful   TIMESTAMPTZ,
  first_detected    TIMESTAMPTZ DEFAULT NOW(),
  resolved_at       TIMESTAMPTZ,
  snoozed_until     TIMESTAMPTZ,

  -- Assignment
  assigned_to       TEXT,
  assigned_agent    TEXT,

  -- Metadata
  tags              TEXT[] DEFAULT '{}',
  notes             TEXT,
  suggested_fix     TEXT,
  pini_raw_data     JSONB DEFAULT '{}',

  -- Tracking
  is_new            BOOLEAN DEFAULT TRUE,
  view_count        INTEGER DEFAULT 0,

  -- Standard
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE (pini_project_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_stuck_projects_status ON stuck_projects(status);
CREATE INDEX IF NOT EXISTS idx_stuck_projects_priority ON stuck_projects(priority);
CREATE INDEX IF NOT EXISTS idx_stuck_projects_client ON stuck_projects(client_name);
CREATE INDEX IF NOT EXISTS idx_stuck_projects_updated ON stuck_projects(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_stuck_projects_is_new ON stuck_projects(is_new) WHERE is_new = TRUE;

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_stuck_projects_updated_at
  BEFORE UPDATE ON stuck_projects
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Change history table
CREATE TABLE IF NOT EXISTS stuck_projects_history (
  id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id      UUID NOT NULL REFERENCES stuck_projects(id) ON DELETE CASCADE,
  field_changed   TEXT NOT NULL,
  old_value       TEXT,
  new_value       TEXT,
  changed_by      TEXT DEFAULT 'system',
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stuck_history_project ON stuck_projects_history(project_id);
CREATE INDEX IF NOT EXISTS idx_stuck_history_created ON stuck_projects_history(created_at DESC);

-- RLS Policies (if RLS is enabled)
ALTER TABLE stuck_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE stuck_projects_history ENABLE ROW LEVEL SECURITY;

-- Allow authenticated users full access
CREATE POLICY "Allow all for authenticated" ON stuck_projects
  FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all history for authenticated" ON stuck_projects_history
  FOR ALL USING (auth.role() = 'authenticated');

-- Public read access (for dashboard)
CREATE POLICY "Allow public read" ON stuck_projects
  FOR SELECT USING (true);

CREATE POLICY "Allow public read history" ON stuck_projects_history
  FOR SELECT USING (true);
