-- Migration: Core Features (Versions & Batch Processing)
-- Corresponding to Sub-Agent 4 Tasks

-- Projects table (assuming it exists, but creating a dummy reference if needed for the schema)
CREATE TABLE IF NOT EXISTS projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES auth.users(id),
    name text NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- Versions
CREATE TABLE IF NOT EXISTS versions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid REFERENCES projects(id) ON DELETE CASCADE,
  version_number integer NOT NULL,
  html_url text NOT NULL,
  notes text,
  created_at timestamptz DEFAULT now()
);

-- Batch Jobs
CREATE TABLE IF NOT EXISTS batch_jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  status text DEFAULT 'pending',
  total_items integer NOT NULL,
  completed_items integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Batch Items
CREATE TABLE IF NOT EXISTS batch_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  batch_id uuid REFERENCES batch_jobs(id) ON DELETE CASCADE,
  url text NOT NULL,
  status text DEFAULT 'queued',
  result_url text,
  score integer,
  error text,
  created_at timestamptz DEFAULT now()
);

-- Public Previews (Task 5.1)
CREATE TABLE IF NOT EXISTS public_previews (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid REFERENCES projects(id) ON DELETE CASCADE,
  token uuid NOT NULL DEFAULT gen_random_uuid(),
  expires_at timestamptz NOT NULL,
  created_at timestamptz DEFAULT now()
);
