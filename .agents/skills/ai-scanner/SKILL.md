# SKILL: AI Scanner — LLM Security Assessment
**Source:** https://github.com/0din-ai/ai-scanner
**Domain:** code
**Trigger:** When you need to security-test or penetration-test an AI/LLM system for vulnerabilities

## Summary
Open-source web app for AI model security assessments using NVIDIA garak. Runs 179 probes across 35 vulnerability families aligned with OWASP LLM Top 10.

## Key Patterns
- Deploy via Docker Compose one-liner: `curl -sL https://raw.githubusercontent.com/0din-ai/ai-scanner/main/scripts/install.sh | bash`
- Supports multi-target scanning: API-based LLMs and browser-based chat UIs
- Attack Success Rate (ASR) scoring with trend tracking
- PDF report export, SIEM integration (Splunk/Rsyslog), multi-tenant

## Usage
Use when auditing LLM deployments for security vulnerabilities before production. Covers OWASP LLM Top 10.

## Code/Template
```bash
curl -O https://raw.githubusercontent.com/0din-ai/ai-scanner/main/dist/docker-compose.yml
curl -O https://raw.githubusercontent.com/0din-ai/ai-scanner/main/.env.example
cp .env.example .env
# Set SECRET_KEY_BASE and POSTGRES_PASSWORD in .env
docker compose up -d
# Login: admin@example.com / password
```
