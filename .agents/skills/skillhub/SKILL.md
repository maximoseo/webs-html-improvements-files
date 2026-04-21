# SKILL: SkillHub — Enterprise Agent Skill Registry
**Source:** https://github.com/iflytek/skillhub
**Domain:** agent-tools
**Trigger:** Use when setting up a private, self-hosted enterprise registry for publishing, discovering, and managing reusable AI agent skill packages across an organization.

## Summary
SkillHub is a self-hosted, enterprise-grade skill registry (Java 21 + React 19) where teams publish and discover agent skills with semantic versioning, namespace-based team management, review governance, audit logs, and pluggable S3/MinIO storage.

## Key Patterns
- Team namespaces with Owner/Admin/Member roles
- Semantic versioning + tags (beta, stable, latest)
- Full-text search with filters by namespace, downloads, ratings, recency
- Governance: namespace admins review; platform admins gate global promotions
- Pluggable storage: local filesystem (dev) or S3/MinIO (production)
- CLI-first with ClawHub-compatible API for existing registry clients
- One-command local start: curl install script

## Usage
When an enterprise team needs a private alternative to public skill registries, with access control, audit trails, and governance over which skills are approved for production agent use.

## Code/Template
```bash
# Start full local stack
curl -fsSL https://imageless.oss-cn-beijing.aliyuncs.com/runtime.sh | sh -s -- up
# Access at configured public URL

# Publish a skill
clawhub publish ./my-skill --namespace my-team

# Install a skill
clawhub install my-team/my-skill
```
