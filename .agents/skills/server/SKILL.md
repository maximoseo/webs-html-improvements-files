# SKILL: Sync-in Server — Self-Hosted File Collaboration
**Source:** https://github.com/Sync-in/server
**Domain:** code
**Trigger:** When setting up self-hosted collaborative file sharing with OIDC, LDAP, WebDAV, and real-time editing

## Summary
Self-hosted collaboration platform with full file ownership. OIDC/SSO, LDAP, MFA, Collabora Online + OnlyOffice integration, WebDAV, full-text search, fine-grained permissions. AGPL-3.0.

## Key Patterns
- Deploy via Docker or NPM: `docker run -p 80:80 syncin/server` or `npm install @sync-in/server`
- Collabora Online + OnlyOffice for collaborative document editing
- WebDAV support for native OS file access
- OIDC SSO for enterprise identity

## Usage
Use as self-hosted alternative to Nextcloud or SharePoint with modern UI and AI-ready APIs.

## Code/Template
```bash
# Docker (recommended)
docker run -p 80:80 syncin/server

# NPM
npm install -g @sync-in/server && sync-in-server start

# Full docs: https://sync-in.com/docs/setup-guide/docker
```
