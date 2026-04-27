-- n8n Workflow Sync schema
-- SAFETY: This migration creates storage tables only.
-- It does not call n8n, does not execute HTTP requests, and does not modify workflows.
-- Original workflow rows are read-only reference copies from n8n GET requests.
-- Update packages stored here are MANUAL IMPORT ONLY.

create extension if not exists pgcrypto;

create table if not exists n8n_workflows (
  id uuid primary key default gen_random_uuid(),
  n8n_workflow_id varchar(50) not null,
  name varchar(500) not null,
  domain varchar(255),
  tags text[] default '{}',
  workflow_json jsonb not null,
  is_active boolean,
  node_count integer default 0,
  html_node_count integer default 0,
  downloaded_at timestamptz default now(),
  last_synced_at timestamptz default now(),
  unique(n8n_workflow_id)
);

comment on table n8n_workflows is 'Read-only reference copies of n8n workflows downloaded via GET only.';

create table if not exists n8n_html_templates (
  id uuid primary key default gen_random_uuid(),
  workflow_id uuid references n8n_workflows(id) on delete cascade,
  node_name varchar(500),
  node_type varchar(100),
  html_content text not null,
  source varchar(50),
  domain varchar(255),
  extracted_at timestamptz default now()
);

comment on table n8n_html_templates is 'Extracted original HTML templates from read-only workflow references.';

create table if not exists n8n_improved_templates (
  id uuid primary key default gen_random_uuid(),
  original_template_id uuid references n8n_html_templates(id) on delete set null,
  workflow_id uuid references n8n_workflows(id) on delete set null,
  domain varchar(255) not null,
  agent_name varchar(100) not null,
  model_name varchar(100) not null,
  provider varchar(100) not null,
  improved_html text not null,
  improvement_prompt text,
  n8n_update_json jsonb,
  changelog text,
  quality_score decimal(5,2),
  file_size_bytes integer,
  created_date date not null default current_date,
  created_at timestamptz default now(),
  safety_note text not null default 'MANUAL IMPORT ONLY — this record must not be auto-applied to n8n.'
);

comment on table n8n_improved_templates is 'Agent-generated improved template versions. MANUAL IMPORT ONLY; never auto-applied to n8n.';

create table if not exists n8n_improvement_prompts (
  id uuid primary key default gen_random_uuid(),
  domain varchar(255),
  agent_name varchar(100),
  model_name varchar(100),
  prompt_text text not null,
  prompt_type varchar(50),
  was_effective boolean,
  effectiveness_score integer check (effectiveness_score is null or (effectiveness_score between 1 and 10)),
  created_at timestamptz default now()
);

create table if not exists n8n_sync_log (
  id uuid primary key default gen_random_uuid(),
  action varchar(50) not null,
  workflow_count integer default 0,
  html_nodes_found integer default 0,
  status varchar(20) not null,
  error_message text,
  synced_at timestamptz default now()
);

create index if not exists idx_n8n_workflows_domain on n8n_workflows(domain);
create index if not exists idx_n8n_html_domain on n8n_html_templates(domain);
create index if not exists idx_improved_domain on n8n_improved_templates(domain, agent_name, created_date desc);
create index if not exists idx_improved_agent on n8n_improved_templates(agent_name, created_date desc);
create index if not exists idx_n8n_sync_log_synced_at on n8n_sync_log(synced_at desc);

-- Optional RLS can be enabled later after dashboard service-role access is finalized.
-- No policies are enabled in this migration to avoid accidentally breaking existing dashboard reads.
